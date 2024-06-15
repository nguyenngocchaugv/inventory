# forms.py
from enum import Enum
from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import SelectField
from wtforms.validators import DataRequired

from inventory.location.models import Location, LocationType, LocationTypeEnum

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