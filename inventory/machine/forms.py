# -*- coding: utf-8 -*-
"""Public forms."""
from flask import current_app
from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import DateTimeField, HiddenField, SelectField, StringField, IntegerField, SubmitField, FloatField, ValidationError, TextAreaField
from wtforms.validators import DataRequired
from enum import Enum

from db.seeds import LocationTypeEnum, RoleEnum
from inventory.location.models import Location, LocationType
from inventory.machine.models import Machine
from inventory.user.models import Role, User
from inventory.utils import validate_decimal_places

class MachineStatusEnum(Enum):
  AVAILABLE = "AVAILABLE"
  FIXING = "FIXING"
  HIRING = "HIRING"
  
class RentInvoiceStatusEnum(Enum):
  ACTIVE = "ACTIVE"
  COMPLETED = "COMPLETED"
  CANCELLED = "CANCELLED"
    
class RentInvoiceForm(FlaskForm):
  """Rent invoice form."""
  id = HiddenField()
  name = StringField('Name', validators=[DataRequired()])
  serial = StringField('Serial', validators=[DataRequired()])
  start_date = DateTimeField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
  end_date = DateTimeField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
  status = SelectField('Status',
                       choices=[(status.value, status.value) for status in RentInvoiceStatusEnum],
                       default=RentInvoiceStatusEnum.ACTIVE.value,
                       render_kw={'disabled': True})
  price = FloatField('Price', validators=[DataRequired(), validate_decimal_places])
  location = SelectField('Location', coerce=str)
  machine = SelectField('Machine', coerce=str)
  user = SelectField('Assign to', coerce=str)
  submit = SubmitField('Submit')
  
  def __init__(self, *args, **kwargs):
    super(RentInvoiceForm, self).__init__(*args, **kwargs)
    locations = [(str(location.id), location.name) for location in Location.query
                 .join(Location.location_type)
                 .filter(and_(LocationType.name==LocationTypeEnum.SCHOOL.value, Location.is_deleted == False, Location.is_active == True)).all()]
    locations.insert(0, ('', 'Select a school...'))
    self.location.choices = locations
    
    users = [(str(user.id), user.email) for user in User.query
             .join(User.role)
             .filter(and_(User.is_active == True, User.is_deleted == False, Role.name == RoleEnum.USER.value))
             .all()]
    users.insert(0, ('', 'Assign to...'))
    self.user.choices = users
    
    machines = [(str(machine.id), machine.name) for machine in Machine.query
                .filter(and_(Machine.status==MachineStatusEnum.AVAILABLE.value, Machine.is_deleted == False)).all()]
    machines.insert(0, ('', 'Select a machine...'))
    self.machine.choices = machines
    current_app.logger.info(self.machine.choices)
    
    
    # Set the choices for the status field based on the current status of the invoice
    # current_app.logger.info(kwargs.field)
    # in case of editing an existing invoice, the status field should be enabled
    # if kwargs.get('obj') and kwargs['obj'].status == RentInvoiceStatusEnum.ACTIVE.value:
    #   self.status.choices = [(status.value, status.value) for status in [RentInvoiceStatusEnum.COMPLETED, RentInvoiceStatusEnum.CANCELLED]]
    #   # self.status.render_kw = {'disabled': False}
    # else:
    #   self.status.choices = [(RentInvoiceStatusEnum.ACTIVE.value, RentInvoiceStatusEnum.ACTIVE.value)]
    #   # self.status.render_kw = {'disabled': True}
    # current_app.logger.info(self.status.choices)
    
     # Set the choices for the status field based on the mode
    # if mode == 'Create':
    #   self.status.choices = [(RentInvoiceStatusEnum.ACTIVE.value, RentInvoiceStatusEnum.ACTIVE.value)]
    # elif mode == 'View':
    #   self.status.choices = [(status.value, status.value) for status in RentInvoiceStatusEnum]
    # elif mode == 'Edit':
    #   self.status.choices = [(status.value, status.value) for status in RentInvoiceStatusEnum]
    
     # Set the default value for the location dropdown
    if kwargs.get('obj'):
      self.status.choices = [(RentInvoiceStatusEnum.ACTIVE.value, RentInvoiceStatusEnum.ACTIVE.value)]
      self.location.data = str(kwargs['obj'].location_id)
      self.user.data = str(kwargs['obj'].user_id)
      
      # machine = Machine.query.get(kwargs['obj'].machine_id)
      # self.machine.choices = [(str(machine.id), machine.name)]
      
      self.machine.data = str(kwargs['obj'].machine_id)
  def validate_end_date(self, field):
    if self.start_date.data and field.data:
      if field.data < self.start_date.data:
        raise ValidationError("End date should not be earlier than start date.")
      
