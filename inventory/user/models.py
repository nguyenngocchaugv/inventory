# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property

from inventory.database import Column, PkModel, db, relationship, reference_col
from inventory.extensions import bcrypt

class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    
    __table_args__ = (UniqueConstraint('name', 'is_deleted'),) 

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    first_name = Column(db.String(20), nullable=False)
    last_name = Column(db.String(20), nullable=True)
    email = Column(db.String(80), unique=True, nullable=False)
    telephone = Column(db.String(20), nullable=True)
    username = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    street = Column(db.String(20), nullable=True)
    ward = Column(db.String(20), nullable=True)
    district = Column(db.String(20), nullable=True)
    city = Column(db.String(20), nullable=True)
    state = Column(db.String(20), nullable=True)
    zip_code = Column(db.String(20), nullable=True)
    position = Column(db.String(50), nullable=False)
    work_duration = Column(db.Integer, nullable=False)
    status = Column(db.Boolean(), default=True)
    
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )
   
    active = Column(db.Boolean(), default=False)
    
    role_id = reference_col("roles", nullable=False)
    role = relationship("Role", backref="users")
    
    __table_args__ = (
        UniqueConstraint('email', 'is_deleted'),
        UniqueConstraint('username', 'is_deleted'),
    )
    
    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self._password, value)
    
    @classmethod
    def find_by_username(self, username):
        """Find a user by username."""
        return self.query.filter_by(username=username).first()

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"
