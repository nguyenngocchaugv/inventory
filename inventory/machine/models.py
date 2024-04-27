# -*- coding: utf-8 -*-
"""Machines models."""

from inventory.database import PkModel, db, reference_col, relationship

class MachineHistory(PkModel):
   """A machine history of the app."""

   __tablename__ = "machine_histories"

   type = db.Column(db.String(20), nullable=False)
   location = db.Column(db.String(20), nullable=False)
   estimated_date = db.Column('EstimatedDate', db.Date, nullable=False)
   
   machine_id = reference_col("machines", nullable=True)
   machine = relationship("Machine", backref="histories")
   
   location_id = reference_col("locations", nullable=True)
   location = relationship("Location", backref="histories")
   
   staff_id = reference_col("staffs", nullable=True)
   staff = relationship("Staff", backref="histories")
   

class Machine(PkModel):
  """A machine of the app."""

  __tablename__ = "machines"
  
  type = db.Column(db.String(20), nullable=False)
  serial = db.Column(db.String(20), nullable=False)
  model = db.Column(db.String(20), nullable=False)
  price = db.Column(db.Integer, nullable=False)
  status = db.Column(db.String(20), nullable=False)
  description = db.Column(db.String(100), nullable=False)
  
  location_id = reference_col("locations", nullable=True)
  location = relationship("Location", backref="machines")