class RentInvoiceEditForm(FlaskForm):
  """Rent invoice edit form."""
  id = HiddenField()
  name = StringField('Name')
  serial = StringField('Serial')
  start_date = DateTimeField('Start Date', format='%Y-%m-%d')
  end_date = DateTimeField('End Date', format='%Y-%m-%d')
  status = SelectField('Status')
  price = FloatField('Price', validators=[DataRequired(), validate_decimal_places])
  location = SelectField('Location', coerce=str)
  machine = SelectField('Machine', coerce=str)
  user = SelectField('Assign to', coerce=str)
  submit = SubmitField('Submit')
  
  def __init__(self, *args, **kwargs):
    super(RentInvoiceEditForm, self).__init__(*args, **kwargs)
    
    if kwargs.get('obj'):
      location = Location.query.get(kwargs.get('obj').location_id)
    
      self.location.choices = [(str(location.id), location.name)]    
      
      user = User.query.get(kwargs.get('obj').user_id)
      self.user.choices = [(str(user.id), user.email)]
      
      machine = Machine.query.get(kwargs.get('obj').machine_id)
      self.machine.choices = [(str(machine.id), machine.name)]
      
      self.status.choices = [(status.value, status.value) for status in RentInvoiceStatusEnum]
      
      self.location.data = str(kwargs['obj'].location_id)
      self.user.data = str(kwargs['obj'].user_id)
      self.machine.data = str(kwargs['obj'].machine_id)
      
class MachineForm(FlaskForm):
  """Machine form."""
  id = HiddenField()
  name = StringField('Name', validators=[DataRequired()])
  description = TextAreaField('Description')
  type = StringField('Type', validators=[DataRequired()])
  serial = StringField('Serial', validators=[DataRequired()])
  model = StringField('Model', validators=[DataRequired()])
  price = FloatField('Price', validators=[DataRequired(), validate_decimal_places])
  status = SelectField('Status', coerce=str)
  submit = SubmitField('Submit')
  
  def __init__(self, *args, **kwargs):
    super(MachineForm, self).__init__(*args, **kwargs)

    # Set the choices for the status field based on the current status of the machine
    if kwargs.get('obj'):
      if kwargs['obj'].status == MachineStatusEnum.AVAILABLE.value:
        self.status.choices = [(MachineStatusEnum.AVAILABLE.value, MachineStatusEnum.AVAILABLE.value)]
        # self.status.render_kw = {'disabled': True}
      elif kwargs['obj'].status in [MachineStatusEnum.HIRING.value, MachineStatusEnum.FIXING.value]:
        self.status.choices = [(status.value, status.value) for status in [MachineStatusEnum.HIRING, MachineStatusEnum.FIXING]]
        # self.status.render_kw = {'disabled': False}
    else:
      self.status.choices = [(MachineStatusEnum.AVAILABLE.value, MachineStatusEnum.AVAILABLE.value)]
      self.status.default=MachineStatusEnum.AVAILABLE.value
      # self.status.render_kw = {'disabled': True}
    current_app.logger.info(self.status.choices)
  
  
  def validate(self, **kwargs):
    # Convert status from string to enum
    if 'status' in self.data and self.data['status'] is not None:
      self.data['status'] = MachineStatusEnum[self.data['status']]
      
    return super().validate(**kwargs)
  
  
