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
                    view='sql',
                    filename=f'{date_}_export.sql.7z')) as rv:
            assert b'7z' in rv.data

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
            url_for('delete_export', view='sql', filename='non_existing'),
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

        c.post(
            url_for('insert', class_='reference_system'),
            data={
                'name': 'Ring References',
                'website_url': 'https://ring_references.org',
                'resolver_url': 'https://ring_references.org',
                'classes': ['place', 'person']})

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
                    case 'Picture with a License':
                        file_with_license = entity
                    case 'File not public':
                        file_not_public = entity
                    case 'CC BY 4.0':
                        cc_by_license = entity
                    case 'Frodo':
                        actor = entity
                    case 'Ring References':
                        ext_ref_sys = entity
                    case 'exact match':
                        exact_match = entity
                    case 'https://viaf.org/viaf/95218067':
                        tolkien = entity

            openatlas_logo.link('P67', actor)
            openatlas_logo.link('P2', cc_by_license)
            openatlas_logo.link('P2', case_study)
            actor.link('P67', ext_ref_sys, 'Frodo', True, exact_match.id)
            tolkien.link('P67', ext_ref_sys, 'Tolkien', True, exact_match.id)

        file_path = app.config['UPLOAD_PATH']
        openatlas_logo_path = file_path / f'{openatlas_logo.id}.png'
        file_without_license_path = (
                file_path / f'{file_without_license.id}.png')
        file_with_license_path = file_path / f'{file_with_license.id}.png'
        file_not_public_path = file_path / f'{file_not_public.id}.jpg'
        shutil.copy(openatlas_logo_path, file_without_license_path)
        shutil.copy(openatlas_logo_path, file_with_license_path)
        shutil.copy(logo_path / '422.jpg', file_not_public_path)

        rv = c.get(
            url_for('arche_execute'),
            follow_redirects=True)
        assert b'Data was exported' in rv.data

        # Run ARCHE export again with typeIds and without GeoNames
        app.config['ARCHE_METADATA']['typeIds'] = [case_study.id]
        app.config['ARCHE_METADATA']['excludeReferenceSystems'] = ['GeoNames']
        rv = c.get(
            url_for('arche_execute'),
            follow_redirects=True)
        assert b'Data was exported' in rv.data

        date_ = current_date_for_filename()
        collection_name = app.config["ARCHE_METADATA"]["topCollection"]
        filename = f'{date_}_{collection_name.replace(" ", "_")}.zip'
        rv = c.get(url_for('download_export', view='arche', filename=filename))
        assert b'PK' in rv.data

        with c.get(
                url_for('delete_export', view='arche', filename=filename),
                follow_redirects=True) as rv_:
            if os.name == 'posix':
                assert b'File deleted' in rv_.data

        with c.get(
                url_for('check_files', arche='arche'),
                follow_redirects=True) as rv:
            assert b'No license' in rv.data

        assert b'Export RDF/NT' in c.get(url_for('export_rdf')).data

        rv = c.get(
            url_for('rdf_execute'),
            follow_redirects=True)
        assert b'Data was exported' in rv.data

        rv = c.get(
            url_for(
                'delete_export',
                view='rdf',
                filename=f'{date_}_export.nt'),
            follow_redirects=True)
        if os.name == 'posix':
            assert b'File deleted' in rv.data

        openatlas_logo_path.unlink()
        file_without_license_path.unlink()
        file_with_license_path.unlink()
        file_not_public_path.unlink()
