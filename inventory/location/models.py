# -*- coding: utf-8 -*-
"""Locations models."""

from enum import Enum
from sqlalchemy import UniqueConstraint
from inventory.database import Column, PkModel, db, relationship, reference_col

class LocationTypeEnum(Enum):
  SCHOOL = 'School'
  WAREHOUSE = 'Warehouse'
  SUPPLIER = 'Supplier'
  
class Location(PkModel):
  """A location of the app."""

  __tablename__ = "locations"
  
  name = Column(db.String(50), nullable=False)
  street = Column(db.String(20), nullable=False)
  ward = Column(db.String(20), nullable=False)
  district = Column(db.String(20), nullable=False)
  city = Column(db.String(20), nullable=False)
  principal = Column(db.String(20), nullable=False)
  telephone = Column(db.Integer, nullable=False)
  group = Column(db.String(10), nullable=False)
  num_class_total = Column(db.Integer, nullable=False)
  num_f1 = Column(db.Integer, nullable=False)
  num_f2 = Column(db.Integer, nullable=False)
  num_f3 = Column(db.Integer, nullable=False)
  num_infant = Column(db.Integer, nullable=False)
  office = Column(db.Integer, nullable=False)
  is_active = Column(db.Boolean, nullable=False)
  
  location_type_id = reference_col("location_types", nullable=False)  
  location_type = relationship("LocationType", backref="locations")
  
  __table_args__ = (UniqueConstraint('name', 'is_deleted'),) 

class LocationType(PkModel):
  """A location type of the app."""

  __tablename__ = "location_types"
  
  name = Column(db.String(50), unique=True, nullable=False)
  
  __table_args__ = (UniqueConstraint('name', 'is_deleted'),) 
  
 