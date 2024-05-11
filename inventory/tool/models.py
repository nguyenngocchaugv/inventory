# -*- coding: utf-8 -*-
"""Tool models."""
import datetime as dt

from inventory.database import PkModel, db, reference_col, relationship

class Tool(PkModel):
  """A tool of the app."""

  __tablename__ = "tools"

  name = db.Column(db.String(20), nullable=False)
  type = db.Column(db.String(10), nullable=False)
  model = db.Column(db.String(20), nullable=False)
  price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  quantity = db.Column(db.Integer, nullable=False)

class SellInvoice(PkModel):
  """A sell invoice of the app."""

  __tablename__ = "sell_invoices"

  name = db.Column(db.String(20), nullable=False)
  type = db.Column(db.String(10), nullable=False)
  model = db.Column(db.String(20), nullable=False)
  price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  
  est_date = db.Column(db.DateTime, nullable=False)
  created_date = db.Column(db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc))
  status = db.Column(db.String(10), nullable=False)

  tool_id = reference_col("tools", nullable=False)
  tool = relationship("Tool", backref="sell_invoices")

  location_id = reference_col("locations", nullable=False)
  location = relationship("Location", backref="sell_invoices")