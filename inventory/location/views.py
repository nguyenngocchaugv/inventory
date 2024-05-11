# -*- coding: utf-8 -*-
"""Location views."""
from flask import (
  Blueprint,
  flash,
  jsonify,
  redirect,
  render_template,
  url_for,
  request
)
from flask import current_app
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

@blueprint.route('/<int:location_id>', methods=['GET'])
@login_required
def view_location(location_id):
  location = Location.query.get(location_id)
  if location:
    form = LocationForm(obj=location)
    form.location_type.choices = [(lt.id, lt.name) for lt in LocationType.query.all()]
    return render_template('locations/location.html', location=location, form=form, mode='View')
  else:
    flash("Location not found.", "danger")
    return redirect(url_for('location.locations'))

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
  return render_template("locations/location.html", form=form, mode='Create')

@blueprint.route("/<int:location_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
  """View or edit a location."""
  location = Location.query.get(location_id)
  if not location:
    flash("Location not found.", "danger")
    return redirect(url_for('location.locations'))

  if request.method == 'POST':
    form = LocationForm(request.form)
    
    current_app.logger.info(location)
  else:
    form = LocationForm(obj=location)
    
  form.location_type.choices = [(lt.id, lt.name) for lt in LocationType.query.all()]

  if form.validate_on_submit():
    location.update( 
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
    flash("Location is updated successfully.", "success")
    return redirect(url_for('location.view_location', location_id=location.id))
  else:
      flash_errors(form)

  return render_template("locations/location.html", form=form, mode='Edit', location=location)

@blueprint.route('/delete_location/<int:location_id>', methods=['POST'])
@login_required
def delete_location(location_id):
  location = Location.query.get(location_id)
  if location:
    Location.delete(location)
    flash("Location is deleted successfully.", "success")
  else:
    flash("Location not found.", "danger")
  return jsonify({'redirect_url': url_for('location.locations')})