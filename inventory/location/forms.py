# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, IntegerField, SubmitField, RadioField, ValidationError
from wtforms.validators import DataRequired

from inventory.location.models import Location

class LocationForm(FlaskForm):
  """Location form."""
  id = HiddenField()
  name = StringField('Location Name', validators=[DataRequired()])
  location_type = SelectField('Location Type', coerce=int)
  street = StringField('Street', validators=[DataRequired()])
  ward = StringField('Ward', validators=[DataRequired()])
  district = StringField('District', validators=[DataRequired()])
  city = StringField('City', validators=[DataRequired()])
  principal = StringField('Principal', validators=[DataRequired()])
  telephone = IntegerField('Telephone', validators=[DataRequired()])
  group = StringField('Group', validators=[DataRequired()])
  num_class_total = IntegerField('Total Class', validators=[DataRequired()])
  num_f1 = IntegerField('Num F1', validators=[DataRequired()])
  num_f2 = IntegerField('Num F2', validators=[DataRequired()])
  num_f3 = IntegerField('Num F3', validators=[DataRequired()])
  num_infant = IntegerField('Num Infant', validators=[DataRequired()])
  office = IntegerField('Office', validators=[DataRequired()])
  status = RadioField('Status', choices=[(True, 'Active'), (False, 'Inactive')], validators=[DataRequired()], default='True')
  submit = SubmitField('Submit')
  
  def validate_name(self, field):
    """Validate location name."""
    location = Location.query.filter_by(name=field.data).first()
    if location and (not self.id.data or location.id != int(self.id.data)):
      raise ValidationError('Location name already registered')
