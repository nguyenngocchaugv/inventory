# -*- coding: utf-8 -*-
"""Location views."""
from flask import (
  Blueprint,
  flash,
  redirect,
  render_template,
  url_for,
  request
)
from flask_login import login_required
from sqlalchemy import desc
from inventory.location.forms import LocationForm
from inventory.location.models import Location, LocationType
from inventory.utils import flash_errors

blueprint = Blueprint("location", __name__, url_prefix="/locations", static_folder="../static")


@blueprint.route("/")
@login_required
def locations():
  """List locations."""
  locations = Location.query.order_by(desc(Location.id)).all()
  return render_template("locations/locations.html", locations=locations)

@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_location():
  """Create a new location."""
  form = LocationForm(request.form)
  form.location_type.choices = [(lt.id, lt.name) for lt in LocationType.query.all()]
  if form.validate_on_submit():
    Location.create(
      name=form.name.data,
      street=form.street.data,
      ward=form.ward.data,
      district=form.district.data,
      city=form.city.data,
      principal=form.principal.data,
      telephone=form.telephone.data,
      group=form.group.data,
      num_class_total=form.num_class_total.data,
      num_f1=form.num_f1.data,
      num_f2=form.num_f2.data,
      num_f3=form.num_f3.data,
      num_infant=form.num_infant.data,
      office=form.office.data,
      status=form.status.data == 'True',
      location_type_id=form.location_type.data
    )
    flash("Location is created successfully.", "success")
    return redirect(url_for('location.locations'))
  else:
    flash_errors(form)
  return render_template("locations/new_location.html", form=form)
