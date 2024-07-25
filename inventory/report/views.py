# -*- coding: utf-8 -*-
"""Report views."""
from datetime import datetime
import io
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
import pandas as pd
from sqlalchemy import and_, or_
from inventory.extensions import (
  db,
)
from flask_login import login_required

from inventory.location.models import Location
from inventory.machine.models import Machine, MachineStatusEnum, RentInvoice, RentInvoiceHistory
from inventory.report.forms import MachineAvailabilityForm, RentedMachinesForm, SchoolReportForm, SchoolReportTypeEnum, SoldToolsForm
from inventory.tool.models import InvoiceItem, SellInvoice
from inventory.utils import flash_errors

blueprint = Blueprint("report", __name__, static_folder="../static")

def get_reported_schools(type, location_id, city):
  """Get reported schools based on the type, location_id, and city."""
  invoices = []
  
  query_conditions = []
  
  # Initialize an empty list to hold the final results
  final_invoices = []
  
  if location_id != "All":
    query_conditions.append(Location.name == location_id)
  if city != "All":
    query_conditions.append(Location.city == city)
  
  
  # Check if type is not "All", then filter by the specific type
  if type != "All": 
    if type == SchoolReportTypeEnum.RENT.value:
      query = db.session.query(
              Location.name.label('school_name'),
              RentInvoice.machine_type.label('type'),
              RentInvoice.machine_model.label('model'),
              db.literal(1).label('quantity') # Quantity is always 1 for rent invoices
            ).join(RentInvoice, Location.id == RentInvoice.location_id
            )
            
      if query_conditions:
        query = query.filter(*query_conditions)

      invoices = query.all()
      final_invoices.extend(invoices)
      
    elif type == SchoolReportTypeEnum.SELL.value:
      query = db.session.query(
          Location.name.label('school_name'),
          InvoiceItem.tool_type.label('type'),
          InvoiceItem.tool_model.label('model'),
          InvoiceItem.quantity.label('quantity')
      ).join(SellInvoice, Location.id == SellInvoice.location_id
      ).join(InvoiceItem, SellInvoice.id == InvoiceItem.invoice_id)
      
      if query_conditions:
        query = query.filter(*query_conditions)
      
      invoices = query.all()
      final_invoices.extend(invoices)
  # If type is "All", combine queries for both RENT and SELL types
  else:
    # Query for RENT type
    rent_query = db.session.query(
      Location.name.label('school_name'),
      RentInvoice.machine_type.label('type'),
      RentInvoice.machine_model.label('model'),
      db.literal(1).label('quantity')
    ).join(RentInvoice, Location.id == RentInvoice.location_id)
    
    # Query for SELL type
    sell_query = db.session.query(
      Location.name.label('school_name'),
      InvoiceItem.tool_type.label('type'),
      InvoiceItem.tool_model.label('model'),
      InvoiceItem.quantity.label('quantity')
    ).join(SellInvoice, Location.id == SellInvoice.location_id
          ).join(InvoiceItem, SellInvoice.id == InvoiceItem.invoice_id)
  
     # Apply common conditions to both queries
    if query_conditions:
      rent_query = rent_query.filter(*query_conditions)
      sell_query = sell_query.filter(*query_conditions)
      
    # Execute both queries and combine results
    final_invoices.extend(rent_query.all())
    final_invoices.extend(sell_query.all())
          
  # Convert list of tuples to list of dictionaries
  invoices = [dict(zip(['school_name', 'type', 'model', 'quantity'], invoice)) for invoice in final_invoices]
  
  return invoices

@blueprint.route("/schools", methods=["GET", "POST"])
@login_required
def schools():
  """List reported schools."""
  form = SchoolReportForm()
  invoices = []
  
  type = form.type.data
  location_id = form.location.data
  city = form.city.data
  
  invoices = get_reported_schools(type, location_id, city)
    
  return render_template("reports/schools.html", form=form, invoices=invoices)
  
