# -*- coding: utf-8 -*-
"""User views."""
import io
from flask import (
  Blueprint,
  flash,
  jsonify,
  redirect,
  render_template,
  send_file,
  url_for,
  request
)
from flask_login import current_user, login_required
import pandas as pd
from sqlalchemy import and_, desc
from inventory.user.forms import EditUserForm, UserForm
from inventory.user.models import Role, RoleEnum, User
from inventory.utils import flash_errors

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def users():
  """List users."""
  page = request.args.get('page', 1, type=int)
  per_page = 10
  users = User.query.join(User.role).filter(Role.name != RoleEnum.SUPER_ADMIN.value).order_by(desc(User.id)).paginate(page=page, per_page=per_page, error_out=False)
  return render_template("users/users.html", users=users)

@blueprint.route("/search", methods=["GET"])
def search():
  """Search users."""
  search_term = request.args.get('q', '')
  page = request.args.get('page', 1, type=int)
  per_page = 10
  if search_term == '':  # Show all users if no search term
    return redirect(url_for('user.users', page=page))
  
  users = User.query.join(User.role).filter(and_(Role.name != RoleEnum.SUPER_ADMIN.value, User.email.contains(search_term))).order_by(desc(User.id)).paginate(page=page, per_page=per_page, error_out=False)
  return render_template("users/users.html", users=users, search_term=search_term)

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
    form = EditUserForm(request.form)
  else:
    form = EditUserForm(obj=user)
    
  if form.validate_on_submit():
    user.update( 
      first_name=form.first_name.data,
      last_name=form.last_name.data,
      email=form.email.data,
      telephone=form.telephone.data,
      username=form.username.data,
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

@blueprint.route('/export', methods=['GET'])
@login_required
def export_users():
  """Export users to Excel."""
  users = User.query.join(User.role).filter(Role.name != RoleEnum.SUPER_ADMIN.value).order_by(desc(User.id)).all()
  
  # Convert the users data to a pandas DataFrame
  data = {
    'First Name': [user.first_name for user in users],
    'Last Name': [user.last_name for user in users],
    'Email': [user.email for user in users],
    'Telephone': [user.telephone for user in users],
    'Username': [user.username for user in users],
    'Street': [user.street for user in users],
    'Ward': [user.ward for user in users],
    'District': [user.district for user in users],
    'City': [user.city for user in users],
    'State': [user.state for user in users],
    'Zip Code': [user.zip_code for user in users],
    'Position': [user.position for user in users],
    'Work Duration': [user.work_duration for user in users],
    'Role': [user.role.name for user in users],
    'Is Active': [user.is_active for user in users],
  }
  
  df = pd.DataFrame(data)
  
  # Create an in-memory BytesIO object
  output = io.BytesIO()
  # Write the DataFrame to the BytesIO object
  with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Sheet1')

  # Create a Flask response with the Excel file
  output.seek(0)
  return send_file(output, download_name='users.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')