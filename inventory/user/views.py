# -*- coding: utf-8 -*-
"""User views."""
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
from flask_login import current_user, login_required
from sqlalchemy import desc
from inventory.user.forms import UserForm
from inventory.user.models import Role, User
from inventory.utils import flash_errors

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def users():
  """List users."""
  users = User.query.join(User.role).filter(Role.name != 'SuperAdmin').order_by(desc(User.id)).all()
  return render_template("users/users.html", users=users)

@blueprint.route('/<int:user_id>', methods=['GET'])
@login_required
def view_user(user_id):
  user = User.query.get(user_id)
  
  if user:
    form = UserForm(obj=user)
    return render_template('users/user.html', user=user, form=form, mode='View')
  else:
    flash("User not found.", "danger")
    return redirect(url_for('user.users'))

@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_user():
  """Create a new user."""
  form = UserForm(request.form)
  
  form.role.choices = [(role.id, role.name) for role in Role.query.all() if role.name != 'SuperAdmin']
  
  if form.validate_on_submit():
    User.create(
      first_name=form.first_name.data,
      last_name=form.last_name.data,
      email=form.email.data,
      telephone=form.telephone.data,
      username=form.username.data,
      password=form.password.data,
      street=form.street.data,
      ward=form.ward.data,
      district=form.district.data,
      city=form.city.data,
      state=form.state.data,
      zip_code=form.zip_code.data,
      position=form.position.data,
      work_duration=form.work_duration.data,
      is_active=form.is_active.data == 'True',
      role_id=form.role.data,
      created_by=current_user.id,
      updated_by=current_user.id
    )
    flash(f"User {form.first_name.data} {form.last_name.data} is created successfully.", "success")
    return redirect(url_for('user.users'))
  else:
    flash_errors(form)
  return render_template("users/user.html", form=form, mode='Create')

@blueprint.route("/<int:user_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
  """View or edit a user."""
  user = User.query.get(user_id)
  if not user:
    flash("User not found.", "danger")
    return redirect(url_for('user.users'))

  if request.method == 'POST':
    form = UserForm(request.form)
    
    current_app.logger.info(user)
  else:
    form = UserForm(obj=user)
    
  if form.validate_on_submit():
    user.update( 
      first_name=form.first_name.data,
      last_name=form.last_name.data,
      email=form.email.data,
      telephone=form.telephone.data,
      username=form.username.data,
      password=form.password.data,
      street=form.street.data,
      ward=form.ward.data,
      district=form.district.data,
      city=form.city.data,
      state=form.state.data,
      zip_code=form.zip_code.data,
      position=form.position.data,
      work_duration=form.work_duration.data,
      is_active=form.is_active.data == 'True',
      role_id=form.role.data,
      updated_by=current_user.id
    )
    flash(f"User {user.first_name} {user.last_name} is updated successfully.", "success")
    return redirect(url_for('user.view_user', user_id=user.id))
  else:
      flash_errors(form)

  return render_template("users/user.html", form=form, mode='Edit', user=user)

@blueprint.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
  user = User.query.get(user_id)
  if user:
    User.delete(user)
    flash(f"User {user.first_name} {user.last_name} is deleted successfully.", "success")
  else:
    flash("User not found.", "danger")
  return jsonify({'redirect_url': url_for('user.users')})