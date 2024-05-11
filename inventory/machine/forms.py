# -*- coding: utf-8 -*-
"""Public forms."""
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, IntegerField, SubmitField, FloatField, ValidationError, TextAreaField
from wtforms.validators import DataRequired
from enum import Enum

class Status(Enum):
  READY = "READY"
  FIXING = "FIXING"
  HIRING = "HIRING"
    
def validate_decimal_places(form, field):
  if round(field.data, 2) != field.data:
    raise ValidationError('Field must have at most 2 decimal places.')
    
      
class MachineForm(FlaskForm):
  """Machine form."""
  id = HiddenField()
  name = StringField('Name', validators=[DataRequired()])
  description = TextAreaField('Description')
  type = StringField('Type', validators=[DataRequired()])
  serial = StringField('Serial', validators=[DataRequired()])
  model = StringField('Model', validators=[DataRequired()])
  price = FloatField('Price', validators=[DataRequired(), validate_decimal_places])
  status = SelectField('Status',
                       choices=[(status.value, status.value) for status in Status],
                       default=Status.READY.value,
                       render_kw={'disabled': True})
  submit = SubmitField('Submit')
  
  def validate(self, **kwargs):
    # Convert status from string to enum
    if 'status' in self.data:
      self.data['status'] = Status[self.data['status']]
      
    return super().validate(**kwargs)
  
  
