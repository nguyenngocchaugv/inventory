# -*- coding: utf-8 -*-
"""Tool views."""
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
from inventory.tool.forms import ToolForm
from inventory.tool.models import Tool
from inventory.utils import flash_errors

blueprint = Blueprint("tool", __name__, url_prefix="/tools", static_folder="../static")


@blueprint.route("/")
@login_required
def tools():
  """List tools."""
  tools = Tool.query.filter_by(is_deleted=False).order_by(desc(Tool.id)).all()
  return render_template("tools/tools.html", tools=tools)

@blueprint.route('/<int:tool_id>', methods=['GET'])
@login_required
def view_tool(tool_id):
  tool = Tool.query.get(tool_id)
  if tool and not tool.is_deleted:
    form = ToolForm(obj=tool)
    return render_template('tools/tool.html', tool=tool, form=form, mode='View')
  else:
    flash("Tool not found.", "danger")
    return redirect(url_for('tool.tools'))

@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_tool():
  """Create a new tool."""
  form = ToolForm(request.form)
  current_app.logger.info(form.data)

  if form.validate_on_submit():
    Tool.create(
      name=form.name.data,
      type=form.type.data,
      model=form.model.data,
      price=form.price.data,
      quantity=form.quantity.data,
    )
    flash("Tool is created successfully.", "success")
    return redirect(url_for('tool.tools'))
  else:
    flash_errors(form)
  return render_template("tools/tool.html", form=form, mode='Create')

@blueprint.route("/<int:tool_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_tool(tool_id):
  """View or edit a tool."""
  tool = Tool.query.get(tool_id)
  if not tool:
    flash("Tool not found.", "danger")
    return redirect(url_for('tool.tools'))

  if request.method == 'POST':
    form = ToolForm(request.form)
  else:
    form = ToolForm(obj=tool)
    
  if form.validate_on_submit():
    tool.update( 
     name=form.name.data,
      type=form.type.data,
      model=form.model.data,
      price=form.price.data,
      quantity=form.quantity.data,
    )
    flash("Tool is updated successfully.", "success")
    return redirect(url_for('tool.view_tool', tool_id=tool.id))
  else:
      flash_errors(form)

  return render_template("tools/tool.html", form=form, mode='Edit', tool=tool)

@blueprint.route('/delete_tool/<int:tool_id>', methods=['POST'])
@login_required
def delete_tool(tool_id):
  tool = Tool.query.get(tool_id)
  if tool:
    Tool.delete(tool)
    flash("Tool is deleted successfully.", "success")
  else:
    flash("Tool not found.", "danger")
  return jsonify({'redirect_url': url_for('tool.tools')})