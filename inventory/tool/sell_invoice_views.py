# -*- coding: utf-8 -*-
"""Sell invoice views."""
import io
from flask import (
  Blueprint,
  flash,
  jsonify,
  redirect,
  render_template,
  send_file,
  url_for,
  request
)
from flask_login import login_required
import pandas as pd
from sqlalchemy.orm import joinedload
from sqlalchemy import desc

from inventory.tool.forms import InvoiceItemForm, SellInvoiceForm
from inventory.tool.models import InvoiceItem, SellInvoice, Tool
from inventory.utils import flash_errors

blueprint = Blueprint("sell_invoices", __name__, url_prefix="/sell-invoices", static_folder="../static")


@blueprint.route("/")
@login_required
def sell_invoices():
  """List sell_invoices."""
  page = request.args.get('page', 1, type=int)
  per_page = 10
  sell_invoices = SellInvoice.query.order_by(desc(SellInvoice.id)).paginate(page=page, per_page=per_page, error_out=False)
  return render_template("invoices/sell_invoices.html", sell_invoices=sell_invoices)

@blueprint.route("/search", methods=["GET"])
def search():
  """Search sell invoices."""
  search_term = request.args.get('q', '')
  page = request.args.get('page', 1, type=int)
  per_page = 10
  if search_term == '':  # Show all sell invoices if no search term
    return redirect(url_for('sell_invoices.sell_invoices', page=page))
  
  sell_invoices = SellInvoice.query.filter(SellInvoice.name.contains(search_term)).order_by(desc(SellInvoice.id)).paginate(page=page, per_page=per_page, error_out=False)
  return render_template("invoices/sell_invoices.html", sell_invoices=sell_invoices, search_term=search_term)

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

@blueprint.route('/export', methods=['GET'])
@login_required
def export_sell_invoices():
  """Export sell invoices to Excel."""
  # Query all invoices and their items
  invoices = SellInvoice.query.order_by(desc(SellInvoice.id)).options(joinedload(SellInvoice.invoice_items)).all()
 # Convert the invoices to a DataFrame
  invoices_df = pd.DataFrame([{
    'name': invoice.name,
    'description': invoice.description,
    'issue_date': invoice.issue_date,
    'location_id': invoice.location_id,
    'total_price': invoice.total_price,
  } for invoice in invoices])
  
  # Convert the invoice items to a DataFrame
  items_df = pd.DataFrame([{
    'invoice_name': item.invoice.name,
    'tool_name': item.tool_name,
    'tool_type': item.tool_type,
    'tool_model': item.tool_model,
    'quantity': item.quantity,
    'price': item.price,
  } for invoice in invoices for item in invoice.invoice_items])
  
  # Create an in-memory BytesIO object
  output = io.BytesIO()
    
  # Write the DataFrames to the BytesIO object
  with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    invoices_df.to_excel(writer, sheet_name='Invoices', index=False)
    items_df.to_excel(writer, sheet_name='Invoice Items', index=False)


  # Create a Flask response with the Excel file
  output.seek(0)
  return send_file(output, download_name='sell_invoices.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')