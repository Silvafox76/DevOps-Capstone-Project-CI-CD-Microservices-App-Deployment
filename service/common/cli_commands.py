"""
CLI Commands for Flask App
"""

import click
from flask.cli import with_appcontext

from service.models import db


@click.command("db-create")
@with_appcontext
def db_create():
    """Creates the database tables"""
    db.create_all()
    click.echo("Database created")


def register_commands(app):
    """Register CLI commands with the Flask app"""
    app.cli.add_command(db_create)