@blueprint.route('/export_schools', methods=['GET'])
@login_required
def export_schools():
  """Export schools to Excel."""
  
  type = request.args.get('type')
  location_id = request.args.get('location_id')
  city = request.args.get('city')

  invoices = get_reported_schools(type, location_id, city)
    
  # Get the school name from the Location model
  school_name = None
  if (location_id != "All"):
    school_name = Location.query.filter_by(id=location_id).first().name
          
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
    
    sheet_name = 'Reported Schools'
    
    # Write the DataFrame to the Excel file
    df.to_excel(writer, sheet_name=sheet_name, startrow=6)
    
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    
    # Create a format for the cell borders
    border_format = workbook.add_format({'border': 1})

    
    # Apply the cell borders format to the DataFrame area
    worksheet.conditional_format('A7:{}{}'.format(chr(65+len(df.columns)), len(df)+7), {'type': 'no_errors', 'format': border_format})

    # Create a format for the title
    title_format = workbook.add_format({'bold': True, 'font_size': 18})
    
     # Write the title to the Excel file
    title = None
    if type == SchoolReportTypeEnum.RENT.value:
      title = 'Reported Schools for Rent'
    elif type == SchoolReportTypeEnum.SELL.value:
      title = 'Reported Schools for Sell'
    else:
      title = 'Reported Schools'
    
    worksheet.write('A1', title, title_format)
    
    
    # Write the additional information to the Excel file
    worksheet.write('A3', 'Type: ' + type)
    if (school_name):
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
  machines_report = []

  if form.validate_on_submit():
    start_date = form.start_date.data
    end_date = form.end_date.data
    selected_serial = form.serial.data
    selected_model = form.model.data

    # Get the filtered machines for the given date range, serial, and model
    machines_report = get_filtered_machines(start_date, end_date, selected_serial, selected_model)
  else:
    flash_errors(form)
    
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

@blueprint.route("/sold_tools", methods=["GET", "POST"])
@login_required
def sold_tools():
  """List tools sold in the store."""
  form = SoldToolsForm()
  tools_report = []
  
  if form.validate_on_submit():
    start_date = form.start_date.data
    end_date = form.end_date.data
    selected_type = form.type.data
    selected_model = form.model.data
    
    tools_report = get_sold_tools(start_date, end_date, selected_type, selected_model)
  else:
    flash_errors(form)
    
  return render_template("reports/sold_tools.html", form=form, sold_tools=tools_report)

def get_sold_tools(start_date, end_date, selected_type, selected_model):
  """Get sold tools for the given date range, type, and model."""
  base_query = InvoiceItem.query.join(SellInvoice, InvoiceItem.invoice_id == SellInvoice.id)
  
  if selected_type != 'All':
    base_query = base_query.filter(InvoiceItem.tool_type == selected_type)
  if selected_model != 'All':
    base_query = base_query.filter(InvoiceItem.tool_model == selected_model)
    
  tools_report = base_query.filter(
    and_(
      SellInvoice.issue_date >= start_date,
      SellInvoice.issue_date <= end_date
    )
  ).all()
  
  tools_report = [
    {
      "type": tool.tool_type,
      "model": tool.tool_model,
      "quantity": tool.quantity,
      "price": tool.price,
      "sold_date": tool.invoice.issue_date.strftime('%m-%d-%Y')
    }
    for tool in tools_report
  ]
  
  return tools_report

@blueprint.route('/export_sold_tools', methods=['GET'])
@login_required
def export_sold_tools():
  start_date = request.args.get('start_date')
  end_date = request.args.get('end_date')
  type = request.args.get('type')
  model = request.args.get('model')
  
  tools_report = get_sold_tools(start_date, end_date, type, model)
  
  # Convert start_date and end_date from string to datetime objects
  start_date = datetime.strptime(start_date.split(' ')[0], '%Y-%m-%d') if start_date else None
  end_date = datetime.strptime(end_date.split(' ')[0], '%Y-%m-%d') if end_date else None
  
  if not tools_report:
    flash("No data to export.", "danger")
    return redirect(url_for('report.sold_tools'))
  
  df = pd.DataFrame(tools_report)
  
  output = io.BytesIO()
  
  with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    # Rename the DataFrame columns
    df.columns = ['Type', 'Model', 'Quantity', 'Price', 'Sold Date']
    
    df.to_excel(writer, sheet_name='Sold Tools', startrow=7)
    workbook = writer.book
    worksheet = writer.sheets['Sold Tools']
    
     # Create a format for the title
    title_format = workbook.add_format({'bold': True, 'font_size': 18})
    
    # Write the title and details to the Excel file
    worksheet.write('A1', 'Sold Tools Report', title_format)
    worksheet.write('A3', 'Type:')
    worksheet.write('B3', type)
    worksheet.write('D3', 'Model:')
    worksheet.write('E3', model)
    worksheet.write('A5', 'Start Date:')
    worksheet.write('B5', start_date.strftime('%m-%d-%Y'))
    worksheet.write('D5', 'End Date:')
    worksheet.write('E5', end_date.strftime('%m-%d-%Y'))
    
    border_format = workbook.add_format({'border': 1})
    worksheet.conditional_format('A8:F{}'.format(len(df)+8), {'type': 'no_errors', 'format': border_format})
    
  output.seek(0)
    
  return send_file(
    output,
    download_name='sold_tools.xlsx',
    as_attachment=True,
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  )
  
