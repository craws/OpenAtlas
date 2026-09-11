import shutil
from pathlib import Path
from typing import Any

from flask import g, url_for
from rdflib import Graph, URIRef

from openatlas import app
from openatlas.api.external.arche import add_licenses
from openatlas.api.external.arche_class import ArcheFileMetadata
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.models.entity import Entity
from openatlas.models.export import (
    _get_license_url_mapping,
    current_date_for_filename,
    get_arche_file_metadata,
    get_arche_file_turtle_graph)
from tests.base import ImportTestCase, get_hierarchy, insert


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
        assert b'File deleted' in rv.data

        rv = c.get(
            url_for(
                'delete_export',
                view='sql',
                filename=f'{date_}_export.dump.7z'),
            follow_redirects=True)
        assert b'File deleted' in rv.data

        rv = c.get(
            url_for('delete_export', view='sql', filename='non_existing'),
            follow_redirects=True)
        assert b'An error occurred when trying to delete the f' in rv.data

        with c.get(url_for('export_arche')) as rv:
            assert b'Export ARCHE' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            rights_holder_ids = [rh.id for rh in g.rights_holder]
        logo_path = Path(app.root_path) / 'static' / 'images' / 'layout'
        public_type = get_hierarchy('Public sharing allowed')
        with open(logo_path / 'logo.png', 'rb') as img:
            c.post(
                url_for('insert', class_='file'),
                data={
                    'name': 'OpenAtlas logo',
                    'file': img,
                    'creator': f'{rights_holder_ids}',
                    'license_holder': f'{rights_holder_ids}',
                    str(public_type.id): public_type.subs[0]},
                follow_redirects=True)

        c.post(
            url_for('insert', class_='reference_system'),
            data={
                'name': 'Ring References',
                'website_url': 'https://ring_references.org',
                'resolver_url': 'https://ring_references.org',
                'classes': ['place', 'person'],
                'api': ''})

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

        with c.get(url_for('arche_execute'), follow_redirects=True) as rv:
            assert b'Data was exported' in rv.data

        # Run ARCHE export again with typeIds and without GeoNames
        app.config['ARCHE_METADATA']['typeIds'] = [case_study.id]
        app.config['ARCHE_METADATA']['excludeReferenceSystems'] = ['GeoNames']
        with c.get(url_for('arche_execute'), follow_redirects=True) as rv:
            assert b'Data was exported' in rv.data

        date_ = current_date_for_filename()
        collection_name = app.config["ARCHE_METADATA"]["topCollection"]
        filename = f'{date_}_{collection_name.replace(" ", "_")}.zip'
        with c.get(
                url_for(
                    'download_export',
                    view='arche',
                    filename=filename)) as rv:
            assert b'PK' in rv.data

        with c.get(
                url_for('delete_export', view='arche', filename=filename),
                follow_redirects=True) as rv_:
            assert b'File deleted' in rv_.data

        with c.get(
                url_for('check_files', arche='arche'),
                follow_redirects=True) as rv_:
            assert b'No license' in rv_.data

        assert b'Export RDF/NT' in c.get(url_for('export_rdf')).data

        with c.get(url_for('rdf_execute'), follow_redirects=True) as rv_:
            assert b'Data was exported' in rv_.data

        with c.get(
                url_for(
                    'delete_export',
                    view='rdf',
                    filename=f'{date_}_export.nt'),
                follow_redirects=True) as rv_:
            assert b'File deleted' in rv_.data

        openatlas_logo_path.unlink()
        file_without_license_path.unlink()
        file_with_license_path.unlink()
        file_not_public_path.unlink()

    def test_arche_license_multiple_urls(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            rights_holder_ids = [rh.id for rh in g.rights_holder]
        logo_path = Path(app.root_path) / 'static' / 'images' / 'layout'
        public_type = get_hierarchy('Public sharing allowed')
        with open(logo_path / 'logo.png', 'rb') as img:
            rv = c.post(
                url_for('insert', class_='file'),
                data={
                    'name': 'OpenAtlas logo multi',
                    'file': img,
                    'creator': f'{rights_holder_ids}',
                    'license_holder': f'{rights_holder_ids}',
                    str(public_type.id): public_type.subs[0]})
        file_id = int(rv.location.split('/')[-1])

        with app.test_request_context():
            app.preprocess_request()
            mapping = _get_license_url_mapping()
            assert isinstance(mapping, dict)
            for urls in mapping.values():
                assert isinstance(urls, list)

            cc_by_license = next(
                type_ for type_ in g.types.values() if type_.name == 'CC BY 4.0')
            initial_count = len(mapping.get(cc_by_license.id, []))

            new_url = 'https://creativecommons.org/licenses/by/4.0/'
            ref_entity = insert('external_reference', new_url)
            ref_entity.link('P67', cc_by_license)

            updated_mapping = _get_license_url_mapping()
            assert cc_by_license.id in updated_mapping
            assert len(updated_mapping[cc_by_license.id]) == initial_count + 1
            assert new_url in updated_mapping[cc_by_license.id]

            # Duplicate link should not add duplicate URL
            ref_entity.link('P67', cc_by_license)
            duplicate_mapping = _get_license_url_mapping()
            assert len(duplicate_mapping[cc_by_license.id]) == initial_count + 1

            file_entity = Entity.get_by_id(file_id)
            file_entity.link('P2', cc_by_license)
            file_entity = Entity.get_by_id(file_id, types=True)

            metadata_list = get_arche_file_metadata(
                [file_entity],
                None,
                'TopCollection')
            assert len(metadata_list) == 1
            assert isinstance(metadata_list[0].license, list)
            assert len(metadata_list[0].license) >= 2
            assert new_url in metadata_list[0].license

            turtle = get_arche_file_turtle_graph(
                [file_entity],
                None,
                'TopCollection')
            for lic_url in metadata_list[0].license:
                assert lic_url in turtle

            # Test construct with single string
            meta_str = ArcheFileMetadata.construct(
                file_entity,
                'type_name',
                [],
                [],
                new_url)
            assert meta_str.license == [new_url]

            # Test add_licenses with None
            test_graph = Graph()
            add_licenses(test_graph, URIRef('https://example.org/res'), None)
            assert len(test_graph) == 0

        file_path = app.config['UPLOAD_PATH'] / f'{file_entity.id}.png'
        if file_path.exists():
            file_path.unlink()
