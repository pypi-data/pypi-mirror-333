# flask_gen/cli.py

import click
from flask_gen.src import app_creator, project_creator

@click.group(help="Flask Project Generator CLI")
def cli():
    """Interface en ligne de commande pour générer des projets Flask."""
    pass

@cli.command("project", help="Initialise un projet Flask complet")
@click.argument("name")
@click.argument("path", default=".")
def init_project(name, path):
    """
    Initialise un projet Flask complet.
    
    NAME: nom du projet.
    PATH: chemin de destination (par défaut : répertoire courant).
    """
    project_creator.init_project(name, path)
    click.echo(f"Projet '{name}' initialisé à {path}.")

@cli.command("app", help="Initialise une nouvelle application (blueprint) Flask")
@click.argument("name")
@click.argument("path", default=".")
def init_app(name, path):
    """
    Initialise une nouvelle application (blueprint).

    NAME: nom de l'application.
    PATH: répertoire du projet où sera créée l'application (par défaut : répertoire courant).
    """
    app_creator.init_app(name, path)
    click.echo(f"Application '{name}' initialisée à {path}.")

if __name__ == "__main__":
    cli()
