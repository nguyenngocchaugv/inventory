# forms.py
from enum import Enum
from flask import current_app
from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import DateTimeField, SelectField, ValidationError
from wtforms.validators import DataRequired

from inventory.location.models import Location, LocationType, LocationTypeEnum
from inventory.machine.models import Machine
from inventory.tool.models import Tool

class SchoolReportTypeEnum(Enum):
  SELL = 'Sell'
  RENT = 'Rent'

class SchoolReportForm(FlaskForm):
  location = SelectField('Location', coerce=str, validators=[DataRequired()])
  city = SelectField('City', coerce=str, validators=[DataRequired()])
  type = SelectField('Type', validators=[DataRequired()], choices=[(report_type.value, report_type.value) for report_type in SchoolReportTypeEnum])
  
  def __init__(self, *args, **kwargs):
    super(SchoolReportForm, self).__init__(*args, **kwargs)
    all_schools = Location.query.join(Location.location_type).filter(and_(LocationType.name==LocationTypeEnum.SCHOOL.value, Location.is_deleted == False)).all()
    
    self.location.choices = [(str(location.id), location.name) for location in all_schools]
    
    city_names = list(set([location.city for location in all_schools]))
    self.city.choices = [(city_name, city_name) for city_name in city_names]
    
class MachineAvailabilityForm(FlaskForm):
  serial = SelectField('Serial', coerce=str, validators=[DataRequired()])
  model = SelectField('Model', coerce=str, validators=[DataRequired()])
  start_date = DateTimeField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
  end_date = DateTimeField('End Date', format='%Y-%m-%d', validators=[DataRequired()])

  def __init__(self, *args, **kwargs):
    super(MachineAvailabilityForm, self).__init__(*args, **kwargs)

    all_machines = Machine.query.filter(Machine.is_deleted == False).all()
    
    # Extract unique serials and models
    serials = [("All", "All")] + list(set((machine.serial, machine.serial) for machine in all_machines))
    models = [("All", "All")] + list(set((machine.model, machine.model) for machine in all_machines))
    
    # Sort the lists if desired
    serials.sort(key=lambda x: x[1])
    models.sort(key=lambda x: x[1])
    
    # Set the choices for the serial and model fields
    self.serial.choices = serials
    self.model.choices = models
  
  def validate_end_date(self, field):
    if self.start_date.data and field.data:
      if field.data < self.start_date.data:
        raise ValidationError("End date should not be earlier than start date.")
      
class SoldToolsForm(FlaskForm):
  start_date = DateTimeField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
  end_date = DateTimeField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
  type = SelectField('Serial', coerce=str, validators=[DataRequired()])
  model = SelectField('Model', coerce=str, validators=[DataRequired()])
  
  def __init__(self, *args, **kwargs):
    super(SoldToolsForm, self).__init__(*args, **kwargs)

    all_tools = Tool.query.filter(Tool.is_deleted == False).all()
    
    # Extract unique serials and models
    types = [("All", "All")] + list(set((tool.type, tool.type) for tool in all_tools))
    models = [("All", "All")] + list(set((tool.model, tool.model) for tool in all_tools))
    
    # Sort the lists if desired
    types.sort(key=lambda x: x[1])
    models.sort(key=lambda x: x[1])
    
    # Set the choices for the serial and model fields
    self.type.choices = types
    self.model.choices = models
  
  def validate_end_date(self, field):
    if self.start_date.data and field.data:
      if field.data < self.start_date.data:
        raise ValidationError("End date should not be earlier than start date.")