import os
from typing import Any

import pandas as pd
from flask import url_for

from openatlas import app
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.models.export import current_date_for_filename
from tests.base import ExportImportTestCase


class ExportImportTest(ExportImportTestCase):

    def test_export(self) -> None:
        with app.app_context():
            assert b'Export SQL' in self.app.get(url_for('export_sql')).data

            date_ = current_date_for_filename()
            rv: Any = self.app.get(
                url_for('export_execute', format_='sql'),
                follow_redirects=True)
            assert b'Data was exported' in rv.data

            rv = self.app.get(
                url_for('download_sql', filename=f'{date_}_export.sql.7z'))
            assert b'7z' in rv.data

            date_ = current_date_for_filename()
            rv = self.app.get(
                url_for('export_execute', format_='dump'),
                follow_redirects=True)
            assert b'Data was exported' in rv.data

            rv = self.app.get(
                url_for('download_sql', filename=f'{date_}_export.dump.7z'))
            assert b'7z' in rv.data

            assert b'Warning' in self.app.get(url_for('sql_index')).data
            assert b'execute' in self.app.get(url_for('sql_execute')).data

            rv = self.app.post(
                url_for('sql_execute'),
                data={'statement': 'SELECT * FROM web.user;'})
            assert b'Alice' in rv.data

            rv = self.app.post(url_for('sql_execute'), data={'statement': 'e'})
            assert b'syntax error' in rv.data

            rv = self.app.get(url_for('import_project_insert'))
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

            assert b'Project X' in self.app.get(url_for('import_index')).data

            rv = self.app.get(
                url_for('import_data', class_='person', project_id=p_id))
            assert b'file *' in rv.data

            with open(self.static_path / 'example.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file, 'duplicate': True},
                    follow_redirects=True)
            assert b'Vienna' in rv.data

            with open(self.static_path / 'example.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file, 'duplicate': True},
                    follow_redirects=True)
            assert b'IDs already in database' in rv.data

            with open(self.static_path / 'favicon.ico', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'File type not allowed' in rv.data

            with open(self.test_path / 'invalid_1.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='source', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'missing name column' in rv.data

            with open(self.test_path / 'invalid_2.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'invalid columns: not_existing_column' in rv.data
            assert b'invalid administrative units' in rv.data
            assert b'invalid type ids' in rv.data
            assert b'invalid value type ids' in rv.data
            assert b'invalid value type values' in rv.data
            assert b'invalid reference system' in rv.data
            assert b'invalid reference id' in rv.data
            assert b'empty names' in rv.data
            assert b'double IDs in import' in rv.data

            with open(self.test_path / 'invalid_3.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'invalid coordinates' in rv.data
            assert b'invalid value types' in rv.data
            assert b'invalid reference system value' in rv.data
            assert b'invalid match type' in rv.data
            assert b'invalid openatlas class' in rv.data
            assert b'invalid parent class' in rv.data
            assert b'empty ids' in rv.data

            data_frame = pd.read_csv(
                self.test_path / 'invalid_3.csv',
                keep_default_na=False)
            data_frame.at[0, 'openatlas_class'] = 'place'
            data_frame.to_csv(
                self.test_path / 'invalid_3_modified.csv',
                index=False)
            with open(self.test_path / 'invalid_3_modified.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'invalid parent class' in rv.data

            data_frame.at[4, 'parent_id'] = 'strati_1'
            data_frame.at[4, 'openatlas_class'] = 'human remains'
            data_frame.to_csv(
                self.test_path / 'invalid_3_modified.csv',
                index=False)
            with open(self.test_path / 'invalid_3_modified.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'invalid parent id' in rv.data
            (self.test_path / 'invalid_3_modified.csv').unlink()

    def test_export2(self) -> None:
        with app.app_context():
            rv = self.app.post(
                url_for('import_project_insert'),
                data={'name': 'Project X'})
            p_id = rv.location.split('/')[-1]
            with app.test_request_context():
                app.preprocess_request()
                for entity in ApiEntity.get_by_cidoc_classes(['all']):
                    match entity.name:
                        case 'Boundary Mark':
                            boundary_mark = entity
                        case 'Infrastructure':
                            infrastructure = entity
                        case 'Austria':
                            austria = entity
                        case 'Height':
                            height = entity
                        case 'Carantania':
                            carantania = entity
                        case 'Place':
                            place_type = entity
                        case 'https://lotr.fandom.com/':
                            reference = entity
                        case 'Shire':
                            place = entity

            data_frame = pd.read_csv(
                self.test_path / 'invalid_3.csv',
                keep_default_na=False)
            data_frame.at[4, 'openatlas_parent_id'] = place.id
            data_frame.to_csv(
                self.test_path / 'invalid_3_modified.csv',
                index=False)
            with open(self.test_path / 'invalid_3_modified.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'multiple parent IDs' in rv.data

            data_frame.at[3, 'openatlas_parent_id'] = 99999
            data_frame.to_csv(
                self.test_path / 'invalid_3_modified.csv',
                index=False)
            with open(self.test_path / 'invalid_3_modified.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'invalid parent id' in rv.data

            data_frame.at[3, 'openatlas_parent_id'] = place_type.id
            data_frame.to_csv(
                self.test_path / 'invalid_3_modified.csv',
                index=False)
            with open(self.test_path / 'invalid_3_modified.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file},
                    follow_redirects=True)
            assert b'invalid parent class' in rv.data

            (self.test_path / 'invalid_3_modified.csv').unlink()

            data_frame = pd.read_csv(
                self.static_path / 'example.csv',
                keep_default_na=False)
            data_frame.at[0, 'id'] = 'new_place_1'
            data_frame.at[1, 'id'] = 'new_place_2'
            data_frame.at[2, 'id'] = 'new_place_3'
            data_frame.at[0, 'administrative_unit'] = austria.id
            data_frame.at[0, 'historical_place'] = carantania.id
            type_ids = [
                boundary_mark.id,
                infrastructure.id,
                austria.id,
                place_type.id]
            data_frame.at[0, 'type_ids'] = ' '.join(map(str, type_ids))
            data_frame.at[0, 'value_types'] = f'{height.id};42'
            data_frame.at[0, 'references'] = f'{reference.id};IV'
            data_frame.at[0, 'wkt'] = "POLYGON((16.1203 BLA, 16.606275))"
            data_frame.to_csv(self.test_path / 'example.csv', index=False)
            with open(self.test_path / 'example.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file, 'duplicate': True},
                    follow_redirects=True)
            assert b'single type duplicates' in rv.data
            assert b'Vienna' in rv.data

            with open(self.test_path / 'example.csv', 'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='source', project_id=p_id),
                    data={'file': file, 'duplicate': True},
                    follow_redirects=True)
            assert b'invalid reference system class' in rv.data
            (self.test_path / 'example.csv').unlink()

            data_frame = pd.read_csv(
                self.static_path / 'example_place_hierarchy.csv',
                keep_default_na=False)
            data_frame.at[7, 'openatlas_parent_id'] = place.id
            data_frame.to_csv(
                self.test_path / 'example_place_hierarchy.csv',
                index=False)
            with open(
                    self.test_path / 'example_place_hierarchy.csv',
                    'rb') as file:
                rv = self.app.post(
                    url_for('import_data', class_='place', project_id=p_id),
                    data={'file': file, 'duplicate': True},
                    follow_redirects=True)
                assert b'Bone' in rv.data
            (self.test_path / 'example_place_hierarchy.csv').unlink()

            rv = self.app.get(url_for('import_project_view', id_=p_id))
            assert b'London' in rv.data

            rv = self.app.get(
                url_for('import_project_delete', id_=p_id),
                follow_redirects=True)
            assert b'Project deleted' in rv.data

            date_ = current_date_for_filename()
            rv = self.app.get(
                url_for('delete_export', filename=f'{date_}_export.sql.7z'),
                follow_redirects=True)
            if os.name == 'posix':
                assert b'File deleted' in rv.data

            rv = self.app.get(
                url_for('delete_export', filename=f'{date_}_export.dump.7z'),
                follow_redirects=True)
            if os.name == 'posix':
                assert b'File deleted' in rv.data

            rv = self.app.get(
                url_for('delete_export', filename='non_existing'),
                follow_redirects=True)
            assert b'An error occurred when trying to delete the f' in rv.data
