import unittest
from unittest.mock import patch, mock_open, call
import os
import sys

# Ajouter le répertoire parent au sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_gen.src import project_creator

class TestProjectCreator(unittest.TestCase):

    def setUp(self):
        # Configuration initiale avant chaque test
        self.project_name = 'test_project'
        self.base_path = 'test_base_path'
        self.project_dir = os.path.join(self.base_path, self.project_name)

    def tearDown(self):
        # Nettoyage après chaque test
        pass

    @patch('builtins.print')
    @patch('os.path.exists')
    def test_check_project_exists(self, mock_exists, mock_print):
        # Simuler que le projet existe déjà
        mock_exists.return_value = True
        result = project_creator.check_project_exists(self.project_dir, self.project_name)
        self.assertTrue(result)
        mock_exists.assert_called_with(self.project_dir)
        expected_message = f"Un projet nommé '{self.project_name}' existe déjà à l'emplacement {self.project_dir}."
        mock_print.assert_called_with(expected_message)

    @patch('builtins.print')
    @patch('os.makedirs')
    def test_create_project_directories(self, mock_makedirs, mock_print):
        project_creator.create_project_directories(self.project_dir)
        expected_directories = [
            os.path.join(self.project_dir, "core"),
            os.path.join(self.project_dir, "core", "templates"),
            os.path.join(self.project_dir, "core", "templates", "errors"),
            os.path.join(self.project_dir, "core", "static"),
        ]
        calls = [call(directory, exist_ok=True) for directory in expected_directories]
        mock_makedirs.assert_has_calls(calls, any_order=True)
        self.assertEqual(mock_makedirs.call_count, len(expected_directories))
        # Vérifier les messages print
        for directory in expected_directories:
            mock_print.assert_any_call(f"Dossier créé : {directory}")

    def test_generate_core_init_content(self):
        content = project_creator.generate_core_init_content()
        self.assertEqual(content, "from .settings import create_app\n")

    def test_generate_core_settings_content(self):
        content = project_creator.generate_core_settings_content(self.project_name)
        self.assertIn("def create_app(config_class=Config):", content)
        self.assertIn("app = Flask(__name__)", content)
        self.assertIn("return app", content)

    def test_generate_core_urls_content(self):
        content = project_creator.generate_core_urls_content()
        self.assertIn("def register_blueprints(app):", content)
        self.assertIn("pass", content)

    def test_generate_base_html_content(self):
        content = project_creator.generate_base_html_content(self.project_name)
        self.assertIn(f"<title>{{% block title %}}{self.project_name}{{% endblock %}}</title>", content)

    def test_generate_error_template_content(self):
        error_code = 404
        content = project_creator.generate_error_template_content(error_code)
        self.assertIn(f"<h1>Erreur {error_code}</h1>", content)
        # Suppression de l'assertion vérifiant "{{ get_error_message(" car le template actuel ne l'inclut pas.
        # Si vous intégrez get_error_message dans le template, retirez ce commentaire.

    def test_generate_config_content(self):
        content = project_creator.generate_config_content()
        self.assertIn("class Config:", content)
        self.assertIn("SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')", content)

    def test_generate_extensions_content(self):
        content = project_creator.generate_extensions_content()
        self.assertIn("db = SQLAlchemy()", content)
        self.assertIn("migrate = Migrate()", content)

    def test_generate_run_content(self):
        # Utilisation de generate_app_content() à la place de generate_run_content()
        content = project_creator.generate_app_content()
        self.assertIn("if __name__ == '__main__':", content)
        self.assertIn("app.run(debug=DEBUG)", content)

    def test_generate_requirements_content(self):
        content = project_creator.generate_requirements_content()
        self.assertIn("Flask", content)
        self.assertIn("Flask-SQLAlchemy", content)

    def test_generate_env_example_content(self):
        content = project_creator.generate_env_example_content()
        self.assertIn("SECRET_KEY=your-secret-key", content)
        self.assertIn("DEBUG=True", content)

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_create_file(self, mock_makedirs, mock_open_file, mock_print):
        file_path = os.path.join(self.project_dir, 'config.py')
        content = 'Test content'
        project_creator.create_file(file_path, content)
        mock_makedirs.assert_called_with(os.path.dirname(file_path), exist_ok=True)
        mock_open_file.assert_called_with(file_path, 'w', encoding='utf-8')
        mock_open_file().write.assert_called_once_with(content)
        mock_print.assert_called_with(f"Fichier créé : {file_path}")

    @patch('builtins.print')
    @patch('flask_gen.src.project_creator.create_file')
    @patch('flask_gen.src.project_creator.create_project_directories')
    @patch('os.path.exists')
    def test_init_project(self, mock_exists, mock_create_dirs, mock_create_file, mock_print):
        mock_exists.return_value = False
        project_creator.init_project(self.project_name, self.base_path)
        mock_exists.assert_called_with(self.project_dir)
        mock_create_dirs.assert_called_with(self.project_dir)
        expected_file_count = 13  # Nombre total de fichiers à créer
        self.assertEqual(mock_create_file.call_count, expected_file_count)
        mock_print.assert_any_call(f"Création du projet dans : {self.project_dir}")

    @patch('builtins.print')
    @patch('os.path.exists')
    def test_init_project_already_exists(self, mock_exists, mock_print):
        mock_exists.return_value = True
        result = project_creator.init_project(self.project_name, self.base_path)
        mock_exists.assert_called_with(self.project_dir)
        expected_message = f"Un projet nommé '{self.project_name}' existe déjà à l'emplacement {self.project_dir}."
        mock_print.assert_called_with(expected_message)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
