import unittest
from unittest.mock import patch, mock_open, call
import os
import sys

# Add the parent directory to sys.path to import flask_gen
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_gen.src import app_creator

class TestAppCreator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('builtins.print')
    @patch('os.path.exists')
    def test_check_app_exists(self, mock_exists, mock_print):
        mock_exists.return_value = True
        app_path = 'test_project/existing_app'
        result = app_creator.check_app_exists(app_path)
        self.assertTrue(result)
        mock_exists.assert_called_with(app_path)
        mock_print.assert_called_with(
            f"An application named '{os.path.basename(app_path)}' already exists at {app_path}."
        )

    @patch('builtins.print')
    @patch('os.makedirs')
    def test_create_app_directories(self, mock_makedirs, mock_print):
        app_name = 'test_app'
        app_path = 'test_project/test_app'
        app_creator.create_app_directories(app_path, app_name)
        expected_directories = [
            app_path,
            os.path.join(app_path, "models"),
            os.path.join(app_path, "routes"),
            os.path.join(app_path, "templates", app_name),
        ]
        calls = [unittest.mock.call(directory, exist_ok=True) for directory in expected_directories]
        mock_makedirs.assert_has_calls(calls, any_order=True)
        self.assertEqual(mock_makedirs.call_count, len(expected_directories))
        for directory in expected_directories:
            mock_print.assert_any_call(f"Directory created: {directory}")

    def test_generate_routes_index_content(self):
        app_name = 'test_app'
        content = app_creator.generate_routes_index_content(app_name)
        self.assertIn(f"{app_name}_bp = Blueprint('{app_name}'", content)
        self.assertIn(f"@{app_name}_bp.route('/')" , content)
        self.assertIn(
            f"return render_template('{app_name}/index.html', app_name='{app_name}')" , content
        )

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_create_file(self, mock_makedirs, mock_open_file, mock_print):
        file_path = 'test_project/test_file.txt'
        content = 'Test content'
        app_creator.create_file(file_path, content)
        mock_makedirs.assert_called_with(os.path.dirname(file_path), exist_ok=True)
        mock_open_file.assert_called_with(file_path, 'w', encoding='utf-8')
        mock_open_file().write.assert_called_once_with(content)
        mock_print.assert_called_with(f"File created: {file_path}")

    @patch('builtins.print')
    @patch('flask_gen.src.app_creator.create_file')
    @patch('flask_gen.src.app_creator.create_app_directories')
    @patch('os.path.exists')
    def test_init_app(self, mock_exists, mock_create_dirs, mock_create_file, mock_print):
        mock_exists.return_value = False
        app_name = 'test_app'
        project_dir = 'test_project'
        app_path = os.path.join(project_dir, app_name)
        app_creator.init_app(app_name, project_dir)
        mock_exists.assert_called_with(app_path)
        mock_create_dirs.assert_called_with(app_path, app_name)
        self.assertEqual(mock_create_file.call_count, 3)  # index.py, urls.py, index.html
        mock_print.assert_called_with(f"Creating the application in: {app_path}")

    @patch('builtins.print')
    @patch('os.path.exists')
    def test_init_app_already_exists(self, mock_exists, mock_print):
        mock_exists.return_value = True
        app_name = 'existing_app'
        project_dir = 'test_project'
        app_path = os.path.join(project_dir, app_name)
        result = app_creator.init_app(app_name, project_dir)
        mock_exists.assert_called_with(app_path)
        self.assertNotIn(
            call(f"Creating the application in: {app_path}"),
            mock_print.call_args_list
        )
        mock_print.assert_called_with(
            f"An application named '{app_name}' already exists at {app_path}."
        )
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
