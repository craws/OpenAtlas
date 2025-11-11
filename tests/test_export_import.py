import os
from typing import Any

import pandas as pd
from flask import url_for

from openatlas import app
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.models.export import current_date_for_filename
from tests.base import ImportTestCase


class ImportTest(ImportTestCase):

    def test_import(self) -> None:
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

        c = self.client
        assert b'Export SQL' in c.get(url_for('export_sql')).data

        date_ = current_date_for_filename()
        rv: Any = c.get(
            url_for('export_execute', format_='sql'),
            follow_redirects=True)
        assert b'Data was exported' in rv.data

        with c.get(
                url_for(
                    'download_export',
                    view='sql',
                    filename=f'{date_}_export.sql.7z')) as rv:
            assert b'7z' in rv.data

        date_ = current_date_for_filename()
        rv = c.get(
            url_for('export_execute', format_='dump'),
            follow_redirects=True)
        assert b'Data was exported' in rv.data

        with c.get(
                url_for(
                    'download_export',
                    view='sql',
                    filename=f'{date_}_export.dump.7z')) as rv:
            assert b'7z' in rv.data

        rv = c.get(url_for('import_project_insert'))
        assert b'name *' in rv.data

        rv = c.post(url_for('import_project_insert'), data={'name': 'X-Files'})
        p_id = rv.location.split('/')[-1]

        rv = c.get(url_for('import_project_update', id_=p_id))
        assert b'name *' in rv.data

        rv = c.post(
            url_for('import_project_update', id_=p_id),
            data={'name': 'X-Files', 'description': 'whoa!'},
            follow_redirects=True)
        assert b'whoa!' in rv.data

        rv = c.post(url_for('import_project_insert'), data={'name': 'X-Files'})
        assert b'The name is already in use' in rv.data

        rv = c.get(url_for('import_index'))
        assert b'X-Files' in rv.data

        rv = c.get(url_for('import_data', class_='person', project_id=p_id))
        assert b'file *' in rv.data

        with open(self.test_path / 'bibliography.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='bibliography', project_id=p_id),
                data={'file': file, 'duplicate': True},
                follow_redirects=True)
        assert b'OpenAtlas 2024' in rv.data

        with open(self.static_path / 'example.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file, 'duplicate': True},
                follow_redirects=True)
        assert b'Vienna' in rv.data

        data_frame = pd.read_csv(
            self.test_path / 'import_type.csv',
            keep_default_na=False)
        data_frame.at[0, 'openatlas_parent_id'] = infrastructure.id
        data_frame.at[4, 'openatlas_parent_id'] = infrastructure.id
        data_frame.at[5, 'openatlas_parent_id'] = height.id
        data_frame.at[6, 'openatlas_parent_id'] = height.id
        data_frame.to_csv(
            self.test_path / 'example_type.csv',
            index=False)
        with open(self.test_path / 'example_type.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='type', project_id=p_id),
                data={'file': file},
                follow_redirects=True)
        assert b'Dam' in rv.data
        (self.test_path / 'example_type.csv').unlink()


        with open(self.static_path / 'example.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file, 'duplicate': True},
                follow_redirects=True)
        assert b'IDs already in database' in rv.data

        with open(self.test_path / 'import_type.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='type', project_id=p_id),
                data={'file': file, 'duplicate': True},
                follow_redirects=True)
        assert b'empty parend id' in rv.data

        with open(self.static_path / 'favicon.ico', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file},
                follow_redirects=True)
        assert b'File type not allowed' in rv.data

        with open(self.test_path / 'invalid_1.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='source', project_id=p_id),
                data={'file': file},
                follow_redirects=True)
        assert b'missing name column' in rv.data

        with open(self.test_path / 'invalid_2.csv', 'rb') as file:
            rv = c.post(
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
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file},
                follow_redirects=True)
        assert b'invalid coordinates' in rv.data
        assert b'invalid dates' in rv.data
        assert b'invalid value types' in rv.data
        assert b'invalid reference system value' in rv.data
        assert b'invalid origin reference id' in rv.data
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
            rv = c.post(
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
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file},
                follow_redirects=True)
        assert b'invalid parent id' in rv.data
        (self.test_path / 'invalid_3_modified.csv').unlink()

        data_frame = pd.read_csv(
            self.test_path / 'invalid_3.csv',
            keep_default_na=False)
        data_frame.at[4, 'openatlas_parent_id'] = place.id
        data_frame.to_csv(
            self.test_path / 'invalid_3_modified.csv',
            index=False)
        with open(self.test_path / 'invalid_3_modified.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file},
                follow_redirects=True)
        assert b'multiple parent IDs' in rv.data

        data_frame.at[3, 'openatlas_parent_id'] = 99999
        data_frame.to_csv(
            self.test_path / 'invalid_3_modified.csv',
            index=False)
        with open(self.test_path / 'invalid_3_modified.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file},
                follow_redirects=True)
        assert b'invalid parent id' in rv.data

        data_frame.at[3, 'openatlas_parent_id'] = place_type.id
        data_frame.to_csv(
            self.test_path / 'invalid_3_modified.csv',
            index=False)
        with open(self.test_path / 'invalid_3_modified.csv', 'rb') as file:
            rv = c.post(
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
        data_frame.at[0, 'administrative_unit_id'] = austria.id
        data_frame.at[0, 'historical_place_id'] = carantania.id
        data_frame.at[0, 'wkt'] = "POLYGON((16.1203 BLA, 16.606275))"
        data_frame.at[0, 'reference_ids'] = \
            f'{reference.id};IV {height.id};IV lit_1;55'
        data_frame.at[0, 'origin_reference_ids'] = 'Lit_1;IV type_3; all'
        data_frame.at[0, 'type_ids'] = ' '.join(
            map(str, [austria.id, reference.id, place.id]))
        data_frame.to_csv(self.test_path / 'example.csv', index=False)
        with open(self.test_path / 'example.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file, 'duplicate': True},
                follow_redirects=True)
        assert b'invalid reference id' in rv.data
        assert b'invalid origin reference id' in rv.data
        assert b'invalid type ids' in rv.data

        data_frame = pd.read_csv(
            self.test_path / 'example.csv',
            keep_default_na=False)
        data_frame.at[0, 'id'] = 'new_place_11'
        data_frame.at[1, 'id'] = 'new_place_22'
        data_frame.at[2, 'id'] = 'new_place_33'
        data_frame.at[0, 'administrative_unit_id'] = austria.id
        data_frame.at[0, 'historical_place_id'] = carantania.id
        type_ids = [
            boundary_mark.id,
            infrastructure.id,
            austria.id,
            place_type.id]
        data_frame.at[0, 'type_ids'] = ' '.join(map(str, type_ids))
        data_frame.at[0, 'value_types'] = f'{height.id};42'
        data_frame.to_csv(self.test_path / 'example.csv', index=False)
        with open(self.test_path / 'example.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file, 'duplicate': True},
                follow_redirects=True)
        assert b'single type duplicates' in rv.data

        with open(self.test_path / 'example.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='source', project_id=p_id),
                data={'file': file, 'duplicate': True},
                follow_redirects=True)
        assert b'invalid reference system class' in rv.data

        data_frame = pd.read_csv(
            self.test_path / 'example.csv',
            keep_default_na=False)
        data_frame.at[0, 'type_ids'] = ''
        data_frame.at[0, 'origin_type_ids'] = 'type_1'
        data_frame.to_csv(self.test_path / 'example.csv', index=False)
        with open(self.test_path / 'example.csv', 'rb') as file:
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file, 'duplicate': True},
                follow_redirects=True)
        assert b'Vienna' in rv.data

        (self.test_path / 'example.csv').unlink()

        data_frame = pd.read_csv(
            self.static_path / 'example_place_hierarchy.csv',
            keep_default_na=False)
        data_frame.at[7, 'openatlas_parent_id'] = place.id
        data_frame.at[7, 'origin_value_types'] = 'type_7;38'
        data_frame.at[2, 'origin_value_types'] = 'type_7;38'
        data_frame.at[6, 'origin_value_types'] = 'type_6 type_7;25'
        data_frame.at[5, 'origin_value_types'] = 'type_10'
        data_frame.at[4, 'origin_type_ids'] = 'type_10'
        data_frame.at[0, 'origin_type_ids'] = 'type_3'
        data_frame.to_csv(
            self.test_path / 'example_place_hierarchy.csv',
            index=False)
        with open(
                self.test_path / 'example_place_hierarchy.csv',
                'rb') as file:
            rv = c.post(
                url_for('import_data', class_='place', project_id=p_id),
                data={'file': file, 'duplicate': True},
                follow_redirects=True)
            assert b'Bone' in rv.data
            assert b'invalid type origin ids' in rv.data
            assert b'invalid origin value type ids' in rv.data
        (self.test_path / 'example_place_hierarchy.csv').unlink()

        rv = c.get(url_for('import_project_view', id_=p_id))
        assert b'London' in rv.data

        rv = c.get(
            url_for('import_project_delete', id_=p_id),
            follow_redirects=True)
        assert b'Project deleted' in rv.data

        rv = c.get(
            url_for(
                'delete_export',
                view='sql',
                filename=f'{date_}_export.sql.7z'),
            follow_redirects=True)
        if os.name == 'posix':
            assert b'File deleted' in rv.data

        rv = c.get(
            url_for(
                'delete_export',
                view='sql',
                filename=f'{date_}_export.dump.7z'),
            follow_redirects=True)
        if os.name == 'posix':
            assert b'File deleted' in rv.data

        rv = c.get(
            url_for(
                'delete_export',
                view='sql',
                filename='non_existing'),
            follow_redirects=True)
        assert b'An error occurred when trying to delete the f' in rv.data
