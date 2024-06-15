# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys
import os
import click
from flask.cli import with_appcontext
from flask import Flask, render_template
from jinja2 import Undefined
from sqlalchemy import MetaData

from inventory import commands, public, report, user, location, machine, tool
from inventory.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)


def create_app(config_object="inventory.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    # define the database path to be in the 'db' subfolder
    database_path = os.path.join(os.getcwd(), 'db', 'dev.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
  
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_filters(app)
    configure_logger(app)
    return app

@click.command("seed")
@with_appcontext
def seed_db():
    """Seed the database."""
    from db.seeds import seed
    seed()

def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)

    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    # debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.dashboard_views.blueprint)
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(location.views.blueprint)
    app.register_blueprint(machine.views.blueprint)
    app.register_blueprint(machine.rent_invoice_views.blueprint)
    app.register_blueprint(tool.views.blueprint)
    app.register_blueprint(tool.sell_invoice_views.blueprint)
    app.register_blueprint(report.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            "db": db,
            "User": user.models.User
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(seed_db)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler('flask.log')
    if not app.logger.handlers:
        app.logger.addHandler(handler)
        app.logger.addHandler(file_handler)

def register_filters(app):
    """Register custom Jinja filters."""

    def format_thousands(value):
        if value is None or isinstance(value, Undefined):
            return ''
        return '{:,}'.format(value)

    app.jinja_env.filters['format_thousands'] = format_thousands