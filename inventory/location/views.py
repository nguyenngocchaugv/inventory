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
  page = request.args.get('page', 1, type=int)
  per_page = 10
  locations = Location.query.filter_by(is_deleted=False).order_by(desc(Location.id)).paginate(page=page, per_page=per_page, error_out=False)
  return render_template("locations/locations.html", locations=locations)

@blueprint.route("/search", methods=["GET"])
def search():
  """Search locations."""
  search_term = request.args.get('q', '')
  page = request.args.get('page', 1, type=int)
  per_page = 10
  if search_term == '':  # Show all locations if no search term
    return redirect(url_for('location.locations', page=page))
  
  locations = Location.query.filter_by(is_deleted=False).filter(Location.name.contains(search_term)).order_by(desc(Location.id)).paginate(page=page, per_page=per_page, error_out=False)
  return render_template("locations/locations.html", locations=locations, search_term=search_term)

@blueprint.route('/<int:location_id>', methods=['GET'])
@login_required
def view_location(location_id):
  location = Location.query.get(location_id)
  if location and not location.is_deleted:
    form = LocationForm(obj=location)
    form.location_type.choices = [(lt.id, lt.name) for lt in LocationType.query.all()]
    form.location_type.data = location.location_type.id  # Set the selected value
    return render_template('locations/location.html', location=location, form=form, mode='View')
  else:
    flash("Location not found.", "danger")
    return redirect(url_for('location.locations'))

@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_location():
  """Create a new location."""
  form = LocationForm(request.form)
  
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
      is_active=form.is_active.data == 'True',
      location_type_id=form.location_type.data
    )
    flash(f"Location {form.name.data} is created successfully.", "success")
    return redirect(url_for('location.locations'))
  else:
    flash_errors(form)
  return render_template("locations/location.html", form=form, mode='Create')

@blueprint.route("/<int:location_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
  """View or edit a location."""
  location = Location.query.get(location_id)
  if not location or location.is_deleted:
    flash("Location not found.", "danger")
    return redirect(url_for('location.locations'))

  if request.method == 'POST':
    form = LocationForm(request.form)
  else:
    form = LocationForm(obj=location)

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
      is_active=form.is_active.data == 'True',
      location_type_id=form.location_type.data
    )
    flash(f"Location {form.name.data} is updated successfully.", "success")
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
    flash(f"Location {location.name} is deleted successfully.", "success")
  else:
    flash("Location not found.", "danger")
  return jsonify({'redirect_url': url_for('location.locations')})