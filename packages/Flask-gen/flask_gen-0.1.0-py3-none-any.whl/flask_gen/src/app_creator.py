import os

def check_app_exists(app_path):
    """
    Checks if an application already exists at the given path.
    Returns True if it exists, False otherwise.
    """
    exists = os.path.exists(app_path)
    if exists:
        print(f"An application named '{os.path.basename(app_path)}' already exists at {app_path}.")
    return exists

def create_app_directories(app_path, app_name):
    """
    Creates the necessary directories for the application.
    """
    directories = [
        app_path,
        os.path.join(app_path, "models"),
        os.path.join(app_path, "routes"),
        os.path.join(app_path, "templates", app_name),
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory created: {directory}")

def generate_routes_index_content(app_name):
    """
    Generates the content for routes/index.py file.
    """
    content = f"""import os
from flask import Blueprint, render_template

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
{app_name}_bp = Blueprint('{app_name}', __name__, template_folder=template_dir)

@{app_name}_bp.route('/')
def index():
    return render_template('{app_name}/index.html', app_name='{app_name}')
"""
    return content

def generate_routes_urls_content(app_name):
    """
    Generates the content for routes/urls.py file.
    """
    content = f'''"""
To register the '{app_name}' blueprint in your 'core/urls.py', add the following:

    from {app_name}.routes.urls import {app_name}_register_blueprints

    def register_blueprints(app):
        {app_name}_register_blueprints(app)

Example with 'blog' app:

    from blog.routes.urls import blog_register_blueprints

    def register_blueprints(app):
        blog_register_blueprints(app)
"""

from {app_name}.routes.index import {app_name}_bp

def {app_name}_register_blueprints(app):
    app.register_blueprint({app_name}_bp, url_prefix='/{app_name}')
'''
    return content

def generate_index_html_content(app_name):
    """
    Generates the content for templates/<app_name>/index.html file.
    """
    content = f"""{{% extends 'base.html' %}}
{{% block title %}}{app_name.capitalize()} - Home{{% endblock %}}

{{% block content %}}
<h1>App {app_name.capitalize()} is working perfectly!</h1>
{{% endblock %}}
"""
    return content

def create_file(filepath, content):
    """
    Creates a file with the specified content.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"File created: {filepath}")

def init_app(app_name, project_dir):
    """
    Initializes a new application (blueprint) in an existing project.

    The application will be created in the directory: project_dir/<app_name>
    """
    app_path = os.path.join(project_dir, app_name)

    # Check if the app already exists
    if check_app_exists(app_path):
        return  # Exit the function without creating the app

    print(f"Creating the application in: {app_path}")
    
    # Create necessary directories
    create_app_directories(app_path, app_name)

    # Create files with their content
    # routes/index.py
    index_py_path = os.path.join(app_path, "routes", "index.py")
    index_py_content = generate_routes_index_content(app_name)
    create_file(index_py_path, index_py_content)

    # routes/urls.py
    urls_py_path = os.path.join(app_path, "routes", "urls.py")
    urls_py_content = generate_routes_urls_content(app_name)
    create_file(urls_py_path, urls_py_content)

    # templates/<app_name>/index.html
    index_html_path = os.path.join(app_path, "templates", app_name, "index.html")
    index_html_content = generate_index_html_content(app_name)
    create_file(index_html_path, index_html_content)
