# -*- coding: utf-8 -*-
"""Public forms."""
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import DateTimeField, DecimalField, FieldList, FormField, HiddenField, SelectField, StringField, IntegerField, SubmitField, FloatField, ValidationError
from wtforms.validators import DataRequired, NumberRange

from inventory.location.models import Location, LocationType
from inventory.tool.models import SellInvoice, Tool
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
 
class InvoiceItemForm(FlaskForm):
  tool = SelectField('Tool', coerce=str, validators=[DataRequired()])
  quantity = IntegerField('Quantity', validators=[DataRequired()])
  price = DecimalField('Price', validators=[DataRequired()])

  def __init__(self, *args, **kwargs):
    super(InvoiceItemForm, self).__init__(*args, **kwargs)
    
    tools = [(str(t.id), t.name) for t in Tool.query.all()]
    
    # Add a placeholder option with an empty value
    tools.insert(0, ('', 'Select a tool...'))
    self.tool.choices = tools
  
  # form.tool.choices = tools  # Populate the tool dropdown
  def validate_quantity(self, field):
    tool = Tool.query.filter_by(name=self.tool.data).first()
    if tool and field.data > tool.quantity:
      raise ValidationError('The quantity entered is larger than the quantity available.')
    
class SellInvoiceForm(FlaskForm):
  """SellInvoice form."""
  id = HiddenField()
  name = StringField('Invoice Name', validators=[DataRequired()])
  description = StringField('Description', validators=[DataRequired()])
  issue_date = DateTimeField('Issue Date', format='%Y-%m-%d', validators=[DataRequired()])
  location = SelectField('Location', coerce=str, validators=[DataRequired()])
  invoice_item_forms = FieldList(FormField(InvoiceItemForm), min_entries=1)
  submit = SubmitField('Submit')
  
  def __init__(self, *args, **kwargs):
    super(SellInvoiceForm, self).__init__(*args, **kwargs)
    locations = [(str(location.id), location.name) for location in Location.query.join(Location.location_type).filter(LocationType.name=='School').all()]
    locations.insert(0, ('', 'Select a school...'))
    self.location.choices = locations
    
  def validate_name(self, field):
    """Validate invoice name."""
    invoice = SellInvoice.query.filter_by(name=field.data).first()
    if invoice and (not self.id.data or invoice.id != int(self.id.data)):
      raise ValidationError('Invoice name already registered')
    