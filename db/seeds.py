# db/seeds.py

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
    is_admin=True
  )
  
  super_admin_role = Role.query.filter_by(name='SuperAdmin').first()
  super_admin_user.roles.append(super_admin_role)
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
    is_admin=True
  )
  admin_role = Role.query.filter_by(name='Admin').first()
  admin_user.roles.append(admin_role)
  db.session.add(admin_user)
  db.session.commit()
