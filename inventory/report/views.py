# -*- coding: utf-8 -*-
"""Report views."""
import io
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
import pandas as pd
from inventory.extensions import (
  db,
)
from flask_login import login_required

from inventory.location.models import Location
from inventory.machine.models import RentInvoice
from inventory.report.forms import SchoolReportForm, SchoolReportTypeEnum
from inventory.tool.models import InvoiceItem, SellInvoice

blueprint = Blueprint("report", __name__, static_folder="../static")

@blueprint.route("/schools", methods=["GET", "POST"])
@login_required
def schools():
  """List reported schools."""
  form = SchoolReportForm()
  invoices = []
  
  type = form.type.data
  location_id = form.location.data
  city = form.city.data
  
  if type == SchoolReportTypeEnum.RENT.value:
    invoices = db.session.query(
            Location.name.label('school_name'),
            RentInvoice.machine_type.label('type'),
            RentInvoice.machine_model.label('model'),
            db.literal(1).label('quantity') # Quantity is always 1 for rent invoices
          ).join(RentInvoice, Location.id == RentInvoice.location_id
          ).filter(
              RentInvoice.location_id == location_id,
              Location.city == city,
          ).all()
  if type == SchoolReportTypeEnum.SELL.value:
    invoices = db.session.query(
        Location.name.label('school_name'),
        InvoiceItem.tool_type.label('type'),
        InvoiceItem.tool_model.label('model'),
        InvoiceItem.quantity.label('quantity')
    ).join(SellInvoice, Location.id == SellInvoice.location_id
    ).join(InvoiceItem, SellInvoice.id == InvoiceItem.invoice_id
    ).filter(
        SellInvoice.location_id == location_id,
        Location.city == city,
    ).all()
          
  # Convert list of tuples to list of dictionaries
  invoices = [dict(zip(['school_name', 'type', 'model', 'quantity'], invoice)) for invoice in invoices]
    
  return render_template("reports/schools.html", form=form, invoices=invoices)
  
@blueprint.route('/export_schools', methods=['GET'])
@login_required
def export_schools():
  """Export schools to Excel."""
  
  type = request.args.get('type')
  location_id = request.args.get('location_id')
  city = request.args.get('city')

  invoices = []
  
  if type == SchoolReportTypeEnum.RENT.value:
    invoices = db.session.query(
            Location.name.label('school_name'),
            RentInvoice.machine_type.label('type'),
            RentInvoice.machine_model.label('model'),
            db.literal(1).label('quantity') # Quantity is always 1 for rent invoices
          ).join(RentInvoice, Location.id == RentInvoice.location_id
          ).filter(
              RentInvoice.location_id == location_id,
              Location.city == city,
          ).all()
  if type == SchoolReportTypeEnum.SELL.value:
    invoices = db.session.query(
        Location.name.label('school_name'),
        InvoiceItem.tool_type.label('type'),
        InvoiceItem.tool_model.label('model'),
        InvoiceItem.quantity.label('quantity')
    ).join(SellInvoice, Location.id == SellInvoice.location_id
    ).join(InvoiceItem, SellInvoice.id == InvoiceItem.invoice_id
    ).filter(
        SellInvoice.location_id == location_id,
        Location.city == city,
    ).all()
    
  # Get the school name from the Location model
  school_name = Location.query.filter_by(id=location_id).first().name
          
  # Convert list of tuples to list of dictionaries
  invoices = [dict(zip(['school_name', 'type', 'model', 'quantity'], invoice)) for invoice in invoices]

  # Convert the invoices data to a pandas DataFrame
  df = pd.DataFrame(invoices)
  
  if df.empty:
    flash("No data to export.", "danger")
    return redirect(url_for('report.schools'))
  
  # Create an in-memory BytesIO object
  output = io.BytesIO()
  # Write the DataFrame to the BytesIO object
  with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    # Rename the DataFrame columns
    df.columns = ['School Name', 'Type', 'Model', 'Quantity']
    
    # Write the DataFrame to the Excel file
    df.to_excel(writer, sheet_name='Sheet1', startrow=6)
    
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    
    # Create a format for the cell borders
    border_format = workbook.add_format({'border': 1})

    
    # Apply the cell borders format to the DataFrame area
    worksheet.conditional_format('A7:{}{}'.format(chr(65+len(df.columns)), len(df)+7), {'type': 'no_errors', 'format': border_format})

    # Create a format for the title
    title_format = workbook.add_format({'bold': True, 'font_size': 18})
    
     # Write the title to the Excel file
    title = 'Summary of Machines' if type == SchoolReportTypeEnum.RENT.value else 'Summary of Tools'
    worksheet.write('A1', title, title_format)
    
    
    # Write the additional information to the Excel file
    worksheet.write('A3', 'Type: ' + type)
    worksheet.write('A4', 'School Name: ' + school_name)
    worksheet.write('A5', 'City: ' + city)

  # Create a Flask response with the Excel file
  output.seek(0)
  return send_file(output, download_name='schools.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')