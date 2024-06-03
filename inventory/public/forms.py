# -*- coding: utf-8 -*-
"""Public forms."""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired

from inventory.user.models import User

class ChangePasswordForm(FlaskForm):
    """Change password form."""

    old_password = PasswordField("Old password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm new password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, **kwargs):
        """Validate the form."""
        initial_validation = super(ChangePasswordForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=current_user.username).first()
        if self.new_password.data != self.confirm_password.data:
            self.confirm_password.errors.append("Passwords must match")
            return False

        if not self.user.check_password(self.old_password.data):
            self.old_password.errors.append("Invalid password")
            return False

        if self.old_password.data == self.new_password.data:
            self.new_password.errors.append("New password must be different from old password")
            return False
        return True


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, **kwargs):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Unknown username")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        if not self.user.is_active:
            self.username.errors.append("User not activated")
            return False
        return True
