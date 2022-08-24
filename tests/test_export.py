import os

from flask import url_for

from openatlas import app
from openatlas.models.export import current_date_for_filename
from tests.base import TestBaseCase


class ExportTest(TestBaseCase):

    def test_export(self) -> None:
        with app.app_context():
            rv = self.app.get(url_for('export_sql'))
            assert b'Export SQL' in rv.data

            date_string = current_date_for_filename()  # Less error before
            rv = self.app.post(url_for('export_sql'), follow_redirects=True)
            assert b'Data was exported as SQL' in rv.data

            self.app.get(
                url_for('download_sql', filename=f'{date_string}_dump.sql'))
            rv = self.app.get(url_for('sql_index'))
            assert b'Warning' in rv.data

            rv = self.app.get(url_for('sql_execute'))
            assert b'Execute' in rv.data

            rv = self.app.post(
                url_for('sql_execute'),
                data={'statement': 'SELECT * FROM web.user'})
            assert b'Alice' in rv.data

            rv = self.app.post(
                url_for('sql_execute'),
                data={'statement': 'SELECT * FROM fail;'})
            assert b'relation "fail" does not exist' in rv.data

            rv = self.app.get(
                url_for(
                    'delete_export',
                    type_='sql',
                    filename=f'{date_string}_dump.sql.7z'),
                follow_redirects=True)
            if os.name == 'posix':
                assert b'File deleted' in rv.data

            rv = self.app.get(
                url_for('delete_export', type_='sql', filename='non_existing'),
                follow_redirects=True)
            assert b'An error occurred when trying to delete the f' in rv.data

            rv = self.app.get(url_for('export_csv'))
            assert b'Export CSV' in rv.data

            date_string = current_date_for_filename()
            rv = self.app.post(
                url_for('export_csv'),
                follow_redirects=True,
                data={
                    'zip': True,
                    'cidoc_class': True,
                    'cidoc_class_inheritance': True,
                    'entity': True,
                    'link': True,
                    'property': True,
                    'property_inheritance': True,
                    'gis': True,
                    'gis_format': 'wkt'})
            assert b'Data was exported as CSV' in rv.data

            data = {
                'class': True,
                'timestamps': True,
                'gis': True,
                'gis_format': 'postgis'}
            rv = self.app.post(
                url_for('export_csv'),
                follow_redirects=True,
                data=data)
            assert b'Data was exported as CSV' in rv.data

            data['gis'] = True
            data['gis_format'] = 'coordinates'
            rv = self.app.post(
                url_for('export_csv'),
                follow_redirects=True,
                data=data)
            assert b'Data was exported as CSV' in rv.data

            self.app.get(
                url_for('download_csv', filename=f'{date_string}_csv.zip'))
            rv = self.app.get(
                url_for(
                    'delete_export',
                    type_='csv',
                    filename=f'{date_string}_csv.zip'),
                follow_redirects=True)
            assert b'File deleted' in rv.data

            rv = self.app.get(
                url_for('delete_export', type_='csv', filename='non_existing'),
                follow_redirects=True)
            assert b'An error occurred when trying to delete' in rv.data
