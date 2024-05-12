# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from wtforms import ValidationError


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)

def validate_decimal_places(form, field):
  if round(field.data, 2) != field.data:
    raise ValidationError('Field must have at most 2 decimal places.')