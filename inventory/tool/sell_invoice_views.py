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
  # tool = Tool.query.get(sell_invoice_id)
  # if tool:
  #   form = ToolForm(obj=tool)
  #   return render_template('tools/tool.html', tool=tool, form=form, mode='View')
  # else:
  #   flash("Tool not found.", "danger")
    return redirect(url_for('sell_invoices.sell_invoices'))

@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_sell_invoice():
  """Create a new sell invoice."""
  form = SellInvoiceForm(request.form)
  
   # Get the list of locations from the database that are of type 'School'
  # locations = [(str(location.id), location.name) for location in Location.query.join(Location.location_type).filter(LocationType.name=='School').all()]
  # Add a placeholder option with a "-1" value
  # locations.insert(0, (-1, 'Select a school...'))
  # form.location.choices = locations
  current_app.logger.info(form.data)
  if form.validate_on_submit():
    if form.location.data == -1:
      flash('Please select a school', 'error')
    else:
      # Validate each InvoiceItemForm
      for item_form in form.invoice_item_forms:
        if not item_form.validate():
          # If an InvoiceItemForm is not valid, return an error response
          return jsonify(success=False, errors=item_form.errors)
        
      # If all InvoiceItemForms are valid, create the sell invoice
      sell_invoice = SellInvoice.create(
        name=form.name.data,
        description=form.description.data,
        issue_date=form.issue_date.data,
        price=form.price.data,
        quantity=form.quantity.data,
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
          price=item_form.price.data,
          tool_id=int(item_form.tool.data),
          invoice_id=sell_invoice.id
        )

      flash("Sell invoice is created successfully.", "success")
      return redirect(url_for('sell_invoices.sell_invoices'))
  # else:
  #   # If the form did not validate, manually repopulate the nested form fields
  #   for i in range(len(request.form.getlist('invoice_item_forms-tool'))):
  #     item_form = InvoiceItemForm()
  #     item_form.tool.data = request.form.getlist('invoice_item_forms-tool')[i]
  #     item_form.quantity.data = request.form.getlist('invoice_item_forms-quantity')[i]
  #     item_form.price.data = request.form.getlist('invoice_item_forms-price')[i]
  #     form.invoice_item_forms.append_entry(item_form)
    flash_errors(form)
  return render_template("invoices/sell_invoice.html", form=form, mode='Create')

@blueprint.route('/get-invoice-item-form', methods=['GET'])
@login_required
def get_invoice_item_form():
  # Get the list of tools from the database
  # tools = [(tool.id, tool.name) for tool in Tool.query.order_by(Tool.name).all()]
  
    
  # Add a placeholder option with an empty value
  # tools.insert(0, ('', 'Select a tool...'))
  
  form = InvoiceItemForm()
  # form.tool.choices = tools  # Populate the tool dropdown
  return render_template('invoices/sell_invoice_item_form.html', form=form)

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