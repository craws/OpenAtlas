import os
from flask import url_for

from openatlas import app
from openatlas.models.date import DateMapper
from tests.base import TestBaseCase


class ExportTest(TestBaseCase):

    def test_export(self) -> None:
        with app.app_context():
            self.login()

            # SQL export
            rv = self.app.get(url_for('export_sql'))
            assert b'Export SQL' in rv.data
            rv = self.app.post(url_for('export_sql'), follow_redirects=True)
            assert b'Data was exported as SQL' in rv.data
            date_string = DateMapper.current_date_for_filename()
            self.app.get(url_for('download_sql', filename=date_string + '_dump.sql'))

            # SQL execute (located here because a recent dump is needed to work
            rv = self.app.get(url_for('sql_index'))
            assert b'Warning' in rv.data
            rv = self.app.get(url_for('sql_execute'))
            assert b'Execute' in rv.data
            rv = self.app.post(url_for('sql_execute'), data={'statement': 'SELECT * FROM web.user'})
            assert b'Alice' in rv.data
            rv = self.app.post(url_for('sql_execute'), data={'statement': 'SELECT * FROM fail;'})
            if os.name == 'posix':
                assert b'relation "fail" does not exist' in rv.data

            # Delete SQL dump
            rv = self.app.get(url_for('delete_sql', filename=date_string + '_dump.sql'),
                              follow_redirects=True)
            if os.name == 'posix':
                assert b'File deleted' in rv.data

            # CSV export
            rv = self.app.get(url_for('export_csv'))
            assert b'Export CSV' in rv.data
            rv = self.app.post(url_for('export_csv'), follow_redirects=True,
                               data={'zip': True, 'model_class': True,
                                     'gis_point': True, 'gis_format': 'wkt'})
            assert b'Data was exported as CSV' in rv.data
            rv = self.app.post(url_for('export_csv'), follow_redirects=True,
                               data={'model_class': True, 'timestamps': True,
                                     'gis_polygon': True, 'gis_format': 'postgis'})
            assert b'Data was exported as CSV' in rv.data
            rv = self.app.post(url_for('export_csv'), follow_redirects=True,
                               data={'model_class': True, 'timestamps': True, 'gis_point': True,
                                     'gis_polygon': True, 'gis_format': 'coordinates'})
            assert b'Data was exported as CSV' in rv.data
            date_string = DateMapper.current_date_for_filename()
            self.app.get(url_for('download_csv', filename=date_string + '_csv.zip'))
            rv = self.app.get(url_for('delete_csv', filename=date_string + '_csv.zip'),
                              follow_redirects=True)
            assert b'File deleted' in rv.data
