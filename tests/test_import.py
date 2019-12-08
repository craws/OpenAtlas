import os
from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from tests.base import TestBaseCase


class ExportTest(TestBaseCase):

    def test_export(self) -> None:
        with app.app_context():
            self.login()
            # Projects
            rv = self.app.get(url_for('import_project_insert'))
            assert b'Name *' in rv.data
            rv = self.app.post(url_for('import_project_insert'), data={'name': 'Project Import'})
            project_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('import_project_update', id_=project_id))
            assert b'Name *' in rv.data
            rv = self.app.post(url_for('import_project_update', id_=project_id),
                               follow_redirects=True, data={'name': 'Yup', 'description': 'whoa!'})
            assert b'whoa!' in rv.data
            rv = self.app.post(url_for('import_project_insert'), data={'name': 'Yup'},
                               follow_redirects=True)
            assert b'The name is already in use.' in rv.data
            rv = self.app.get(url_for('import_index'))
            assert b'Yup' in rv.data

            # Import data
            rv = self.app.get(url_for('import_data', class_code='E21', project_id=project_id))
            assert b'File *' in rv.data
            path = app.config['ROOT_PATH'].joinpath('static', 'import', 'example.csv')
            with open(path, 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_code='E18', project_id=project_id),
                    data={'file': file, 'duplicate': True}, follow_redirects=True)
            assert b'Vienna' in rv.data
            path = app.config['ROOT_PATH'].joinpath('static', 'import', 'example.xlsx')
            with open(path, 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_code='E18', project_id=project_id),
                    data={'file': file, 'duplicate': True}, follow_redirects=True)
            if os.name == 'posix':
                assert b'IDs already in database' in rv.data
            with open(app.config['ROOT_PATH'].joinpath('static', 'favicon.ico'), 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_code='E18', project_id=project_id),
                    data={'file': file}, follow_redirects=True)
            assert b'File type not allowed' in rv.data
            rv = self.app.get(url_for('import_project_view', id_=project_id))
            assert b'London' in rv.data

            # View an imported entity
            with app.test_request_context():
                app.preprocess_request()
                place_id = EntityMapper.get_by_system_type('place')[0].id
            rv = self.app.get(url_for('entity_view', id_=place_id))
            assert b'Yup' in rv.data

            rv = self.app.get(url_for('import_project_delete', id_=project_id),
                              follow_redirects=True)
            assert b'Project deleted' in rv.data
