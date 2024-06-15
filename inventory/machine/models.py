# -*- coding: utf-8 -*-
"""Machines models."""

from enum import Enum
from inventory.database import Column, PkModel, db, relationship, reference_col

class MachineStatusEnum(Enum):
  AVAILABLE = "AVAILABLE"
  FIXING = "FIXING"
  HIRING = "HIRING"
  
class RentInvoiceStatusEnum(Enum):
  ACTIVE = "ACTIVE"
  COMPLETED = "COMPLETED"
  CANCELLED = "CANCELLED"
  
class RentInvoice(PkModel):
  """A rent invoice of the app."""

  __tablename__ = "rent_invoices"
  
  name = Column(db.String(10), nullable=False)
  serial = Column(db.String(10), nullable=False)
  start_date = Column(db.DateTime, nullable=False)
  end_date = Column(db.DateTime, nullable=False)

  status = Column(db.String(10), nullable=False)
  price = Column(db.Numeric(precision=10, scale=2), nullable=False)
  
  machine_type = Column(db.String(10), nullable=False)
  machine_model = Column(db.String(10), nullable=False)
  
  location_id = reference_col("locations", nullable=False)
  location = relationship("Location", backref="rent_invoices")
  
  machine_id = reference_col("machines", nullable=False)
  machine = relationship("Machine", backref="rent_invoices")
  
  user_id = reference_col("users", nullable=False)
  user = relationship("User", backref="rent_invoices")
  
class RentInvoiceHistory(PkModel):
  """A rent invoice detail of the app."""

  __tablename__ = "rent_invoice_histories"
  
  status = Column(db.String(10), nullable=False)
  
  rent_invoice_id = reference_col("rent_invoices", nullable=False)
  rent_invoice = relationship("RentInvoice", backref="rent_invoice_histories") 
   
class Machine(PkModel):
  """A machine of the app."""

  __tablename__ = "machines"
  
  name = Column(db.String(10), nullable=False)
  description = Column(db.String(100), nullable=True)
  type = Column(db.String(10), nullable=False)
  serial = Column(db.String(10), nullable=False)
  model = Column(db.String(10), nullable=False)
  price = Column(db.Numeric(precision=10, scale=2), nullable=False)
  status = Column(db.String(10), nullable=False)

