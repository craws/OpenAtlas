from pathlib import Path
from typing import Any

from flask import url_for

from openatlas import app
from tests.base import TestBaseCase


class ImportTest(TestBaseCase):

    def test_import(self) -> None:
        with app.app_context():

            rv: Any = self.app.get(url_for('import_project_insert'))
            assert b'name *' in rv.data

            rv = self.app.post(
                url_for('import_project_insert'),
                data={'name': 'Project X'})
            p_id = rv.location.split('/')[-1]

            rv = self.app.get(url_for('import_project_update', id_=p_id))
            assert b'name *' in rv.data

            rv = self.app.post(
                url_for('import_project_update', id_=p_id),
                data={'name': 'Project X', 'description': 'whoa!'},
                follow_redirects=True)
            assert b'whoa!' in rv.data

            rv = self.app.post(
                url_for('import_project_insert'),
                data={'name': 'Project X'})
            assert b'The name is already in use' in rv.data

            rv = self.app.get(url_for('import_index'))
            assert b'Project X' in rv.data

            rv = self.app.get(
                url_for('import_data', class_='person', project_id=p_id))
            assert b'file *' in rv.data

            static_path = Path(app.root_path) / 'static'
            with open(static_path / 'example.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file, 'duplicate': True},
                    follow_redirects=True)
            assert b'Vienna' in rv.data

            with open(static_path / 'example.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file, 'duplicate': True},
                    follow_redirects=True)
            assert b'IDs already in database' in rv.data

            with open(static_path / 'favicon.ico', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'File type not allowed' in rv.data

            test_path = Path(app.root_path).parent / 'tests'
            with open(test_path / 'invalid_1.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'missing name column' in rv.data

            with open(test_path / 'invalid_2.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'invalid columns: not_existing_column' in rv.data
            assert b'invalid type ids' in rv.data
            assert b'invalid coordinates' in rv.data
            assert b'empty names' in rv.data
            assert b'double IDs in import' in rv.data

            rv = self.app.get(url_for('import_project_view', id_=p_id))
            assert b'London' in rv.data

            rv = self.app.get(
                url_for('import_project_delete', id_=p_id),
                follow_redirects=True)
            assert b'Project deleted' in rv.data
