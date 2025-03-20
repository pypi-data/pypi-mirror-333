# Flask-Gen

**Flask-Gen** is a command-line utility for Flask that simplifies the generation of full Flask projects and modular applications (blueprints). Inspired by Django’s “startproject” and “startapp” commands, it automatically sets everything up by generating a well-structured project with default settings, custom error pages, integration with databases (using Flask-SQLAlchemy and Flask-Migrate), and more.

## Features

- **Project Generation:** Quickly generate a fresh Flask project with a standard directory structure (e.g., static, templates, and error pages).
- **App (Blueprint) Creation:** Rapidly create modular apps (blueprints) that can be directly included in your project.
- **Django-Inspired Workflow:** Leverage the convenience of app and project creation as in Django.
- **Preconfigured Setup:** Automates the creation of files such as `config.py`, `extensions.py`, and default error templates.
- **Extensible:** Simple to extend and customize as per your specific requirements.

## Installation

Install Flask-Gen using pip (Python version 3.7 and above):

```bash
pip install flask-gen
```

*Note:* In the unlikely event that the package is not yet available on PyPI, it can be installed from a local clone by running:

```bash
pip install .
```

## Usage

Flask-Gen operates in two modes:

### 1. Execute CLI Commands via `flask-gen`

These globally available commands enable you to construct a complete project or a modular application (blueprint).

#### Start a New Project

To begin a complete Flask project with a properly organized setup, use:

```bash
flask-gen project <project_name> [path]
```

**Example:**

```bash
flask-gen project my_flask_project .
```

This command accomplishes:
- Checking if a project already exists in the specified location.
- Setting up the necessary directory structure, e.g., core directories, template directories, static files, and error pages.
- Generating required files such as `config.py`, `extensions.py`, `app.py`, and a sample `.env` file.

#### Create a New Application (Blueprint)

To add a new modular application (blueprint) to an existing project or any directory, use:

```bash
flask-gen app <app_name> [path]
```

**Example:**

```bash
flask-gen app blog .
```

This command accomplishes:
- Ensuring an application with the same name does not already exist.
- Setting up the necessary directory structure, e.g., `models/`, `routes/`, and a dedicated templates directory.
- Generating required boilerplate files, such as a default route and a simple template.

### 2. Flask CLI Integration for Blueprint Creation

Flask-Gen also provides support for integration with Flask's built-in CLI for generating new blueprints (applications) in an existing project.

#### Key Points:
- This is meant for creating new applications, not full-fledged projects.
- Ensure that you are in the root directory of your Flask application (at the same level as `app.py`) before running this command.

To build a blueprint with Flask’s CLI integration, run:

```bash
flask gen app <app_name> [path]
```

**Example:**

```bash
flask gen app store 
```

It leverages Flask’s CLI framework, making it ideal for adding more blueprints in an existing project.

## Project Structure

After running the **project** command, your directory should look like this:

```
my_flask_project/
├── config.py
├── extensions.py
├── app.py
├── requirements.txt
├── .env.example
└── core/
    ├── __init__.py       # Imports the create_app function from settings
    ├── settings.py       # Default settings with the create_app function
    ├── urls.py           # Placeholder for blueprint registration
    ├── templates/
    │   ├── base.html     # Base HTML template
    │   └── errors/
    │       ├── 404.html
    │       ├── 403.html
    │       └── 500.html
    └── static/
        └── styles.css    # Styles file for customization
```

When developing a new application (blueprint), the directory layout is as follows:

```
blog/
├── models/
├── routes/
│   ├── index.py        # Contains a sample route that renders a template
│   └── urls.py         # Registers the blueprint with a URL prefix
└── templates/
    └── blog/
        └── index.html  # Sample template for the blog app
```

## Contributing

Your contributions are welcome. Submit issues or make a pull request in the [GitHub repository](https://github.com/htshongany/Flask-gen). See the guidelines in the CONTRIBUTING.md file.

## License

This software is released under the MIT License. See the [LICENSE](LICENSE) file for more information.
