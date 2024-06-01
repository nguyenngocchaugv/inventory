# -*- coding: utf-8 -*-
"""Public forms."""
from collections import defaultdict
from flask_wtf import FlaskForm
from wtforms import DateTimeField, DecimalField, FieldList, FormField, HiddenField, SelectField, StringField, IntegerField, SubmitField, FloatField, ValidationError
from wtforms.validators import DataRequired, NumberRange

from db.seeds import LocationTypeEnum
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
  price = DecimalField('Price')
  tool_prices = {}

  def __init__(self, *args, **kwargs):
    super(InvoiceItemForm, self).__init__(*args, **kwargs)
    tools = [(str(t.id), t.name) for t in Tool.query.filter_by(is_deleted=False).all()]
    # Add a placeholder option with an empty value
    tools.insert(0, ('', 'Select a tool...'))
    self.tool.choices = tools
    # Query the Tool objects again for tool_prices
    tool_objects = Tool.query.filter_by(is_deleted=False).all()
    self.tool_prices = {'tool_' + str(tool.id): str(tool.price) for tool in tool_objects}
    
    if kwargs.get('obj'):
      self.tool.data = str(kwargs['obj'].tool_id)
      # Set the price from the InvoiceItem object instead of the Tool object
      self.price.data = kwargs['obj'].price
      self.quantity.data = kwargs['obj'].quantity
      
  
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
  invoice_item_forms = FieldList(FormField(InvoiceItemForm))
  submit = SubmitField('Submit')
  
  def __init__(self, *args, **kwargs):
    super(SellInvoiceForm, self).__init__(*args, **kwargs)
    locations = [(str(location.id), location.name) for location in Location.query
                 .join(Location.location_type)
                 .filter(LocationType.name==LocationTypeEnum.SCHOOL.value).all()]
    locations.insert(0, ('', 'Select a school...'))
    self.location.choices = locations
    
     # Set the default value for the location dropdown
    if kwargs.get('obj'):
      self.location.data = str(kwargs['obj'].location_id)
      self.invoice_item_forms = [InvoiceItemForm(obj=item) for item in kwargs['obj'].invoice_items]
    
  def validate(self, extra_validators=None):
    # Call the parent class's validate method
    if not super(SellInvoiceForm, self).validate(extra_validators=extra_validators):
      return False
    
    # Check if at least one item has been added
    if len(self.invoice_item_forms) == 0:
      self.invoice_item_forms.errors.append('At least one item must be added to the invoice.')
      return False

    # Calculate the total quantity for each tool
    total_quantities = defaultdict(int)
    for item_form in self.invoice_item_forms:
      total_quantities[item_form.tool.data] += item_form.quantity.data
      
    # Check if the total quantity for each tool is less than or equal to the quantity available
    for tool_id, total_quantity in total_quantities.items():
      tool = Tool.query.get(tool_id)
      if tool and total_quantity > tool.quantity:
        self.invoice_item_forms.errors.append('The total quantity for tool {} is larger than the quantity available.'.format(tool.name))
        return False
      
    return True
    
  def validate_name(self, field):
    """Validate invoice name."""
    invoice = SellInvoice.query.filter_by(name=field.data).first()
    if invoice and (not self.id.data or invoice.id != int(self.id.data)):
      raise ValidationError('Invoice name already registered')
    