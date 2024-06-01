# db/seeds.py

from datetime import datetime
import random
import string
from inventory.location.models import Location, LocationType, LocationTypeEnum
from inventory.machine.models import Machine, MachineStatusEnum, RentInvoice, RentInvoiceHistory, RentInvoiceStatusEnum
from inventory.tool.models import InvoiceItem, SellInvoice, Tool
from inventory.user.models import RoleEnum, User, Role
from inventory.extensions import (
  db,
)

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
    telephone=''.join(random.choices(string.digits, k=10)),  # Generate a random 10-digit telephone number
    last_name='Admin',
    street='Oak Street',
    ward='Ward 1',
    district='District 1',
    city='City 1',
    state='State 1',
    zip_code='12345',
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
  admin_users = [
    {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin', 'first_name': 'Admin', 'last_name': 'User', 'position': 'Admin', 'work_duration': 8, 'is_active': True, 'created_by': 1, 'updated_by': 1,'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'state': 'State 1', 'zip_code': '12345'},
    {'username': 'admin1', 'email': 'admin1@example.com', 'password': 'admin1', 'first_name': 'Admin1', 'last_name': 'User1', 'position': 'Admin', 'work_duration': 8, 'is_active': True, 'created_by': 1, 'updated_by': 1, 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'state': 'State 1', 'zip_code': '12345'},
    {'username': 'admin2', 'email': 'admin2@example.com', 'password': 'admin2', 'first_name': 'Admin2', 'last_name': 'User2', 'position': 'Admin', 'work_duration': 8, 'is_active': True, 'created_by': 1, 'updated_by': 1, 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'state': 'State 1', 'zip_code': '12345'},
  ]
  
  for admin_user in admin_users:
    user = User(
      username=admin_user['username'],
      email=admin_user['email'],
      password=admin_user['password'],
      telephone=''.join(random.choices(string.digits, k=10)),  # Generate a random 10-digit telephone number
      first_name=admin_user['first_name'],
      last_name=admin_user['last_name'],
      is_active=admin_user['is_active'],
      street=admin_user['street'],
      ward=admin_user['ward'],
      district=admin_user['district'],
      city=admin_user['city'],
      state=admin_user['state'],
      zip_code=admin_user['zip_code'],
      position=admin_user['position'],
      work_duration=admin_user['work_duration'],
      created_by=1,
      updated_by=1
    )
    admin_role = Role.query.filter_by(name=RoleEnum.ADMIN.value).first()
    user.role = admin_role
    db.session.add(user)
  db.session.commit()
  
  # Create users
  users = [
    {'username': 'johndoe', 'email': 'johndoe@example.com', 'password': 'password', 'first_name': 'John', 'last_name': 'Doe', 'position': 'Staff', 'work_duration': 40, 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'state': 'State 1', 'zip_code': '12345'},
    {'username': 'janedoe', 'email': 'janedoe@example.com', 'password': 'password', 'first_name': 'Jane', 'last_name': 'Doe', 'position': 'Staff', 'work_duration': 40, 'street': 'Pine Street', 'ward': 'Ward 2', 'district': 'District 2', 'city': 'City 2', 'state': 'State 2', 'zip_code': '12345'},
    {'username': 'mikejohnson', 'email': 'mikejohnson@example.com', 'password': 'password', 'first_name': 'Mike', 'last_name': 'Johnson', 'position': 'Staff', 'work_duration': 40, 'street': 'Maple Street', 'ward': 'Ward 3', 'district': 'District 3', 'city': 'City 3', 'state': 'State 3', 'zip_code': '12345'},
    {'username': 'sarahsmith', 'email': 'sarahsmith@example.com', 'password': 'password', 'first_name': 'Sarah', 'last_name': 'Smith', 'position': 'Staff', 'work_duration': 40, 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'state': 'State 1', 'zip_code': '12345'},
    {'username': 'jamesbrown', 'email': 'jamesbrown@example.com', 'password': 'password', 'first_name': 'James', 'last_name': 'Brown', 'position': 'Staff', 'work_duration': 40, 'street': 'Pine Street', 'ward': 'Ward 2', 'district': 'District 2', 'city': 'City 2', 'state': 'State 2', 'zip_code': '12345'},
    {'username': 'emilyjones', 'email': 'emilyjones@example.com', 'password': 'password', 'first_name': 'Emily', 'last_name': 'Jones', 'position': 'Staff', 'work_duration': 40, 'street': 'Maple Street', 'ward': 'Ward 3', 'district': 'District 3', 'city': 'City 3', 'state': 'State 3', 'zip_code': '12345'},
    {'username': 'davidwilliams', 'email': 'davidwilliams@example.com', 'password': 'password', 'first_name': 'David', 'last_name': 'Williams', 'position': 'Staff', 'work_duration': 40, 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'state': 'State 1', 'zip_code': '12345'},
    {'username': 'olivertaylor', 'email': 'olivertaylor@example.com', 'password': 'password', 'first_name': 'Oliver', 'last_name': 'Taylor', 'position': 'Staff', 'work_duration': 40, 'street': 'Pine Street', 'ward': 'Ward 2', 'district': 'District 2', 'city': 'City 2', 'state': 'State 2', 'zip_code': '12345'},
    {'username': 'sophiawilson', 'email': 'sophiawilson@example.com', 'password': 'password', 'first_name': 'Sophia', 'last_name': 'Wilson', 'position': 'Staff', 'work_duration': 40, 'street': 'Maple Street', 'ward': 'Ward 3', 'district': 'District 3', 'city': 'City 3', 'state': 'State 3', 'zip_code': '12345'},
    {'username': 'williammartin', 'email': 'williammart@example.com', 'password': 'password', 'first_name': 'William', 'last_name': 'Martin', 'position': 'Staff', 'work_duration': 40, 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'state': 'State 1', 'zip_code': '12345'},
    {'username': 'danieldavis', 'email': 'danieldavis@example.com', 'password': 'password', 'first_name': 'Daniel', 'last_name': 'Davis', 'position': 'Staff', 'work_duration': 40, 'street': 'Pine Street', 'ward': 'Ward 2', 'district': 'District 2', 'city': 'City 2', 'state': 'State 2', 'zip_code': '12345'},
    # Add more users...
  ]
  
  for user in users:
    user = User(
      first_name=user['first_name'],
      last_name=user['last_name'],
      email=user['email'],
      telephone=''.join(random.choices(string.digits, k=10)),  # Generate a random 10-digit telephone number
      username=user['username'],
      password=user['password'],
      street=user['street'],
      ward=user['ward'],
      district=user['district'],
      city=user['city'],
      state=user['state'],
      zip_code=user['zip_code'],
      is_active=True,
      position=user['position'],
      work_duration=user['work_duration'],
      created_by=1,
      updated_by=1
    )
    user_role = Role.query.filter_by(name=RoleEnum.USER.value).first()
    user.role = user_role
    db.session.add(user)
  
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
  
  # Create school locations
  school_locations = [
    {'name': 'Greenfield Primary School', 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'principal': 'John Doe', 'telephone': 1234567890, 'group': 'Group 1', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    {'name': 'Greenfield Secondary School', 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'principal': 'Jane Doe', 'telephone': 1234567890, 'group': 'Group 1', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    {'name': 'Greenfield High School', 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'principal': 'Mike Johnson', 'telephone': 1234567890, 'group': 'Group 1', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    {'name': 'Greenfield University', 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'principal': 'Sarah Smith', 'telephone': 1234567890, 'group': 'Group 1', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    {'name': 'Bluefield Primary School', 'street': 'Pine Street', 'ward': 'Ward 2', 'district': 'District 2', 'city': 'City 2', 'principal': 'James Brown', 'telephone': 1234567890, 'group': 'Group 2', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    {'name': 'Bluefield Secondary School', 'street': 'Pine Street', 'ward': 'Ward 2', 'district': 'District 2', 'city': 'City 2', 'principal': 'Emily Jones', 'telephone': 1234567890, 'group': 'Group 2', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    {'name': 'Bluefield High School', 'street': 'Pine Street', 'ward': 'Ward 2', 'district': 'District 2', 'city': 'City 2', 'principal': 'David Williams', 'telephone': 1234567890, 'group': 'Group 2', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    {'name': 'Osafield Primary School', 'street': 'Maple Street', 'ward': 'Ward 3', 'district': 'District 3', 'city': 'City 3', 'principal': 'Oliver Taylor', 'telephone': 1234567890, 'group': 'Group 3', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    {'name': 'Osafield Secondary School', 'street': 'Maple Street', 'ward': 'Ward 3', 'district': 'District 3', 'city': 'City 3', 'principal': 'Sophia Wilson', 'telephone': 1234567890, 'group': 'Group 3', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    {'name': 'Osafield High School', 'street': 'Maple Street', 'ward': 'Ward 3', 'district': 'District 3', 'city': 'City 3', 'principal': 'William Martin', 'telephone': 1234567890, 'group': 'Group 3', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 1},
    # Add more school locations...
  ]
  for school_location in school_locations:
    location = Location(
      name=school_location['name'],
      street=school_location['street'],
      ward=school_location['ward'],
      district=school_location['district'],
      city=school_location['city'],
      principal=school_location['principal'],
      telephone=school_location['telephone'],
      group=school_location['group'],
      num_class_total=school_location['num_class_total'],
      num_f1=school_location['num_f1'],
      num_f2=school_location['num_f2'],
      num_f3=school_location['num_f3'],
      num_infant=school_location['num_infant'],
      office=school_location['office'],
      is_active=school_location['is_active'],
      location_type_id=school_location['location_type_id'],
    )
    db.session.add(location)
  db.session.commit()
  # Create warehouse locations
  warehouse_locations = [
    {'name': 'Greenfield Warehouse', 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'principal': 'John Doe', 'telephone': 1234567890, 'group': 'Group 1', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 2},
    {'name': 'Bluefield Warehouse', 'street': 'Pine Street', 'ward': 'Ward 2', 'district': 'District 2', 'city': 'City 2', 'principal': 'Jane Doe', 'telephone': 1234567890, 'group': 'Group 2', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 2},
    {'name': 'Osafield Warehouse', 'street': 'Maple Street', 'ward': 'Ward 3', 'district': 'District 3', 'city': 'City 3', 'principal': 'Mike Johnson', 'telephone': 1234567890, 'group': 'Group 3', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 2},
    # Add more warehouse locations...
  ]
  for warehouse_location in warehouse_locations:
    location = Location(
      name=warehouse_location['name'],
      street=warehouse_location['street'],
      ward=warehouse_location['ward'],
      district=warehouse_location['district'],
      city=warehouse_location['city'],
      principal=warehouse_location['principal'],
      telephone=warehouse_location['telephone'],
      group=warehouse_location['group'],
      num_class_total=warehouse_location['num_class_total'],
      num_f1=warehouse_location['num_f1'],
      num_f2=warehouse_location['num_f2'],
      num_f3=warehouse_location['num_f3'],
      num_infant=warehouse_location['num_infant'],
      office=warehouse_location['office'],
      is_active=warehouse_location['is_active'],
      location_type_id=warehouse_location['location_type_id'],
    )
    db.session.add(location)
  db.session.commit()
  
  # Create supplier locations
  supplier_locations = [
    {'name': 'Greenfield Supplier', 'street': 'Oak Street', 'ward': 'Ward 1', 'district': 'District 1', 'city': 'City 1', 'principal': 'John Doe', 'telephone': 1234567890, 'group': 'Group 1', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 3},
    {'name': 'Bluefield Supplier', 'street': 'Pine Street', 'ward': 'Ward 2', 'district': 'District 2', 'city': 'City 2', 'principal': 'Jane Doe', 'telephone': 1234567890, 'group': 'Group 2', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 3},
    {'name': 'Osafield Supplier', 'street': 'Maple Street', 'ward': 'Ward 3', 'district': 'District 3', 'city': 'City 3', 'principal': 'Mike Johnson', 'telephone': 1234567890, 'group': 'Group 3', 'num_class_total': 10, 'num_f1': 2, 'num_f2': 2, 'num_f3': 2, 'num_infant': 2, 'office': 2, 'is_active': True, 'location_type_id': 3},
    # Add more supplier locations...
  ] 
  
  for supplier_location in supplier_locations:
    location = Location(
      name=supplier_location['name'],
      street=supplier_location['street'],
      ward=supplier_location['ward'],
      district=supplier_location['district'],
      city=supplier_location['city'],
      principal=supplier_location['principal'],
      telephone=supplier_location['telephone'],
      group=supplier_location['group'],
      num_class_total=supplier_location['num_class_total'],
      num_f1=supplier_location['num_f1'],
      num_f2=supplier_location['num_f2'],
      num_f3=supplier_location['num_f3'],
      num_infant=supplier_location['num_infant'],
      office=supplier_location['office'],
      is_active=supplier_location['is_active'],
      location_type_id=supplier_location['location_type_id'],
    )
    db.session.add(location)
  db.session.commit()
  
  # Create tools
  tools = [
    {'name': 'Mouse', 'type': 'Input', 'model': 'Logitech', 'price': 10.00, 'quantity': 100},
    {'name': 'Keyboard', 'type': 'Input', 'model': 'Logitech', 'price': 20.00, 'quantity': 100},
    {'name': 'Monitor', 'type': 'Output', 'model': 'Dell', 'price': 100.00, 'quantity': 100},
    {'name': 'CPU', 'type': 'Processing', 'model': 'Intel', 'price': 200.00, 'quantity': 100},
    {'name': 'RAM', 'type': 'Memory', 'model': 'Kingston', 'price': 50.00, 'quantity': 100},
    {'name': 'HDD', 'type': 'Storage', 'model': 'Seagate', 'price': 80.00, 'quantity': 100},
    {'name': 'SSD', 'type': 'Storage', 'model': 'Samsung', 'price': 120.00, 'quantity': 100},
    {'name': 'Motherboard', 'type': 'Processing', 'model': 'Asus', 'price': 150.00, 'quantity': 100},
    {'name': 'GPU', 'type': 'Processing', 'model': 'Nvidia', 'price': 300.00, 'quantity': 100},
    {'name': 'PSU', 'type': 'Power', 'model': 'Corsair', 'price': 100.00, 'quantity': 100},
    {'name': 'Case', 'type': 'Output', 'model': 'Cooler Master', 'price': 70.00, 'quantity': 100},
    {'name': 'Table', 'type': 'Furniture', 'model': 'IKEA', 'price': 50.00, 'quantity': 100},
    {'name': 'Chair', 'type': 'Furniture', 'model': 'IKEA', 'price': 30.00, 'quantity': 100},
    {'name': 'Whiteboard', 'type': 'Furniture', 'model': 'IKEA', 'price': 40.00, 'quantity': 100},
  ]
  
  for tool in tools:
    tool = Tool(
      name=tool['name'],
      type=tool['type'],
      model=tool['model'],
      price=tool['price'],
      quantity=tool['quantity'],
      created_by=1,
      updated_by=1
    )
    db.session.add(tool)
  db.session.commit()
  
  # Create sell invoices
  sell_invoices = [
    {'name': 'Sell Invoice 1', 'description': 'Sell Invoice 1 Description', 'issue_date': datetime.strptime('2024-01-01', '%Y-%m-%d'), 'location_id': 1},
    {'name': 'Sell Invoice 2', 'description': 'Sell Invoice 2 Description', 'issue_date': datetime.strptime('2024-02-01', '%Y-%m-%d'), 'location_id': 2},
    {'name': 'Sell Invoice 3', 'description': 'Sell Invoice 3 Description', 'issue_date': datetime.strptime('2024-03-01', '%Y-%m-%d'), 'location_id': 3},
    {'name': 'Sell Invoice 4', 'description': 'Sell Invoice 4 Description', 'issue_date': datetime.strptime('2024-04-01', '%Y-%m-%d'), 'location_id': 4},
    {'name': 'Sell Invoice 5', 'description': 'Sell Invoice 5 Description', 'issue_date': datetime.strptime('2024-05-01', '%Y-%m-%d'), 'location_id': 5},
    # Add more sell invoices...
  ]
  
  for sell_invoice in sell_invoices:
    sell_invoice = SellInvoice(
      name=sell_invoice['name'],
      description=sell_invoice['description'],
      issue_date=sell_invoice['issue_date'],
      location_id=sell_invoice['location_id'],
      created_by=1,
      updated_by=1
    )
    db.session.add(sell_invoice)
  db.session.commit()
  
  # Create sell invoice items
  sell_invoice_items = [
    {'tool_name': 'Mouse', 'tool_type': 'Input', 'tool_model': 'Logitech', 'quantity': 10, 'price': 10.00, 'tool_id': 1, 'invoice_id': 1},
    {'tool_name': 'Keyboard', 'tool_type': 'Input', 'tool_model': 'Logitech', 'quantity': 20, 'price': 20.00, 'tool_id': 2, 'invoice_id': 1},
    {'tool_name': 'Monitor', 'tool_type': 'Output', 'tool_model': 'Dell', 'quantity': 5, 'price': 100.00, 'tool_id': 3, 'invoice_id': 2},
    {'tool_name': 'CPU', 'tool_type': 'Processing', 'tool_model': 'Intel', 'quantity': 3, 'price': 200.00, 'tool_id': 4, 'invoice_id': 2},
    {'tool_name': 'RAM', 'tool_type': 'Memory', 'tool_model': 'Kingston', 'quantity': 4, 'price': 50.00, 'tool_id': 5, 'invoice_id': 3},
    {'tool_name': 'HDD', 'tool_type': 'Storage', 'tool_model': 'Seagate', 'quantity': 2, 'price': 80.00, 'tool_id': 6, 'invoice_id': 3},
    {'tool_name': 'SSD', 'tool_type': 'Storage', 'tool_model': 'Samsung', 'quantity': 1, 'price': 120.00, 'tool_id': 7, 'invoice_id': 4},
    {'tool_name': 'Motherboard', 'tool_type': 'Processing', 'tool_model': 'Asus', 'quantity': 2, 'price': 150.00, 'tool_id': 8, 'invoice_id': 4},
    {'tool_name': 'GPU', 'tool_type': 'Processing', 'tool_model': 'Nvidia', 'quantity': 1, 'price': 300.00, 'tool_id': 9, 'invoice_id': 5},
    {'tool_name': 'PSU', 'tool_type': 'Power', 'tool_model': 'Corsair', 'quantity': 3, 'price': 100.00, 'tool_id': 10, 'invoice_id': 5},
    # Add more sell invoice items...
  ]
  
  for sell_invoice_item in sell_invoice_items:
    sell_invoice_item = InvoiceItem(
      tool_name=sell_invoice_item['tool_name'],
      tool_type=sell_invoice_item['tool_type'],
      tool_model=sell_invoice_item['tool_model'],
      quantity=sell_invoice_item['quantity'],
      price=sell_invoice_item['price'],
      tool_id=sell_invoice_item['tool_id'],
      invoice_id=sell_invoice_item['invoice_id'],
    )
    db.session.add(sell_invoice_item)
  db.session.commit()
  
  # Create Machines
  machines = [
    {'name': 'Printer', 'description': 'Printer Description', 'type': 'Printer', 'serial': 'PRINTER-001', 'model': 'HP', 'price': 100.00, 'status': MachineStatusEnum.AVAILABLE.value},
    {'name': 'Scanner', 'description': 'Scanner Description', 'type': 'Scanner', 'serial': 'SCANNER-001', 'model': 'Canon', 'price': 50.00, 'status': MachineStatusEnum.AVAILABLE.value},
    {'name': 'Projector', 'description': 'Projector Description', 'type': 'Projector', 'serial': 'PROJECTOR-001', 'model': 'Epson', 'price': 200.00, 'status': MachineStatusEnum.AVAILABLE.value},
    {'name': 'Laptop', 'description': 'Laptop Description', 'type': 'Laptop', 'serial': 'LAPTOP-001', 'model': 'Dell', 'price': 500.00, 'status': MachineStatusEnum.AVAILABLE.value},
    {'name': 'Desktop', 'description': 'Desktop Description', 'type': 'Desktop', 'serial': 'DESKTOP-001', 'model': 'HP', 'price': 400.00, 'status': MachineStatusEnum.AVAILABLE.value},
    {'name': 'Tablet', 'description': 'Tablet Description', 'type': 'Tablet', 'serial': 'TABLET-001', 'model': 'Samsung', 'price': 300.00, 'status': MachineStatusEnum.AVAILABLE.value},
    {'name': 'Smartphone', 'description': 'Smartphone Description', 'type': 'Smartphone', 'serial': 'SMARTPHONE-001', 'model': 'Apple', 'price': 600.00, 'status': MachineStatusEnum.AVAILABLE.value},
    {'name': 'Camera', 'description': 'Camera Description', 'type': 'Camera', 'serial': 'CAMERA-001', 'model': 'Canon', 'price': 700.00, 'status': MachineStatusEnum.AVAILABLE.value},
    {'name': 'Microphone', 'description': 'Microphone Description', 'type': 'Microphone', 'serial': 'MICROPHONE-001', 'model': 'Blue', 'price': 800.00, 'status': MachineStatusEnum.FIXING.value},
    {'name': 'Speaker', 'description': 'Speaker Description', 'type': 'Speaker', 'serial': 'SPEAKER-001', 'model': 'Bose', 'price': 900.00, 'status': MachineStatusEnum.HIRING.value},
    # Add more machines...
  ]
  
  for machine in machines:
    machine = Machine(
      name=machine['name'],
      description=machine['description'],
      type=machine['type'],
      serial=machine['serial'],
      model=machine['model'],
      price=machine['price'],
      status=machine['status'],
      created_by=1,
      updated_by=1
    )
    db.session.add(machine)
  db.session.commit()
  
  # Create rent invoices
  rent_invoices = [
    {'name': 'Rent Invoice 1', 'serial': 'RENT-001', 'start_date': datetime.strptime('2024-01-01', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-02-01', '%Y-%m-%d'), 'status': RentInvoiceStatusEnum.ACTIVE.value, 'price': 100.00, 'location_id': 1, 'machine_id': 1, 'user_id': 1},
    {'name': 'Rent Invoice 2', 'serial': 'RENT-002', 'start_date': datetime.strptime('2024-02-01', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-03-01', '%Y-%m-%d'), 'status': RentInvoiceStatusEnum.ACTIVE.value, 'price': 200.00, 'location_id': 2, 'machine_id': 2, 'user_id': 2},
    {'name': 'Rent Invoice 3', 'serial': 'RENT-003', 'start_date': datetime.strptime('2024-03-01', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-04-01', '%Y-%m-%d'), 'status': RentInvoiceStatusEnum.ACTIVE.value, 'price': 300.00, 'location_id': 3, 'machine_id': 3, 'user_id': 3},
    {'name': 'Rent Invoice 4', 'serial': 'RENT-004', 'start_date': datetime.strptime('2024-04-01', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-05-01', '%Y-%m-%d'), 'status': RentInvoiceStatusEnum.ACTIVE.value, 'price': 400.00, 'location_id': 4, 'machine_id': 4, 'user_id': 4},
    {'name': 'Rent Invoice 5', 'serial': 'RENT-005', 'start_date': datetime.strptime('2024-05-01', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-06-01', '%Y-%m-%d'), 'status': RentInvoiceStatusEnum.ACTIVE.value, 'price': 500.00, 'location_id': 5, 'machine_id': 5, 'user_id': 5},
    {'name': 'Rent Invoice 6', 'serial': 'RENT-006', 'start_date': datetime.strptime('2024-06-01', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-06-01', '%Y-%m-%d'), 'status': RentInvoiceStatusEnum.COMPLETED.value, 'price': 600.00, 'location_id': 6, 'machine_id': 6, 'user_id': 1},
    {'name': 'Rent Invoice 7', 'serial': 'RENT-007', 'start_date': datetime.strptime('2024-07-01', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-08-01', '%Y-%m-%d'), 'status': RentInvoiceStatusEnum.CANCELLED.value, 'price': 700.00, 'location_id': 7, 'machine_id': 7, 'user_id': 2},
    {'name': 'Rent Invoice 8', 'serial': 'RENT-008', 'start_date': datetime.strptime('2024-08-01', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-09-01', '%Y-%m-%d'), 'status': RentInvoiceStatusEnum.ACTIVE.value, 'price': 800.00, 'location_id': 8, 'machine_id': 8, 'user_id': 3},
    # Add more rent invoices...
  ]
  
  for rent_invoice in rent_invoices:
    rent_invoice = RentInvoice(
      name=rent_invoice['name'],
      serial=rent_invoice['serial'],
      start_date=rent_invoice['start_date'],
      end_date=rent_invoice['end_date'],
      status=rent_invoice['status'],
      price=rent_invoice['price'],
      location_id=rent_invoice['location_id'],
      machine_id=rent_invoice['machine_id'],
      user_id=rent_invoice['user_id'],
    )
    db.session.add(rent_invoice)
  db.session.commit()
  
  # Create rent invoice histories
  rent_invoice_histories = [
    {'status': MachineStatusEnum.HIRING.value, 'rent_invoice_id': 1},
    {'status': MachineStatusEnum.FIXING.value, 'rent_invoice_id': 2},
    {'status': MachineStatusEnum.HIRING.value, 'rent_invoice_id': 3},
    {'status': MachineStatusEnum.HIRING.value, 'rent_invoice_id': 4},
    {'status': MachineStatusEnum.FIXING.value, 'rent_invoice_id': 5},
    {'status': MachineStatusEnum.FIXING.value, 'rent_invoice_id': 6},
    {'status': MachineStatusEnum.HIRING.value, 'rent_invoice_id': 7},
    {'status': MachineStatusEnum.FIXING.value, 'rent_invoice_id': 8},
    # Add more rent invoice histories...
  ]
  
  for rent_invoice_history in rent_invoice_histories:
    rent_invoice_history = RentInvoiceHistory(
      status=rent_invoice_history['status'],
      rent_invoice_id=rent_invoice_history['rent_invoice_id'],
    )
    db.session.add(rent_invoice_history)
  db.session.commit()
  
  print('Seeding completed!')