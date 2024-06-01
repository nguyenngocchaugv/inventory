# -*- coding: utf-8 -*-
"""Machine views."""
from flask import (
  Blueprint,
  flash,
  jsonify,
  redirect,
  render_template,
  url_for,
  request
)
from flask import current_app
from flask_login import login_required
from sqlalchemy import desc
from inventory.machine.forms import MachineForm
from inventory.machine.models import Machine, MachineStatusEnum, RentInvoice, RentInvoiceHistory, RentInvoiceStatusEnum
from inventory.user.models import User
from inventory.utils import flash_errors

blueprint = Blueprint("machine", __name__, url_prefix="/machines", static_folder="../static")


@blueprint.route("/")
@login_required
def machines():
  """List machines."""
  machines = Machine.query.filter_by(is_deleted=False).order_by(desc(Machine.id)).all()
  
  # Query the User table and create a dictionary where the keys are user IDs and the values are user emails
  users = {user.id: user.email for user in User.query.all()}
  # For each machine, get the emails of the users who created and updated it from the dictionary
  for machine in machines:  
    machine.created_by_email = users.get(machine.created_by)
    machine.updated_by_email = users.get(machine.updated_by)
    
  return render_template("machines/machines.html", machines=machines)

@blueprint.route("/search", methods=["GET"])
def search():
  """Search machines."""
  search_term = request.args.get('q', '')
  if search_term == '':  # Show all machines if no search term
    return redirect(url_for('machine.machines'))
  
  machines = Machine.query.filter_by(is_deleted=False).filter(Machine.name.contains(search_term)).order_by(desc(Machine.id)).all()
  
  # Query the User table and create a dictionary where the keys are user IDs and the values are user emails
  users = {user.id: user.email for user in User.query.all()}
  # For each machine, get the emails of the users who created and updated it from the dictionary
  for machine in machines:  
    machine.created_by_email = users.get(machine.created_by)
    machine.updated_by_email = users.get(machine.updated_by)
    
  return render_template("machines/machines.html", machines=machines, search_term=search_term)

@blueprint.route('/<int:machine_id>', methods=['GET'])
@login_required
def view_machine(machine_id):
  machine = Machine.query.get(machine_id)
  if machine and not machine.is_deleted:
    form = MachineForm(obj=machine)
    return render_template('machines/machine.html', machine=machine, form=form, mode='View')
  else:
    flash("Machine not found.", "danger")
    return redirect(url_for('machine.machines'))

@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_machine():
  """Create a new machine."""
  form = MachineForm(request.form)
  # current_app.logger.info(form.data)

  if form.validate_on_submit():
    Machine.create(
      name=form.name.data,
      description=form.description.data,
      type=form.type.data,
      serial=form.serial.data,
      model=form.model.data,
      price=form.price.data,
      status=form.status.data,
    )
    flash(f"Machine {form.name.data} is created successfully.", "success")
    return redirect(url_for('machine.machines'))
  else:
    flash_errors(form)
  return render_template("machines/machine.html", form=form, mode='Create')

@blueprint.route("/<int:machine_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_machine(machine_id):
  """View or edit a machine."""
  machine = Machine.query.get(machine_id)
  if not machine or machine.is_deleted:
    flash("Machine not found.", "danger")
    return redirect(url_for('machine.machines'))
  
  old_status = machine.status  # Save the old status

  if request.method == 'POST':
    current_app.logger.info(request.form)
    form = MachineForm(request.form, obj=machine)
  else:
    form = MachineForm(obj=machine)
  if form.validate_on_submit():
    machine.update( 
      name=form.name.data,
      description=form.description.data,
      type=form.type.data,
      serial=form.serial.data,
      model=form.model.data,
      price=form.price.data,
      status=form.status.data,
    )
    
     # Check if the status has changed from FIXING to HIRING or vice versa
    statuses = [MachineStatusEnum.FIXING.value, MachineStatusEnum.HIRING.value]
     
    if old_status in statuses and form.status.data in statuses and old_status != form.status.data:
      # Get the RentInvoice with ACTIVE status and machine_id
      rent_invoice = RentInvoice.query.filter_by(status=RentInvoiceStatusEnum.ACTIVE.value, machine_id=machine.id).first()
      if rent_invoice:
        # Create a new RentInvoiceHistory with the current RentInvoice id and update the status
        RentInvoiceHistory.create(
          status=form.status.data,
          rent_invoice_id=rent_invoice.id
        )
      
    flash(f"Machine {machine.name} is updated successfully.", "success")
    return redirect(url_for('machine.view_machine', machine_id=machine.id))
  else:
      flash_errors(form)

  return render_template("machines/machine.html", form=form, mode='Edit', machine=machine)

@blueprint.route('/delete_machine/<int:machine_id>', methods=['POST'])
@login_required
def delete_machine(machine_id):
  machine = Machine.query.get(machine_id)
  if machine:
    Machine.delete(machine)
    flash(f"Machine {machine.name} is deleted successfully.", "success")
  else:
    flash("Machine not found.", "danger")
  return jsonify({'redirect_url': url_for('machine.machines')})