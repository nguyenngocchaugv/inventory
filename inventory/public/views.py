# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from inventory.extensions import login_manager
from inventory.public.forms import ChangePasswordForm, LoginForm
from inventory.user.forms import RegisterForm
from inventory.user.models import User
from inventory.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.users")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))

@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    """Login page."""
    # If the user is already authenticated, redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    # Store the next URL in the session
    next_page = request.args.get('next')
    if next_page:
        session['next'] = next_page

    form = LoginForm(request.form)
    # Check the form is valid on submission (i.e., we're in a POST request)
    if form.validate_on_submit():
        # Log in the user
        login_user(form.user)
        flash("You are logged in.", "success")
        # If login successful, redirect to next URL or default URL
        next_page = session.pop('next', None)
        return redirect(next_page or '/')
    else:
        flash_errors(form)
    return render_template("public/login.html", form=form)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('public.login', next=request.url))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)

@blueprint.route("/change-password/", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password."""
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        current_user.save()
        flash("Password updated.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/change_password.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
