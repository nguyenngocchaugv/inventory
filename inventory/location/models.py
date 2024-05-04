# -*- coding: utf-8 -*-
"""Locations models."""

from inventory.database import PkModel, db, relationship, reference_col

class Location(PkModel):
  """A location of the app."""

  __tablename__ = "locations"
  
  name = db.Column(db.String(50), unique=True, nullable=False)  # Unique constraint added here
  street = db.Column(db.String(20), nullable=False)
  ward = db.Column(db.String(20), nullable=False)
  district = db.Column(db.String(20), nullable=False)
  city = db.Column(db.String(20), nullable=False)
  principal = db.Column(db.String(20), nullable=False)
  telephone = db.Column(db.Integer, nullable=False)
  group = db.Column(db.String(10), nullable=False)
  num_class_total = db.Column('NumClassTotal', db.Integer, nullable=False)
  num_f1 = db.Column('NumF1', db.Integer, nullable=False)
  num_f2 = db.Column('NumF2', db.Integer, nullable=False)
  num_f3 = db.Column('NumF3', db.Integer, nullable=False)
  num_infant = db.Column('NumInfant', db.Integer, nullable=False)
  office = db.Column('Office', db.Integer, nullable=False)
  status = db.Column('Status', db.Boolean, nullable=False)
  
  location_type_id = reference_col("location_types", nullable=False)  

class LocationType(PkModel):
  """A location type of the app."""

  __tablename__ = "location_types"
  
  name = db.Column(db.String(50), unique=True, nullable=False)
  
  locations = relationship("Location", backref="location_type")