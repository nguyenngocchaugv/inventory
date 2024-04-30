# -*- coding: utf-8 -*-
"""Location views."""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint("location", __name__, url_prefix="/locations", static_folder="../static")


@blueprint.route("/")
@login_required
def locations():
  """List locations."""
  locations = [
    {"name": "Warehouse", "id": 1},
    {"name": "Tool Crib", "id": 2},
    {"name": "Machine Shop", "id": 3},
  ]
  return render_template("locations/locations.html", locations=locations)
