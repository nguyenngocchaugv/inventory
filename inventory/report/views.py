# -*- coding: utf-8 -*-
"""Report views."""
import io
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
import pandas as pd
from sqlalchemy import and_, or_
from inventory.extensions import (
  db,
)
from flask_login import login_required

from inventory.location.models import Location
from inventory.machine.models import Machine, MachineStatusEnum, RentInvoice
from inventory.report.forms import MachineAvailabilityForm, SchoolReportForm, SchoolReportTypeEnum
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

def get_filtered_machines(start_date, end_date, selected_serial, selected_model):
  """Get filtered machines for the given date range, serial, and model."""
  # Base query for AVAILABLE machines
  base_query = Machine.query.filter(Machine.status == MachineStatusEnum.AVAILABLE.value)
  
  # Apply filters for selected serial and model if they are not 'All'
  if selected_serial != 'All':
    base_query = base_query.filter(Machine.serial == selected_serial)
  if selected_model != 'All':
    base_query = base_query.filter(Machine.model == selected_model)
    
  # Query for HIRING machines with future start dates
  hiring_machines_query = Machine.query.join(RentInvoice, Machine.id == RentInvoice.machine_id).filter(
    and_(
      Machine.status == MachineStatusEnum.HIRING.value,
      or_(
        RentInvoice.start_date > end_date,  # Case 1: Future start date
        RentInvoice.end_date < start_date   # Case 2: Ends before start date
      )
    )
  )
  
  # Apply the same filters for serial and model to the hiring machines query if not 'All'
  if selected_serial != 'All':
    hiring_machines_query = hiring_machines_query.filter(Machine.serial == selected_serial)
  if selected_model != 'All':
    hiring_machines_query = hiring_machines_query.filter(Machine.model == selected_model)
  
  # Combine queries
  available_machines = base_query.union(hiring_machines_query).all()
  
  # Convert the list of machines to a list of dictionaries
  machines_report = [
    {"serial": machine.serial, "model": machine.model, "status": machine.status, "description": machine.description}
    for machine in available_machines
  ]
  
  return machines_report

@blueprint.route("/machine_availability", methods=["GET", "POST"])
@login_required
def machine_availability():
  """List available machines in the store for a specific date range."""
  form = MachineAvailabilityForm()  # This form should have start_date and end_date fields
  available_machines = []
  machines_report = []

  if form.validate_on_submit():
    start_date = form.start_date.data
    end_date = form.end_date.data
    selected_serial = form.serial.data
    selected_model = form.model.data

    # Get the filtered machines for the given date range, serial, and model
    machines_report = get_filtered_machines(start_date, end_date, selected_serial, selected_model)
    
  else:
    flash("Please enter valid dates.", "danger")
  return render_template("reports/machine_availability.html", form=form, machines=machines_report)

@blueprint.route('/export_machine_availability', methods=['GET'])
@login_required
def export_machine_availability():
  """Export filtered machines to Excel."""
  
  serial = request.args.get('serial')
  model = request.args.get('model')
  start_date = request.args.get('start_date')
  end_date = request.args.get('end_date')
  
  # Get the filtered machines for the given date range, serial, and model
  machines_report = get_filtered_machines(start_date, end_date, serial, model)
  
  if not machines_report:
    flash("No data to export.", "danger")
    return redirect(url_for('report.machine_availability'))
  
  # Convert the list of dictionaries to a pandas DataFrame
  df = pd.DataFrame(machines_report)
  
  # Create an in-memory BytesIO object
  output = io.BytesIO()
  
  # Write the DataFrame to the BytesIO object using ExcelWriter
  with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    # Rename the DataFrame columns
    df.columns = ['Serial', 'Model', 'Status', 'Description']
    
    # Write the DataFrame to the Excel file
    df.to_excel(writer, sheet_name='Available Machines In Store', startrow=7)
    
    workbook = writer.book
    worksheet = writer.sheets['Available Machines In Store']
    
    # Create a format for the cell borders
    border_format = workbook.add_format({'border': 1})
    
    # Apply the cell borders format to the DataFrame area
    worksheet.conditional_format('A8:{}{}'.format(chr(65+len(df.columns)), len(df)+8), {'type': 'no_errors', 'format': border_format})
    
    # Create a format for the title
    title_format = workbook.add_format({'bold': True, 'font_size': 18})
    
    # Write the title and details to the Excel file
    worksheet.write('A1', 'Available Machines Report', title_format)
    worksheet.write('A3', 'Serial:')
    worksheet.write('B3', serial)
    worksheet.write('D3', 'Model:')
    worksheet.write('E3', model)
    worksheet.write('A5', 'Start Date:')
    worksheet.write('B5', start_date)
    worksheet.write('D5', 'End Date:')
    worksheet.write('E5', end_date)
 
  # Reset the pointer of the BytesIO object to the beginning
  output.seek(0)
  
  # Create a Flask response with the Excel file
  return send_file(output, download_name='available-machine.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')