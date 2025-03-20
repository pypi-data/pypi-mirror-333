# flask_init/__init__.py

from flask import Flask
from flask_gen.commands import init_cli

def create_app():
    app = Flask(__name__)
    # Enregistre le groupe de commandes personnalisées dans l'application
    app.cli.add_command(init_cli)
    return app

# Optionnel : Crée une instance globale pour simplifier la détection par Flask
app = create_app()