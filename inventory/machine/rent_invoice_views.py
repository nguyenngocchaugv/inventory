# -*- coding: utf-8 -*-
"""Sell invoice views."""
from flask import (
  Blueprint,
  flash,
  redirect,
  render_template,
  url_for,
  request
)
from flask_login import login_required
from sqlalchemy import desc
from inventory.machine.forms import RentInvoiceEditForm, RentInvoiceForm
from inventory.machine.models import Machine, MachineStatusEnum, RentInvoice, RentInvoiceHistory, RentInvoiceStatusEnum
from inventory.utils import flash_errors

blueprint = Blueprint("rent_invoices", __name__, url_prefix="/rent-invoices", static_folder="../static")


@blueprint.route("/")
@login_required
def rent_invoices():
  """List rent_invoices."""
  page = request.args.get('page', 1, type=int)
  per_page = 10
  rent_invoices = RentInvoice.query.order_by(desc(RentInvoice.id)).paginate(page=page, per_page=per_page, error_out=False)
  return render_template("invoices/rent_invoices.html", rent_invoices=rent_invoices)

@blueprint.route("/search", methods=["GET"])
def search():
  """Search rent invoices."""
  search_term = request.args.get('q', '')
  page = request.args.get('page', 1, type=int)
  per_page = 10
  if search_term == '':  # Show all rent invoices if no search term
    return redirect(url_for('rent_invoices.rent_invoices', page=page))
  
  rent_invoices = RentInvoice.query.filter(RentInvoice.name.contains(search_term)).order_by(desc(RentInvoice.id)).paginate(page=page, per_page=per_page, error_out=False)
  return render_template("invoices/rent_invoices.html", rent_invoices=rent_invoices, search_term=search_term)

@blueprint.route('/<int:rent_invoice_id>', methods=['GET'])
@login_required
def view_rent_invoice(rent_invoice_id):
  rent_invoice = RentInvoice.query.get(rent_invoice_id)
  if rent_invoice:
    form = RentInvoiceEditForm(obj=rent_invoice)
    return render_template('invoices/rent_invoice.html', form=form, mode='View')
  else:
    flash(f"Rent invoice not found.", "danger")
  return redirect(url_for('rent_invoices.rent_invoices'))


@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_rent_invoice():
  """Create a new rent invoice."""
  form = RentInvoiceForm(request.form)
  
  if form.validate_on_submit():
    # Check machine status
    machine = Machine.query.get(int(form.machine.data))
    if machine.status != MachineStatusEnum.AVAILABLE.value:
      flash(f"Machine {machine.name} is currently not available for hire.", "danger")
      return render_template("invoices/rent_invoice.html", form=form, mode='Create')
    
    rent_invoice = RentInvoice.create(
      name=form.name.data,
      serial=form.serial.data,
      start_date=form.start_date.data,
      end_date=form.end_date.data,
      status=form.status.data,
      price=form.price.data,
      user_id=int(form.user.data),
      machine_id=int(form.machine.data),
      location_id=int(form.location.data)
    )
    
    # Update machine status
    machine = Machine.query.get(int(form.machine.data))
    machine.update(status=MachineStatusEnum.HIRING.value)
    
    # Create a rent invoice history
    RentInvoiceHistory.create(
      status=form.status.data,
      rent_invoice_id=rent_invoice.id
    )
    
    flash(f"Rent invoice {rent_invoice.name} created successfully.", "success")
    return redirect(url_for('rent_invoices.rent_invoices'))
  flash_errors(form)
  return render_template("invoices/rent_invoice.html", form=form, mode='Create')

@blueprint.route("/<int:rent_invoice_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_rent_invoice_status(rent_invoice_id):
  """View or edit a rent invoice status."""
  rent_invoice = RentInvoice.query.get(rent_invoice_id)
  if not rent_invoice:
    flash("Rent Invoice not found.", "danger")
    return redirect(url_for('rent_invoices.rent_invoices'))

  if request.method == 'POST':
    form = RentInvoiceEditForm(request.form, obj=rent_invoice)
  else:
    form = RentInvoiceEditForm(obj=rent_invoice)

  if form.validate_on_submit():
    old_status = rent_invoice.status
    new_status = form.status.data
     # Update the status of the rent invoice
    rent_invoice.update(status=new_status)
    
    # If the status has changed from 'ACTIVE' to either 'CANCELLED' or 'COMPLETED',
    # update the status of the machine to 'AVAILABLE'
    if old_status == RentInvoiceStatusEnum.ACTIVE.value and new_status in [RentInvoiceStatusEnum.CANCELLED.value, RentInvoiceStatusEnum.COMPLETED.value]:
      machine = Machine.query.get(rent_invoice.machine_id)
      if machine:
        machine.update(status=MachineStatusEnum.AVAILABLE.value)
        
    flash(f"Rent invoice {rent_invoice.name} is updated successfully.", "success")
    return redirect(url_for('rent_invoices.view_rent_invoice', rent_invoice_id=rent_invoice.id))
  else:
    flash_errors(form)

  return render_template("invoices/rent_invoice.html", form=form, mode='Edit')
