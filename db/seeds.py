# db/seeds.py

from inventory.location.models import LocationType
from inventory.user.models import User, Role
from inventory.extensions import (
  db,
)
# import other models

def seed():
  db.drop_all()
  db.create_all()
  
  # Create roles
  roles = ['SuperAdmin', 'Admin', 'User']
  
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
    active=True,
    position='Super Admin',
    work_duration=8
  )
  
  super_admin_role = Role.query.filter_by(name='SuperAdmin').first()
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
    active=True,
    position='Admin',
    work_duration=8
  )
  admin_role = Role.query.filter_by(name='Admin').first()
  admin_user.role = admin_role
  db.session.add(admin_user)
  db.session.commit()
  
  # Location Types
  location_types = ['School', 'Warehouse', 'Supplier']
  
  for location_type_name in location_types:
    location_type = LocationType(name=location_type_name)
    db.session.add(location_type)
  db.session.commit()
