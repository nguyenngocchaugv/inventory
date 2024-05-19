# -*- coding: utf-8 -*-
"""Locations models."""

from inventory.database import Column, PkModel, db, relationship, reference_col

class Location(PkModel):
  """A location of the app."""

  __tablename__ = "locations"
  
  name = Column(db.String(50), unique=True, nullable=False)
  street = Column(db.String(20), nullable=False)
  ward = Column(db.String(20), nullable=False)
  district = Column(db.String(20), nullable=False)
  city = Column(db.String(20), nullable=False)
  principal = Column(db.String(20), nullable=False)
  telephone = Column(db.Integer, nullable=False)
  group = Column(db.String(10), nullable=False)
  num_class_total = Column('NumClassTotal', db.Integer, nullable=False)
  num_f1 = Column('NumF1', db.Integer, nullable=False)
  num_f2 = Column('NumF2', db.Integer, nullable=False)
  num_f3 = Column('NumF3', db.Integer, nullable=False)
  num_infant = Column('NumInfant', db.Integer, nullable=False)
  office = Column('Office', db.Integer, nullable=False)
  status = Column('Status', db.Boolean, nullable=False)
  
  location_type_id = reference_col("location_types", nullable=False)  
  location_type = relationship("LocationType", backref="locations")

class LocationType(PkModel):
  """A location type of the app."""

  __tablename__ = "location_types"
  
  name = Column(db.String(50), unique=True, nullable=False)
  
 