def get_filtered_rent_invoices_with_status_history(start_date, end_date):
  #Query RentInvoice records based on date range
  rent_invoices = db.session.query(RentInvoice).filter(
    and_(
      RentInvoice.start_date >= start_date,
      RentInvoice.start_date <= end_date
    )
  ).all()
  
  # Aggregate RentInvoiceHistory statuses for each RentInvoice
  for invoice in rent_invoices:
    histories = RentInvoiceHistory.query.filter_by(rent_invoice_id=invoice.id).all()

    # Compile a list of unique statuses from the histories
    status_list = list(set([history.status for history in histories]))
    
    # Merge Results - Attach the status list to the invoice object
    setattr(invoice, 'status_history', status_list)

  return rent_invoices

@blueprint.route("/rented_machines", methods=["GET", "POST"])
@login_required
def rented_machines():
  """List rented machines in the store."""
  form = RentedMachinesForm()
  rent_invoices = []
  
  if form.validate_on_submit():
    start_date = form.start_date.data
    end_date = form.end_date.data
    
    rent_invoices = get_filtered_rent_invoices_with_status_history(start_date, end_date)
  else:
    flash_errors(form)
    
  return render_template("reports/rented_machines.html", form=form, rent_invoices=rent_invoices)

@blueprint.route('/export_rented_machines', methods=['GET'])
@login_required
def export_rented_machines():
  start_date = request.args.get('start_date')
  end_date = request.args.get('end_date')
  
  # Convert start_date and end_date from string to datetime objects
  start_date = datetime.strptime(start_date.split(' ')[0], '%Y-%m-%d') if start_date else None
  end_date = datetime.strptime(end_date.split(' ')[0], '%Y-%m-%d') if end_date else None
  
  rent_invoices = get_filtered_rent_invoices_with_status_history(start_date, end_date)
  
  if not rent_invoices:
    flash("No data to export.", "danger")
    return redirect(url_for('report.rent_machines'))
  
  formatted_rent_invoices = [
    {
      "name": invoice.name,
      "serial": invoice.serial,
      "location_name": invoice.location.name,
      "start_date": invoice.start_date.strftime('%m-%d-%Y'),
      "end_date": invoice.end_date.strftime('%m-%d-%Y'),
      "status_history": invoice.status_history
    }
    for invoice in rent_invoices
  ]
  
  df = pd.DataFrame(formatted_rent_invoices)
  
  output = io.BytesIO()
  
  with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    # Rename the DataFrame columns
    df.columns = ['Name', 'Serial', 'Location Name', 'Start Date', 'End Date','Statuses']
    
    # Format the status_history column as a string
    df['Statuses'] = df['Statuses'].apply(lambda x: ', '.join(x))

    
    df.to_excel(writer, sheet_name='Rented Machines', startrow=5)
    workbook = writer.book
    worksheet = writer.sheets['Rented Machines']
    
    title_format = workbook.add_format({'bold': True, 'font_size': 18})
    
    worksheet.write('A1', 'Rented Machines Report', title_format)
    worksheet.write('A3', 'Start Date:')
    worksheet.write('B3', start_date.strftime('%m-%d-%Y'))
    worksheet.write('D3', 'End Date:')
    worksheet.write('E3', end_date.strftime('%m-%d-%Y'))
    
    border_format = workbook.add_format({'border': 1})
    worksheet.conditional_format('A6:G{}'.format(len(df)+6), {'type': 'no_errors', 'format': border_format})
    
  output.seek(0)
    
  return send_file(
    output,
    download_name='rented_machines.xlsx',
    as_attachment=True,
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  )
  