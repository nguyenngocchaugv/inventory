# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, IntegerField, SubmitField, RadioField, ValidationError
from wtforms.validators import DataRequired

class MachineForm(FlaskForm):
  """Machine form."""
  id = HiddenField()
  name = StringField('Name', validators=[DataRequired()])
  # location_type = SelectField('Location Type', coerce=int)
  # street = StringField('Street', validators=[DataRequired()])
  # ward = StringField('Ward', validators=[DataRequired()])
  # district = StringField('District', validators=[DataRequired()])
  # city = StringField('City', validators=[DataRequired()])
  # principal = StringField('Principal', validators=[DataRequired()])
  # telephone = IntegerField('Telephone', validators=[DataRequired()])
  # group = StringField('Group', validators=[DataRequired()])
  # num_class_total = IntegerField('Total Class', validators=[DataRequired()])
  # num_f1 = IntegerField('Num F1', validators=[DataRequired()])
  # num_f2 = IntegerField('Num F2', validators=[DataRequired()])
  # num_f3 = IntegerField('Num F3', validators=[DataRequired()])
  # num_infant = IntegerField('Num Infant', validators=[DataRequired()])
  # office = IntegerField('Office', validators=[DataRequired()])
  # status = RadioField('Status', choices=[(True, 'Active'), (False, 'Inactive')], validators=[DataRequired()], default='True')
  submit = SubmitField('Submit')
