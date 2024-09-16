from pathlib import Path
from typing import Any

from flask import g, url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, get_hierarchy, insert


class FileTest(TestBaseCase):

    def test_file(self) -> None:

        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()
                place = insert('place', 'File keeper')
                reference = insert('edition', 'Ancient Books')
                license_type = get_hierarchy('License')

            logo = Path(
                app.root_path) / 'static' / 'images' / 'layout' / 'logo.png'

            with open(logo, 'rb') as img_1, open(logo, 'rb') as img_2:
                rv: Any = self.app.post(
                    url_for('insert', class_='file', origin_id=place.id),
                    data={
                        'name': 'OpenAtlas logo',
                        'public': True,
                        'file': [img_1, img_2]},
                    follow_redirects=True)
            assert b'An entry has been created' in rv.data

            with app.test_request_context():
                app.preprocess_request()
                files = Entity.get_by_class('file')
                file_without_creator_id = files[0].id

            rv = self.app.get(url_for('view', id_=file_without_creator_id))
            assert b'but license is missing ' in rv.data

            with open(logo, 'rb') as img:
                rv = self.app.post(
                    url_for('insert', class_='file', origin_id=reference.id),
                    data={
                        'name': 'OpenAtlas logo',
                        'file': img,
                        'public': True,
                        str(license_type.id): license_type.subs[0]},
                    follow_redirects=True)
            assert b'An entry has been created' in rv.data

            with open(logo, 'rb') as img:
                data = {
                    'name': 'IIIF File',
                    'file': img,
                    'creator': 'Max',
                    'license_holder': 'Moritz',
                    'public': True}
                rv = self.app.post(url_for('insert', class_='file'), data=data)
                iiif_id = rv.location.split('/')[-1]

            for type_ in g.types.values():
                if type_.name == 'Public domain':
                    license_ = type_
                    break

            with app.test_request_context():
                app.preprocess_request()
                files = Entity.get_by_class('file')
                iiif_file = Entity.get_by_id(iiif_id)
                iiif_file.link('P2', license_)

            rv = self.app.get(url_for('update', id_=iiif_id))
            assert b'License' in rv.data

            rv = self.app.get(
                url_for('delete_iiif_file', id_=iiif_id),
                follow_redirects=True)
            assert b'IIIF file deleted' in rv.data

            rv = self.app.get(
                url_for('convert_iiif_files'),
                follow_redirects=True)
            assert b'All image files are converted' in rv.data

            rv = self.app.get(
                url_for('delete_iiif_files'), follow_redirects=True)
            assert b'IIIF files are deleted' in rv.data

            filename = f'{iiif_id}.png'
            with self.app.get(url_for('display_logo', filename=filename)):
                pass

            with self.app.get(url_for('download', filename=filename)):
                pass

            rv = self.app.get(url_for('logo'), data={'file': iiif_id})
            assert b'OpenAtlas logo' in rv.data

            rv = self.app.get(
                url_for('logo', id_=iiif_id),
                follow_redirects=True)
            assert b'remove custom logo' in rv.data

            rv = self.app.get(
                url_for('logo_remove', action='remove_logo'),
                follow_redirects=True)
            assert b'Logo' in rv.data

            with open(Path(app.root_path) / 'views' / 'index.py', 'rb') \
                    as invalid_file:
                rv = self.app.post(
                    url_for('insert', class_='file', origin_id=place.id),
                    data={'name': 'Invalid file', 'file': invalid_file},
                    follow_redirects=True)
            assert b'File type not allowed' in rv.data

            rv = self.app.get(
                url_for('remove_profile_image', entity_id=place.id),
                follow_redirects=True)
            assert b'Unset' not in rv.data

            rv = self.app.post(
                url_for('reference_add', id_=reference.id, view='file'),
                data={'file': iiif_id, 'page': '777'},
                follow_redirects=True)
            assert b'777' in rv.data

            rv = self.app.post(
                url_for('update', id_=iiif_id),
                data={'name': 'Updated file'},
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            rv = self.app.get(url_for('file_add', id_=iiif_id, view='actor'))
            assert b'link actor' in rv.data

            rv = self.app.post(
                url_for('file_add', id_=iiif_id, view='actor'),
                data={'checkbox_values': [place.id]},
                follow_redirects=True)
            assert b'File keeper' in rv.data

            rv = self.app.get(url_for('update', id_=place.id))
            assert b'File keeper' in rv.data

            rv = self.app.post(
                url_for('entity_add_file', id_=get_hierarchy('Sex').subs[0]),
                data={'checkbox_values': str([iiif_id])},
                follow_redirects=True)
            assert b'Updated file' in rv.data

            rv = self.app.get(url_for('view', id_=iiif_id))
            assert b'enable IIIF view' in rv.data

            rv = self.app.get(
                url_for('make_iiif_available', id_=iiif_id),
                follow_redirects=True)
            assert b'IIIF converted' in rv.data

            rv = self.app.get(url_for('view', id_=iiif_id))
            assert b'View in IIIF' in rv.data

            rv = self.app.get(
                url_for('view', id_=place.id, _anchor="tab-file"))
            assert b'view all IIIF images' in rv.data

            with app.test_request_context():
                app.preprocess_request()
                license_url = insert("external_reference", "http://this.url/")
                license_url.link('P67', license_)
                iiif_file = Entity.get_by_id(iiif_id)
                iiif_file.link('P2', license_)

            rv = self.app.get(
                url_for(
                    'api.iiif_manifest',
                    id_=iiif_id,
                    version=g.settings['iiif_version']))
            rv = rv.get_json()
            assert bool(rv['label'] == 'Updated file')

            rv = self.app.get(url_for('api.iiif_sequence', id_=iiif_id))
            assert bool(str(iiif_id) in rv.get_json()['@id'])

            rv = self.app.get(url_for('api.iiif_image', id_=iiif_id))
            assert bool(str(iiif_id) in rv.get_json()['@id'])

            rv = self.app.get(url_for('api.iiif_canvas', id_=iiif_id))
            assert bool(str(iiif_id) in rv.get_json()['@id'])

            with app.test_request_context():
                app.preprocess_request()
                files[0].link('P2', g.types[get_hierarchy('License').subs[0]])

            rv = self.app.get(url_for('api.licensed_file_overview'))
            assert bool(len(rv.get_json().keys()) == 4)
            rv = self.app.get(
                url_for('api.licensed_file_overview', download=True))
            assert bool(len(rv.get_json().keys()) == 4)
            rv = self.app.get(
                url_for('api.licensed_file_overview', file_id=iiif_id))
            assert bool(len(rv.get_json().keys()) == 1)

            rv = self.app.get(url_for('view_iiif', id_=place.id))
            assert b'Mirador' in rv.data

            rv = self.app.get(url_for('view', id_=place.id))
            assert b'/full/!100,100/0/default.jpg' in rv.data

            rv = self.app.get(url_for('view', id_=place.id))
            assert b'Logo' in rv.data

            rv = self.app.get(url_for('annotation_insert', id_=iiif_id))
            assert b'annotate' in rv.data

            rv = self.app.post(
                url_for('annotation_insert', id_=iiif_id),
                data={
                    'coordinate': '1.5,1.6,1.4,9.6,8.6,9.6,8.6,1.6',
                    'text': 'An interesting annotation',
                    'entity': place.id},
                follow_redirects=True)
            assert b'An interesting annotation' in rv.data

            rv = self.app.get(url_for(
                'view_iiif',
                id_=iiif_id))
            assert b'Mirador' in rv.data

            rv = self.app.get(
                url_for(
                    'api.iiif_manifest',
                    id_=iiif_id,
                    version=g.settings['iiif_version'],
                    url="https://openatlas.eu"))
            assert b'openatlas.eu' in rv.data

            rv = self.app.get(
                url_for(
                    'api.iiif_manifest',
                    id_=iiif_id,
                    version=g.settings['iiif_version'],
                    url="https://openatlaseu"))
            assert b'URL not valid' in rv.data

            rv = self.app.get(url_for('annotation_update', id_=1))
            assert b'An interesting annotation' in rv.data

            rv = self.app.get(url_for(
                'api.iiif_annotation_list',
                image_id=iiif_id,
                url="https://openatlas.eu"))
            json = rv.get_json()
            assert bool(str(iiif_id) in json['@id'])

            annotation_id = json['resources'][0]['@id'].rsplit('/', 1)[-1]
            rv = self.app.get(url_for(
                'api.iiif_annotation',
                annotation_id=annotation_id.replace('.json', '')))
            assert bool(annotation_id in rv.get_json()['@id'])

            with app.test_request_context():
                app.preprocess_request()
                iiif_file.delete_links(['P67'])

            rv = self.app.get(url_for('orphans'))
            assert b'File keeper' in rv.data

            rv = self.app.get(url_for(
                'admin_annotation_relink',
                image_id=iiif_id,
                entity_id=place.id),
                follow_redirects=True)
            assert b'Entities relinked' in rv.data

            with app.test_request_context():
                app.preprocess_request()
                iiif_file.delete_links(['P67'])

            rv = self.app.get(url_for(
                'admin_annotation_remove_entity',
                annotation_id=1,
                entity_id=place.id),
                follow_redirects=True)
            assert b'Entity removed from annotation' in rv.data

            rv = self.app.post(
                url_for('annotation_update', id_=1),
                data={'text': 'A boring annotation'},
                follow_redirects=True)
            assert b'A boring annotation' in rv.data

            rv = self.app.get(
                url_for('annotation_delete', id_=1),
                follow_redirects=True)
            assert b'Annotation deleted' in rv.data

            self.app.post(
                url_for('annotation_insert', id_=iiif_id),
                data={
                    'coordinate': '1.5,1.6,1.4,9.6,8.6,9.6,8.6,1.6',
                    'text': 'An interesting annotation',
                    'entity': place.id})

            with app.test_request_context():
                app.preprocess_request()
                iiif_file.delete_links(['P67'])

            rv = self.app.get(
                url_for('admin_annotation_delete', id_=2),
                follow_redirects=True)
            assert b'Annotation deleted' in rv.data

            with app.test_request_context():
                app.preprocess_request()
                files = Entity.get_by_class('file')

            for file in files:
                rv = self.app.get(
                    url_for('delete', id_=file.id),
                    follow_redirects=True)
                assert b'The entry has been deleted' in rv.data
