# -*- coding: utf-8 -*-
"""Tool models."""

from inventory.database import PkModel, db, reference_col, relationship

class Tool(PkModel):
  """A tool of the app."""

  __tablename__ = "tools"

  name = db.Column(db.String(50), nullable=False)
  type = db.Column(db.String(10), nullable=False)
  model = db.Column(db.String(10), nullable=False)
  price = db.Column(db.Integer, nullable=False)
  quality = db.Column(db.Integer, nullable=False)
  order_details = relationship("OrderDetail", backref="tools")
  locations = relationship("ToolLocation", backref="tools")

class ToolLocation(PkModel):
  """A tool location of the app."""

  __tablename__ = "tool_locations"
  
  quality = db.Column(db.Integer, nullable=False)
  model = db.Column(db.String(10), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  price = db.Column(db.Integer, nullable=False)
  status = db.Column(db.Boolean, nullable=False)
  est_date = db.Column(db.Date, nullable=False)
  

  tool_id = reference_col("tools", nullable=True)
  location_id = reference_col("locations", nullable=True)