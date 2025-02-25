import os

from flask import url_for

from openatlas.models.export import current_date_for_filename
from tests.base import TestBaseCase


class ImportTest(TestBaseCase):

    def test_export(self) -> None:
        c = self.client
        assert b'Export SQL' in c.get(url_for('export_sql')).data

        date_ = current_date_for_filename()
        rv = c.get(
            url_for('export_execute', format_='sql'),
            follow_redirects=True)
        assert b'Data was exported' in rv.data

        rv = c.get(url_for('download_sql', filename=f'{date_}_export.sql.7z'))
        assert b'7z' in rv.data

        rv = c.get(
            url_for('export_execute', format_='dump'),
            follow_redirects=True)
        assert b'Data was exported' in rv.data

        rv = c.get(url_for('download_sql', filename=f'{date_}_export.dump.7z'))
        assert b'7z' in rv.data

        assert b'Warning' in c.get(url_for('sql_index')).data
        assert b'execute' in c.get(url_for('sql_execute')).data

        rv = c.post(
            url_for('sql_execute'),
            data={'statement': 'SELECT * FROM web.user;'})
        assert b'Alice' in rv.data

        rv = c.post(url_for('sql_execute'), data={'statement': 'e'})
        assert b'syntax error' in rv.data

        rv = c.get(
            url_for('delete_export', filename=f'{date_}_export.sql.7z'),
            follow_redirects=True)
        if os.name == 'posix':
            assert b'File deleted' in rv.data

        rv = c.get(
            url_for('delete_export', filename=f'{date_}_export.dump.7z'),
            follow_redirects=True)
        if os.name == 'posix':
            assert b'File deleted' in rv.data

        rv = c.get(
            url_for('delete_export', filename='non_existing'),
            follow_redirects=True)
        assert b'An error occurred when trying to delete the f' in rv.data
