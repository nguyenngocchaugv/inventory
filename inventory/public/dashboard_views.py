# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user
from sqlalchemy import desc, extract, func

from inventory.extensions import login_manager, db
from inventory.location.models import Location
from inventory.machine.models import Machine, RentInvoice
from inventory.public.forms import LoginForm
from inventory.tool.models import InvoiceItem, SellInvoice, Tool
from inventory.user.forms import RegisterForm
from inventory.user.models import User
from inventory.utils import flash_errors

blueprint = Blueprint("dashboard", __name__, static_folder="../static")


@blueprint.route("/dashboard", methods=["GET", "POST"])
def dashboard():
  """Dashboard page."""
  return render_template("public/dashboard.html")


@blueprint.route("/dashboard/rent-invoice-revenue/<int:year>", methods=["GET"])
def rent_invoice_revenue(year):
  result = db.session.query(
    extract('month', RentInvoice.start_date).label('month'), 
    func.sum(RentInvoice.price).label('total_revenue')
  ).filter(
    extract('year', RentInvoice.start_date) == year
  ).group_by(
    'month'
  ).order_by(
    'month'
  ).all()
  
  # Initialize a list with 12 zeros
  data = [0.0] * 12

  # Update the values for the months that we have data for
  for row in result:
    # Subtract 1 from the month to get the index (months are 1-based, indices are 0-based)
    index = row[0] - 1
    data[index] = float(row[1])

  # The labels are simply the numbers 1 through 12
  labels = list(range(1, 13))
  return jsonify(labels=labels, data=data)

@blueprint.route("/dashboard/top-selling-tools/<int:year>", methods=["GET"])
def top_selling_tools(year):
  result = db.session.query(
    Tool.name, 
    func.sum(InvoiceItem.price * InvoiceItem.quantity).label('total_revenue')
  ).join(
    InvoiceItem, Tool.id == InvoiceItem.tool_id
  ).join(
    SellInvoice, InvoiceItem.invoice_id == SellInvoice.id
  ).filter(
    extract('year', SellInvoice.issue_date) == year
  ).group_by(
    Tool.name
  ).order_by(
    desc('total_revenue')
  ).limit(10).all()
  
  # Convert the result to JSON
  labels = [row[0] for row in result]
  data = [float(row[1]) for row in result]
  return jsonify(labels=labels, data=data)

@blueprint.route("/dashboard/machine-status-count/", methods=["GET"])
def machine_status_count():
  machine_status_counts = db.session.query(
    Machine.status, 
    func.count(Machine.status)
  ).group_by(
      Machine.status
  ).all()
  
   # Convert the result to JSON
  labels = [row[0] for row in machine_status_counts]
  data = [int(row[1]) for row in machine_status_counts]
  return jsonify(labels=labels, data=data)

@blueprint.route("/dashboard/rent-invoice-status-count/", methods=["GET"])
def rent_invoice_status_count():
  rent_invoice_status_counts = db.session.query(
    RentInvoice.status, 
    func.count(RentInvoice.status)
  ).group_by(
      RentInvoice.status
  ).all()
  
   # Convert the result to JSON
  labels = [row[0] for row in rent_invoice_status_counts]
  data = [int(row[1]) for row in rent_invoice_status_counts]
  return jsonify(labels=labels, data=data)

@blueprint.route("/dashboard/top-10-spending-school/", methods=["GET"])
def top_spending_locations():
    # Subquery for tool sales
    tool_sales = db.session.query(
      SellInvoice.location_id,
      func.sum(InvoiceItem.price * InvoiceItem.quantity).label('spend')
    ).join(
      InvoiceItem, SellInvoice.id == InvoiceItem.invoice_id
    ).group_by(
      SellInvoice.location_id
    ).subquery()

    # Subquery for machine rentals
    machine_rentals = db.session.query(
      RentInvoice.location_id,
      func.sum(RentInvoice.price).label('spend')
    ).group_by(
      RentInvoice.location_id
    ).subquery()

    # # Union the subqueries and calculate the total spend for each location
    top_spending_locations = db.session.query(
      Location.name,
      func.sum(tool_sales.c.spend + machine_rentals.c.spend).label('total_spend')
    ).join(
      tool_sales, Location.id == tool_sales.c.location_id
    ).join(
      machine_rentals, Location.id == machine_rentals.c.location_id
    ).group_by(
      Location.name
    ).order_by(
      desc('total_spend')
    ).limit(10).all()

    # Convert the result to JSON
    labels = [row[0] for row in top_spending_locations]
    data = [float(row[1]) for row in top_spending_locations]
    return jsonify(labels=labels, data=data)