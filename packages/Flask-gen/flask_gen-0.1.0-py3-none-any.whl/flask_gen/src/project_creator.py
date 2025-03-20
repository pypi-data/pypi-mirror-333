import os

def check_project_exists(project_dir, project_name):
    """
    Vérifie si un projet existe déjà au chemin donné.
    Retourne True s'il existe, False sinon.
    """
    if os.path.exists(project_dir):
        print(f"Un projet nommé '{project_name}' existe déjà à l'emplacement {project_dir}.")
        return True
    return False

def create_project_directories(project_dir):
    """
    Crée les dossiers nécessaires pour le projet.
    """
    directories = [
        os.path.join(project_dir, "core"),
        os.path.join(project_dir, "core", "templates"),
        os.path.join(project_dir, "core", "templates", "errors"),  # Pour les pages d'erreur
        os.path.join(project_dir, "core", "static"),  # Pour les fichiers statiques
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Dossier créé : {directory}")

def generate_core_init_content():
    """
    Génère le contenu pour le fichier core/__init__.py
    """
    return "from .settings import create_app\n"

def generate_core_settings_content(project_name):
    """
    Génère le contenu pour le fichier core/settings.py
    """
    content = f'''import os
from flask import Flask, render_template
from config import Config
from extensions import db, migrate

DEBUG = True

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Enregistrement des blueprints
    from core.urls import register_blueprints
    register_blueprints(app)

    # Gestion des erreurs si l'application n'est pas en mode debug
    if not DEBUG:
        @app.errorhandler(404)
        def not_found_error(error):
            return render_template("errors/404.html"), 404

        @app.errorhandler(403)
        def forbidden_error(error):
            return render_template("errors/403.html"), 403

        @app.errorhandler(500)
        def internal_error(error):
            return render_template("errors/500.html"), 500

    return app
'''
    return content

def generate_core_urls_content():
    """
    Génère le contenu pour le fichier core/urls.py
    """
    content = '''"""
Pour enregistrer les blueprints de votre application, importez-les et ajoutez-les ici.

Exemple :
    from blog.routes.urls import blog_register_blueprints

    def register_blueprints(app):
        blog_register_blueprints(app)
"""

def register_blueprints(app):
    pass
'''
    return content

def generate_base_html_content(project_name):
    """
    Génère le contenu pour le fichier core/templates/base.html
    """
    content = f'''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{% block title %}}{project_name}{{% endblock %}}</title>
</head>
<body>
    {{% block content %}}{{% endblock %}}
</body>
</html>
'''
    return content

def generate_error_template_content(error_code):
    """
    Génère le contenu pour les pages d'erreur.
    """
    content = f'''{{% extends "base.html" %}}
{{% block content %}}
<h1>Erreur {error_code}</h1>
{{% endblock %}}
'''
    return content

def generate_config_content():
    """
    Génère le contenu pour le fichier config.py
    """
    content = '''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''
    return content

def generate_extensions_content():
    """
    Génère le contenu pour le fichier extensions.py
    """
    content = '''from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
'''
    return content

def generate_app_content():
    """
    Génère le contenu pour le fichier app.py
    """
    content = '''from core.settings import create_app, DEBUG

app = create_app()

if __name__ == '__main__':
    app.run(debug=DEBUG)
'''
    return content

def generate_requirements_content():
    """
    Génère le contenu pour le fichier requirements.txt
    """
    content = '''Flask
Flask-SQLAlchemy
Flask-Migrate
python-dotenv
'''
    return content

def generate_env_example_content():
    """
    Génère le contenu pour le fichier .env.example
    """
    content = '''SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///site.db
FLASK_ENV=development
'''
    return content

def create_file(filepath, content):
    """
    Crée un fichier avec le contenu spécifié.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fichier créé : {filepath}")

def init_project(project_name, base_path):
    """
    Initialise un projet Flask complet avec configuration par défaut,
    Flask-SQLAlchemy, Flask-Migrate, gestion des erreurs, et un fichier .env exemple.
    """
    project_dir = os.path.join(base_path, project_name)

    # Vérifier si le projet existe déjà
    if check_project_exists(project_dir, project_name):
        return  # Sortir de la fonction sans créer le projet

    print(f"Création du projet dans : {project_dir}")

    # Créer les dossiers nécessaires
    create_project_directories(project_dir)

    # Créer les fichiers avec leur contenu
    files_to_create = {
        # core/__init__.py
        os.path.join(project_dir, "core", "__init__.py"): generate_core_init_content(),

        # core/settings.py
        os.path.join(project_dir, "core", "settings.py"): generate_core_settings_content(project_name),

        # core/urls.py
        os.path.join(project_dir, "core", "urls.py"): generate_core_urls_content(),

        # core/templates/base.html
        os.path.join(project_dir, "core", "templates", "base.html"): generate_base_html_content(project_name),

        # core/templates/errors/*.html
        os.path.join(project_dir, "core", "templates", "errors", "404.html"): generate_error_template_content(404),
        os.path.join(project_dir, "core", "templates", "errors", "403.html"): generate_error_template_content(403),
        os.path.join(project_dir, "core", "templates", "errors", "500.html"): generate_error_template_content(500),

        # config.py
        os.path.join(project_dir, "config.py"): generate_config_content(),

        # extensions.py
        os.path.join(project_dir, "extensions.py"): generate_extensions_content(),

        # app.py
        os.path.join(project_dir, "app.py"): generate_app_content(),

        # requirements.txt
        os.path.join(project_dir, "requirements.txt"): generate_requirements_content(),

        # .env.example
        os.path.join(project_dir, ".env.example"): generate_env_example_content(),

        # core/static/styles.css (fichier CSS vide)
        os.path.join(project_dir, "core", "static", "styles.css"): '/* Ajoutez vos styles CSS personnalisés ici */',
    }

    for filepath, content in files_to_create.items():
        create_file(filepath, content)