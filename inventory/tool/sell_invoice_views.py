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
from inventory.tool.forms import InvoiceItemForm, SellInvoiceForm, ToolForm
from inventory.tool.models import InvoiceItem, SellInvoice, Tool
from inventory.utils import flash_errors

blueprint = Blueprint("sell_invoices", __name__, url_prefix="/sell-invoices", static_folder="../static")


@blueprint.route("/")
@login_required
def sell_invoices():
  """List sell_invoices."""
  sell_invoices = SellInvoice.query.order_by(desc(SellInvoice.id)).all()
  return render_template("invoices/sell_invoices.html", sell_invoices=sell_invoices)

@blueprint.route('/<int:sell_invoice_id>', methods=['GET'])
@login_required
def view_sell_invoice(sell_invoice_id):
  sell_invoice = SellInvoice.query.get(sell_invoice_id)
  if sell_invoice:
    form = SellInvoiceForm(obj=sell_invoice)
    return render_template('invoices/sell_invoice.html', form=form, mode='View')
  else:
    flash("Sell invoice not found.", "danger")
  return redirect(url_for('sell_invoices.sell_invoices'))


@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_sell_invoice():
  """Create a new sell invoice."""
  form = SellInvoiceForm(request.form)
  
  if form.validate_on_submit():
    # If all InvoiceItemForms are valid, create the sell invoice
    sell_invoice = SellInvoice.create(
      name=form.name.data,
      description=form.description.data,
      issue_date=form.issue_date.data,
      location_id=int(form.location.data)
    )
    # Create an invoice item for each InvoiceItemForm
    for item_form in form.invoice_item_forms:
      tool = Tool.query.get(item_form.tool.data)
      
      InvoiceItem.create(
        tool_name=tool.name,
        tool_type=tool.type,
        tool_model=tool.model,
        quantity=item_form.quantity.data,
        price=tool.price,
        tool_id=int(item_form.tool.data),
        invoice_id=sell_invoice.id
      )
      
      # Reduce the quantity of the tool
      tool.update(quantity=tool.quantity - item_form.quantity.data)

    flash("Sell invoice is created successfully.", "success")
    return redirect(url_for('sell_invoices.sell_invoices'))
  flash_errors(form)
  return render_template("invoices/sell_invoice.html", form=form, mode='Create')

@blueprint.route('/get-invoice-item-form/<int:row_index>', methods=['GET'])
@login_required
def get_invoice_item_form(row_index):
  form = InvoiceItemForm(prefix='invoice_item_forms-' + str(row_index))
  form_html = render_template('invoices/sell_invoice_item_form.html', form=form)
  return jsonify({'form_html': form_html, 'tool_prices': form.tool_prices})

# @blueprint.route("/<int:tool_id>/edit", methods=['GET', 'POST'])
# @login_required
# def edit_tool(tool_id):
#   """View or edit a tool."""
#   tool = Tool.query.get(tool_id)
#   if not tool:
#     flash("Tool not found.", "danger")
#     return redirect(url_for('tool.tools'))

#   if request.method == 'POST':
#     form = ToolForm(request.form)
#   else:
#     form = ToolForm(obj=tool)
    
#   if form.validate_on_submit():
#     tool.update( 
#      name=form.name.data,
#       type=form.type.data,
#       model=form.model.data,
#       price=form.price.data,
#       quantity=form.quantity.data,
#     )
#     flash("Tool is updated successfully.", "success")
#     return redirect(url_for('tool.view_tool', tool_id=tool.id))
#   else:
#       flash_errors(form)

#   return render_template("tools/tool.html", form=form, mode='Edit', tool=tool)

# @blueprint.route('/delete_tool/<int:tool_id>', methods=['POST'])
# @login_required
# def delete_tool(tool_id):
#   tool = Tool.query.get(tool_id)
#   if tool:
#     Tool.delete(tool)
#     flash("Tool is deleted successfully.", "success")
#   else:
#     flash("Tool not found.", "danger")
#   return jsonify({'redirect_url': url_for('tool.tools')})