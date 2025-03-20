# flask_gen/commands.py

import click
from flask.cli import AppGroup
from flask_gen.src import project_creator, app_creator

gen_cli = AppGroup('gen', help="Initialization commands for your Flask project.")

# @gen_cli.command('project')
# @click.argument("name")
# @click.argument("path", default=".")
# def init_project(name, path):
#     """Initialize a complete Flask project."""
#     project_creator.init_project(name, path)
#     click.echo(f"Project '{name}' has been initialized at {path}.")

@gen_cli.command('app')
@click.argument("name")
@click.argument("path", default=".")
def init_app(name, path):
    """Initialize a new Flask application (blueprint)."""
    app_creator.init_app(name, path)
    click.echo(f"App '{name}' has been initialized at {path}.")
