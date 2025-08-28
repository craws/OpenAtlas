import os
import shutil
from pathlib import Path
from typing import Any

from flask import url_for

from openatlas import app
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.models.export import current_date_for_filename
from tests.base import ImportTestCase


class ImportTest(ImportTestCase):

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

        logo_path = Path(app.root_path) / 'static' / 'images' / 'layout'
        with open(logo_path / 'logo.png', 'rb') as img:
            c.post(
                url_for('insert', class_='file'),
                data={
                    'name': 'OpenAtlas logo',
                    'file': img,
                    'creator': 'Max',
                    'license_holder': 'Moritz',
                    'public': True},
                follow_redirects=True)

        with app.test_request_context():
            app.preprocess_request()
            for entity in ApiEntity.get_by_cidoc_classes(['all']):
                match entity.name:
                    case 'Lord of the rings':
                        case_study = entity
                    case 'OpenAtlas logo':
                        openatlas_logo = entity
                    case 'File without license':
                        file_without_license = entity
                    case 'File without file':
                        file_no_file = entity
                    case 'Picture with a License':
                        file_with_license = entity
                    case 'File not public':
                        file_not_public = entity

        file_path = app.config['UPLOAD_PATH']
        openatlas_logo_path = file_path / f'{openatlas_logo.id}.png'
        file_without_license_path = (
                file_path / f'{file_without_license.id}.png')
        file_with_license_path = file_path / f'{file_with_license.id}.png'
        file_not_public_path = file_path / f'{file_not_public.id}.png'
        shutil.copy(openatlas_logo_path, file_without_license_path)
        shutil.copy(openatlas_logo_path, file_with_license_path)
        shutil.copy(openatlas_logo_path, file_not_public_path)

        app.config['ARCHE_METADATA'] = {
            'topCollection': 'test collection',
            'language': 'en',
            'depositor': 'Sauron',
            'acceptedDate': "2024-01-01",
            'curator': ['Frodo', 'Sam'],
            'principalInvestigator': ['Gandalf'],
            'hasMetadataCreator': ['Gimli'],
            'relatedDiscipline':
                ['https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601003'],
            'typeIds': [case_study.id],
            'excludeReferenceSystems': []}

        date_ = current_date_for_filename()
        collection_name = app.config["ARCHE_METADATA"]["topCollection"]
        filename = f'{date_}_{collection_name.replace(" ", "_")}.zip'

        rv = c.get(
            url_for('check_files', arche='arche'),
            follow_redirects=True)
        assert b'No license' in rv.data

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

        openatlas_logo_path.unlink()
        file_without_license_path.unlink()
        file_with_license_path.unlink()
        file_not_public_path.unlink()
