# -*- coding: utf-8 -*-
"""Public forms."""
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, IntegerField, SubmitField, RadioField, ValidationError
from wtforms.validators import DataRequired

from inventory.location.models import Location, LocationType

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
  is_active = RadioField('Is Active', choices=[(True, 'Active'), (False, 'Inactive')], validators=[DataRequired()], default='True')
  submit = SubmitField('Submit')
  
  def __init__(self, *args, **kwargs):
    super(LocationForm, self).__init__(*args, **kwargs)
    location_types = [(lt.id, lt.name) for lt in LocationType.query.all()]
    self.location_type.choices = location_types
    
    if kwargs.get('obj'):
      self.location_type.data = kwargs['obj'].location_type_id
  
  def validate_name(self, field):
    """Validate location name."""
    location = Location.query.filter_by(is_deleted=False).filter_by(name=field.data).first()
    if location and not location.is_deleted and (not self.id.data or location.id != int(self.id.data)):
      raise ValidationError('Location name already registered')
