# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from typing import Optional, Type, TypeVar

from flask_login import current_user
from sqlalchemy import func, event

from .compat import basestring
from .extensions import db

T = TypeVar("T", bound="PkModel")

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
  """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

  @classmethod
  def create(cls, **kwargs):
    """Create a new record and save it the database."""
    instance = cls(**kwargs)
    return instance.save()

  def update(self, commit=True, **kwargs):
    """Update specific fields of a record."""
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    if commit:
      return self.save()
    return self

  def save(self, commit=True):
    """Save the record."""
    db.session.add(self)
    if commit:
      db.session.commit()
    return self

  def delete(self, commit: bool = True) -> None:
    """Remove the record from the database."""
    self.is_deleted = True
    if commit:
      # db.session.delete(self)
      return db.session.commit()
    return


class Model(CRUDMixin, db.Model):
  """Base model class that includes CRUD convenience methods."""

  __abstract__ = True

class PkModel(Model):
  """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

  __abstract__ = True
  id = Column(db.Integer, primary_key=True)
  
  created_date = Column(db.DateTime, nullable=False, default=func.now())
  updated_date = Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
  created_by = db.Column(db.Integer, nullable=True)
  updated_by = db.Column(db.Integer, nullable=True)
  
  is_deleted = Column(db.Boolean, default=False)
  
  @classmethod
  def get_by_id(cls: Type[T], record_id) -> Optional[T]:
    """Get record by ID."""
    if any(
      (
        isinstance(record_id, basestring) and record_id.isdigit(),
        isinstance(record_id, (int, float)),
     )
    ):
      return cls.query.session.get(cls, int(record_id))
    return None
  
  @classmethod
  def __declare_last__(cls):
    event.listen(cls, 'before_insert', cls.on_before_insert)
    event.listen(cls, 'before_update', cls.on_before_update)

  @staticmethod
  def on_before_insert(mapper, connection, target):
    if not target.created_by:
      target.created_by = current_user.id if current_user else None
    target.is_deleted = False

  @staticmethod
  def on_before_update(mapper, connection, target):
    if not target.updated_by:
      target.updated_by = current_user.id if current_user else None


def reference_col(
  tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None
):
  """Column that adds primary key foreign key reference.

  Usage: ::
    category_id = reference_col('category')
    category = relationship('Category', backref='categories')
  """
  foreign_key_kwargs = foreign_key_kwargs or {}
  column_kwargs = column_kwargs or {}

  return Column(
    db.ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
    nullable=nullable,
    **column_kwargs,
  )
