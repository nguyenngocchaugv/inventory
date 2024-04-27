# db/seeds.py

from inventory.user.models import User, Role
from inventory.extensions import (
  db,
)
# import other models

def seed():
  db.drop_all()
  db.create_all()
  
   # create a super admin user
  super_admin = User(
    username='superadmin',
    email='superadmin@example.com',
    password='superadmin',
    first_name='Super',
    last_name='Admin',
    active=True,
    is_admin=True
  )
  
  # add super admin user to the session
  db.session.add(super_admin)

  # commit the session to save the user object in the database
  # SQLAlchemy will now have assigned an id to super_admin
  db.session.commit()

  # create a role for super_admin
  # reference the id of super_admin in the user_id field
  super_admin_role = Role(name='super_admin', user_id=super_admin.id)

  # add super admin role to the session
  db.session.add(super_admin_role)

  # commit the session to save the role object in the database
  db.session.commit()

  # similarly, create and save other types of objects