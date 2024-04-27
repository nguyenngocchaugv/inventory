# -*- coding: utf-8 -*-
"""Staff models."""

from inventory.database import PkModel, db, reference_col, relationship

class Staff(PkModel):
  """A staff member of the app."""
  
  __tablename__ = "staffs"
  
  status = db.Column(db.Boolean, nullable=False)
  telephone = db.Column(db.Integer, nullable=False)
  
  user_id = reference_col("users", nullable=True)
  user = relationship("User", backref="staff")