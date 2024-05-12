# -*- coding: utf-8 -*-
"""Public forms."""
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange

from inventory.utils import validate_decimal_places
    
      
class ToolForm(FlaskForm):
  """Tool form."""
  id = HiddenField()
  name = StringField('Name', validators=[DataRequired()])
  type = StringField('Type', validators=[DataRequired()])
  model = StringField('Model', validators=[DataRequired()])
  price = FloatField('Price', validators=[DataRequired(), validate_decimal_places])
  quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
  submit = SubmitField('Submit')
 
  
  
