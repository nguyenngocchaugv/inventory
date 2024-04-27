# -*- coding: utf-8 -*-
"""Purchase order models."""

from inventory.database import PkModel, db, reference_col, relationship

class PurchaseOrder(PkModel):
  """A machine history of the app."""

  __tablename__ = 'purchase_orders'
  
  order_date = db.Column(db.Date, nullable=False)

  location_id = reference_col("locations", nullable=True)
  
  location = relationship('Location', backref='orders')
  order_details = relationship('OrderDetail', backref='purchase_order')
  

class OrderDetail(PkModel):
  """A order detail of the app."""
  
  __tablename__ = 'order_details'
  id = db.Column(db.Integer, primary_key=True)
  
  purchase_order_id = reference_col("purchase_orders", nullable=True)
  tool_id = reference_col("tools", nullable=True)
