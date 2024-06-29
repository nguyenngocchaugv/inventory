# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, RadioField, SelectField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import Role, User

class UserForm(FlaskForm):
  """User form."""
  id = HiddenField()
  first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=25)])
  last_name = StringField('Last Name', validators=[Length(min=3, max=25)])
  email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
  telephone = StringField('Telephone', validators=[Length(min=6, max=20)])
  username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
  confirm = PasswordField('Verify password', [DataRequired(), EqualTo('password', message='Passwords must match')])
  street = StringField('Street', validators=[Length(max=20)])
  ward = StringField('Ward', validators=[Length(max=20)])
  district = StringField('District', validators=[Length(max=20)])
  city = StringField('City', validators=[Length(max=20)])
  state = StringField('State', validators=[Length(max=20)])
  zip_code = StringField('Zip Code', validators=[Length(max=20)])
  position = StringField('Position', validators=[DataRequired(), Length(max=50)])
  work_duration = StringField('Work Duration', validators=[DataRequired()])
  is_active = RadioField('Is Active', choices=[(True, 'Active'), (False, 'Inactive')], validators=[DataRequired()], default='True')
  role = SelectField('Role', coerce=int)
  submit = SubmitField('Submit')
  
  def __init__(self, *args, **kwargs):
    super(UserForm, self).__init__(*args, **kwargs)
    roles = [(role.id, role.name) for role in Role.query.all() if role.name != 'SuperAdmin']
    self.role.choices = roles
    
    if kwargs.get('obj'):
      self.role.data = kwargs['obj'].role_id
    
  def validate_username(self, field):
    """Validate username."""
    user = User.query.filter_by(username=field.data).first()
    if user and (not self.id.data or user.id != int(self.id.data)):
      raise ValidationError('Username already registered')
    
class EditUserForm(FlaskForm):
  """Edit User form."""
  id = HiddenField()
  first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=25)])
  last_name = StringField('Last Name', validators=[Length(min=3, max=25)])
  email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
  telephone = StringField('Telephone', validators=[Length(min=6, max=20)])
  username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
  street = StringField('Street', validators=[Length(max=20)])
  ward = StringField('Ward', validators=[Length(max=20)])
  district = StringField('District', validators=[Length(max=20)])
  city = StringField('City', validators=[Length(max=20)])
  state = StringField('State', validators=[Length(max=20)])
  zip_code = StringField('Zip Code', validators=[Length(max=20)])
  position = StringField('Position', validators=[DataRequired(), Length(max=50)])
  work_duration = StringField('Work Duration', validators=[DataRequired()])
  is_active = RadioField('Is Active', choices=[(True, 'Active'), (False, 'Inactive')], validators=[DataRequired()], default='True')
  role = SelectField('Role', coerce=int)
  submit = SubmitField('Submit')
  
  def __init__(self, *args, **kwargs):
    super(EditUserForm, self).__init__(*args, **kwargs)
    roles = [(role.id, role.name) for role in Role.query.all() if role.name != 'SuperAdmin']
    self.role.choices = roles
    
    if kwargs.get('obj'):
      self.role.data = kwargs['obj'].role_id
    
  def validate_username(self, field):
    """Validate username."""
    user = User.query.filter_by(username=field.data).first()
    if user and (not self.id.data or user.id != int(self.id.data)):
      raise ValidationError('Username already registered')


class RegisterForm(FlaskForm):
  """Register form."""

  username = StringField(
    "Username", validators=[DataRequired(), Length(min=3, max=25)]
  )
  email = StringField(
    "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
  )
  password = PasswordField(
    "Password", validators=[DataRequired(), Length(min=6, max=40)]
  )
  confirm = PasswordField(
    "Verify password",
    [DataRequired(), EqualTo("password", message="Passwords must match")],
  )

  def __init__(self, *args, **kwargs):
    """Create instance."""
    super(RegisterForm, self).__init__(*args, **kwargs)
    self.user = None

  def validate(self, **kwargs):
    """Validate the form."""
    initial_validation = super(RegisterForm, self).validate()
    if not initial_validation:
      return False
    user = User.query.filter_by(username=self.username.data).first()
    if user:
      self.username.errors.append("Username already registered")
      return False
    user = User.query.filter_by(email=self.email.data).first()
    if user:
      self.email.errors.append("Email already registered")
      return False
    return True
