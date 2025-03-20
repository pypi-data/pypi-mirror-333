import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Flask-gen",
    version="0.1.0",
    author="Tshongani Hamadou",
    author_email="sirehtshongany@gmail.com",
    description="A command-line tool to generate Flask projects and applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/htshongany/Flask-gen",
    packages=setuptools.find_packages(),
    package_dir={
        'flask_gen.src': 'flask_gen/src',
        'flask_gen': 'flask_gen'
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
    "Flask>=2.0.0,<3.0.0",
    "Flask-SQLAlchemy>=2.5.0,<3.0.0",
    "Flask-Migrate>=3.0.0,<4.0.0",
    "python-dotenv>=0.15.0,<2.0.0",
    "SQLAlchemy>=1.4,<2.0"
    ],
    entry_points={
        'console_scripts': [
            'flask-gen=flask_gen.cli:cli',
        ],
        'flask.commands': [
            'gen=flask_gen.commands:gen_cli',
        ],
    },
)
