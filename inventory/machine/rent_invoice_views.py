# -*- coding: utf-8 -*-
"""Sell invoice views."""
from flask import (
  Blueprint,
  flash,
  jsonify,
  redirect,
  render_template,
  url_for,
  request
)
from sqlalchemy.orm import joinedload
from flask import current_app
from flask_login import login_required
from sqlalchemy import desc
from inventory.location.models import Location, LocationType
from inventory.machine.forms import MachineStatus, RentInvoiceForm
from inventory.machine.models import Machine, RentInvoice, RentInvoiceHistory
from inventory.utils import flash_errors

blueprint = Blueprint("rent_invoices", __name__, url_prefix="/rent-invoices", static_folder="../static")


@blueprint.route("/")
@login_required
def rent_invoices():
  """List rent_invoices."""
  rent_invoices = RentInvoice.query.order_by(desc(RentInvoice.id)).all()
  return render_template("invoices/rent_invoices.html", rent_invoices=rent_invoices)

@blueprint.route('/<int:rent_invoice_id>', methods=['GET'])
@login_required
def view_rent_invoice(rent_invoice_id):
  rent_invoice = RentInvoice.query.get(rent_invoice_id)
  if rent_invoice:
    form = RentInvoiceForm(obj=rent_invoice)
    return render_template('invoices/rent_invoice.html', form=form, mode='View')
  else:
    flash(f"Rent invoice {rent_invoice_id} not found.", "danger")
  return redirect(url_for('rent_invoices.rent_invoices'))


@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_rent_invoice():
  """Create a new rent invoice."""
  form = RentInvoiceForm(request.form)
  
  current_app.logger.info(form.data)
  if form.validate_on_submit():
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
    machine.update(status=MachineStatus.HIRING.value)
    
    # Create a rent invoice history
    RentInvoiceHistory.create(
      status=form.status.data,
      rent_invoice_id=rent_invoice.id
    )
    
    flash(f"Rent invoice {rent_invoice.name} created successfully.", "success")
    return redirect(url_for('rent_invoices.rent_invoices'))
  flash_errors(form)
  return render_template("invoices/rent_invoice.html", form=form, mode='Create')

# @blueprint.route('/get-invoice-item-form/<int:row_index>', methods=['GET'])
# @login_required
# def get_invoice_item_form(row_index):
#   form = InvoiceItemForm(prefix='invoice_item_forms-' + str(row_index))
#   form_html = render_template('invoices/sell_invoice_item_form.html', form=form)
#   return jsonify({'form_html': form_html, 'tool_prices': form.tool_prices})