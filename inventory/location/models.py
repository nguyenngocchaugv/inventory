# -*- coding: utf-8 -*-
"""Locations models."""
import datetime as dt

from flask_login import UserMixin

from inventory.database import Column, PkModel, db, reference_col, relationship

class Location(UserMixin, PkModel):
    """A location of the app."""

    __tablename__ = "locations"
    address = Column(db.String(80), unique=False, nullable=False)

