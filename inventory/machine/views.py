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
from inventory.machine.models import Machine
from inventory.utils import flash_errors

blueprint = Blueprint("machine", __name__, url_prefix="/machines", static_folder="../static")


@blueprint.route("/")
@login_required
def machines():
  """List machines."""
  machines = Machine.query.order_by(desc(Machine.id)).all()
  return render_template("machines/machines.html", machines=machines)

@blueprint.route('/<int:machine_id>', methods=['GET'])
@login_required
def view_machine(machine_id):
  machine = Machine.query.get(machine_id)
  if machine:
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
  current_app.logger.info(form.data)

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
    flash("Machine is created successfully.", "success")
    return redirect(url_for('machine.machines'))
  else:
    flash_errors(form)
  return render_template("machines/machine.html", form=form, mode='Create')

@blueprint.route("/<int:machine_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_machine(machine_id):
  """View or edit a machine."""
  machine = Machine.query.get(machine_id)
  if not machine:
    flash("Machine not found.", "danger")
    return redirect(url_for('machine.machines'))

  if request.method == 'POST':
    form = MachineForm(request.form)
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
    flash("Machine is updated successfully.", "success")
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
    flash("Machine is deleted successfully.", "success")
  else:
    flash("Machine not found.", "danger")
  return jsonify({'redirect_url': url_for('machine.machines')})