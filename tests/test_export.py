import os
from typing import Any

from flask import url_for

from openatlas import app
from openatlas.models.export import current_date_for_filename
from tests.base import TestBaseCase


class ImportTest(TestBaseCase):

    def test_export(self) -> None:
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
                    filename=f'{date_}_export.sql.7z')) as rv:
            assert b'7z' in rv.data

        rv = c.get(
            url_for('export_execute', format_='dump'),
            follow_redirects=True)
        assert b'Data was exported' in rv.data

        with c.get(
                url_for(
                    'download_export',
                    filename=f'{date_}_export.dump.7z')) as rv:
            assert b'7z' in rv.data

        rv = c.get(
            url_for(
                'delete_export',
                view='export_sql',
                filename=f'{date_}_export.sql.7z'),
            follow_redirects=True)
        if os.name == 'posix':
            assert b'File deleted' in rv.data

        rv = c.get(
            url_for(
                'delete_export',
                view='export_sql',
                filename=f'{date_}_export.dump.7z'),
            follow_redirects=True)
        if os.name == 'posix':
            assert b'File deleted' in rv.data

        rv = c.get(
            url_for(
                'delete_export',
                view='export_sql',
                filename='non_existing'),
            follow_redirects=True)
        assert b'An error occurred when trying to delete the f' in rv.data

        assert b'Export ARCHE' in c.get(url_for('export_arche')).data

        app.config['ARCHE_METADATA'] = {
            'topCollection': 'test collection',
            'language': 'en',
            'depositor': 'Sauron',
            'acceptedDate': "2024-01-01",
            'curator': ['Frodo', 'Sam'],
            'principalInvestigator': ['Gandalf'],
            'relatedDiscipline':
                ['https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601003'],
            'typeIds': []}

        date_ = current_date_for_filename()
        collection_name = app.config["ARCHE_METADATA"]["topCollection"]
        filename = f'{date_}_{collection_name.replace(" ", "_")}.zip'

        rv = c.get(
            url_for('arche_execute'),
            follow_redirects=True)
        assert b'Data was exported' in rv.data

        rv = c.get(url_for('download_export', filename=filename))
        assert b'PK' in rv.data

        rv = c.get(
            url_for(
                'delete_export',
                view='export_arche',
                filename=filename),
            follow_redirects=True)
        if os.name == 'posix':
            assert b'File deleted' in rv.data
