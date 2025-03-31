import click
from flask import Flask
from flask.cli import with_appcontext

from .storage import init_db

@click.command("createdb")
@with_appcontext
def init_db_command():
    init_db()

def register_commands(app:Flask):
    app.cli.add_command(init_db_command)