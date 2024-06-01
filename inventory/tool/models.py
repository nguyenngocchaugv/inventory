# -*- coding: utf-8 -*-
"""Tool models."""
from sqlalchemy import UniqueConstraint, func

from inventory.database import Column, PkModel, db, reference_col, relationship

class Tool(PkModel):
  """A tool of the app."""

  __tablename__ = "tools"

  name = Column(db.String(20), nullable=False)
  type = Column(db.String(10), nullable=False)
  model = Column(db.String(20), nullable=False)
  price = Column(db.Numeric(precision=10, scale=2), nullable=False)
  quantity = Column(db.Integer, nullable=False)

class SellInvoice(PkModel):
  """A sell invoice of the app."""

  __tablename__ = "sell_invoices"

  name = Column(db.String(20), nullable=False)
  description = Column(db.String(50), nullable=False)
  issue_date = Column(db.DateTime, nullable=False)

  location_id = reference_col("locations", nullable=False)
  location = relationship("Location", backref="sell_invoices")
  
  __table_args__ = (UniqueConstraint('name', 'is_deleted'),)  
  
  @property
  def total_price(self):
    return db.session.query(func.sum(InvoiceItem.price * InvoiceItem.quantity)).filter(InvoiceItem.invoice_id == self.id).scalar() or 0
  
class InvoiceItem(PkModel):
  """An item in an invoice."""

  __tablename__ = "invoice_items"

  tool_name = Column(db.String(20), nullable=False)
  tool_type = Column(db.String(10), nullable=False)
  tool_model = Column(db.String(20), nullable=False)
  quantity = Column(db.Integer, nullable=False)
  price = Column(db.Numeric(precision=10, scale=2), nullable=False)

  tool_id = reference_col("tools", nullable=False)
  tool = relationship("Tool", backref="invoice_items")
  
  invoice_id = reference_col("sell_invoices", nullable=False)
  invoice = relationship("SellInvoice", backref="invoice_items")