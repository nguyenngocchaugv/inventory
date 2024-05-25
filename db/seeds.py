# db/seeds.py

from enum import Enum
from inventory.location.models import LocationType
from inventory.user.models import User, Role
from inventory.extensions import (
  db,
)
# import other models

class RoleEnum(Enum):
  SUPER_ADMIN = 'SuperAdmin'
  ADMIN = 'Admin'
  USER = 'User'
  
class LocationTypeEnum(Enum):
  SCHOOL = 'School'
  WAREHOUSE = 'Warehouse'
  SUPPLIER = 'Supplier'

def seed():
  db.drop_all()
  db.create_all()
  
  # Create roles
  roles = [role.value for role in RoleEnum]
  
  for role_name in roles:
    role = Role(name=role_name)
    db.session.add(role)
  db.session.commit()
  
  
   # create a super admin user
  super_admin_user = User(
    username='superadmin',
    email='superadmin@example.com',
    password='superadmin',
    first_name='Super',
    last_name='Admin',
    is_active=True,
    position='Super Admin',
    work_duration=8,
    created_by=1,
    updated_by=1
  )
  
  super_admin_role = Role.query.filter_by(name=RoleEnum.SUPER_ADMIN.value).first()
  super_admin_user.role = super_admin_role
  
  db.session.add(super_admin_user)
  db.session.commit()
  
  # Create an Admin user
  admin_user = User(
    username='admin',
    email='admin@example.com',
    password='admin',
    first_name='Admin',
    last_name='User',
    is_active=True,
    position='Admin',
    work_duration=8,
    created_by=1,
    updated_by=1
  )
  admin_role = Role.query.filter_by(name=RoleEnum.ADMIN.value).first()
  admin_user.role = admin_role
  db.session.add(admin_user)
  db.session.commit()
  
  # Location Types
  location_types = [location_type.value for location_type in LocationTypeEnum]
  
  for location_type_name in location_types:
    location_type = LocationType(
      name=location_type_name,
      created_by=1,
      updated_by=1
    )
    db.session.add(location_type)
  db.session.commit()
