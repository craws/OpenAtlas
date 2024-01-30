from pathlib import Path
from typing import Any

from flask import g, url_for

from openatlas import app
from openatlas.display.util import check_iiif_file_exist, get_iiif_file_path
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, get_hierarchy, insert


class FileTest(TestBaseCase):

    def test_file(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()
                place = insert('place', 'File keeper')
                reference = insert('edition', 'Ancient Books')

            logo = Path(app.root_path) \
                / 'static' / 'images' / 'layout' / 'logo.png'

            with open(logo, 'rb') as img_1, open(logo, 'rb') as img_2:
                rv: Any = self.app.post(
                    url_for('insert', class_='file', origin_id=place.id),
                    data={'name': 'OpenAtlas logo', 'file': [img_1, img_2]},
                    follow_redirects=True)
            assert b'An entry has been created' in rv.data

            with open(logo, 'rb') as img:
                rv = self.app.post(
                    url_for('insert', class_='file', origin_id=reference.id),
                    data={'name': 'OpenAtlas logo', 'file': img},
                    follow_redirects=True)
            assert b'An entry has been created' in rv.data

            with app.test_request_context():
                app.preprocess_request()
                files = Entity.get_by_class('file')
                file_id = files[0].id

            # Remove IIIF file to not break tests
            if check_iiif_file_exist(file_id):
                if path := get_iiif_file_path(file_id):  # pragma: no cover
                    path.unlink()  # pragma: no cover

            rv = self.app.get(
                url_for('admin_convert_iiif_files'),
                follow_redirects=True)
            assert b'All image files are converted' in rv.data

            # Remove IIIF file to not break tests
            if check_iiif_file_exist(file_id):
                if path := get_iiif_file_path(file_id):  # pragma: no cover
                    path.unlink()  # pragma: no cover

            filename = f'{file_id}.png'
            with self.app.get(url_for('display_logo', filename=filename)):
                pass

            with self.app.get(url_for('download', filename=filename)):
                pass

            rv = self.app.get(url_for('admin_logo'), data={'file': file_id})
            assert b'OpenAtlas logo' in rv.data

            rv = self.app.get(
                url_for('admin_logo', id_=file_id),
                follow_redirects=True)
            assert b'remove custom logo' in rv.data

            rv = self.app.get(
                url_for('admin_index', action="remove_logo", id_=0),
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
                data={'file': file_id, 'page': '777'},
                follow_redirects=True)
            assert b'777' in rv.data

            rv = self.app.post(
                url_for('update', id_=file_id),
                data={'name': 'Updated file'},
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            rv = self.app.get(url_for('file_add', id_=file_id, view='actor'))
            assert b'link actor' in rv.data

            rv = self.app.post(
                url_for('file_add', id_=file_id, view='actor'),
                data={'checkbox_values': [place.id]},
                follow_redirects=True)
            assert b'File keeper' in rv.data

            rv = self.app.get(url_for('update', id_=place.id))
            assert b'File keeper' in rv.data

            rv = self.app.post(
                url_for('entity_add_file', id_=get_hierarchy('Sex').subs[0]),
                data={'checkbox_values': str([file_id])},
                follow_redirects=True)
            assert b'Updated file' in rv.data

            rv = self.app.get(url_for('view', id_=file_id))
            assert b'Logo' in rv.data

            rv = self.app.get(url_for('view', id_=file_id))
            assert b'enable IIIF view' in rv.data

            rv = self.app.get(
                url_for('make_iiif_available', id_=file_id),
                follow_redirects=True)
            assert b'IIIF converted' in rv.data

            rv = self.app.get(url_for('view', id_=file_id))
            assert b'view in IIIF' in rv.data

            rv = self.app.get(url_for('view', id_=place.id))
            assert b'view in IIIF' in rv.data

            rv = self.app.get(
                url_for(
                    'api.iiif_manifest',
                    id_=file_id,
                    version=g.settings['iiif_version']))
            rv = rv.get_json()
            assert bool(rv['label'] == 'Updated file')

            rv = self.app.get(url_for('api.iiif_sequence', id_=file_id))
            assert bool(str(file_id) in rv.get_json()['@id'])

            rv = self.app.get(url_for('api.iiif_image', id_=file_id))
            assert bool(str(file_id) in rv.get_json()['@id'])

            rv = self.app.get(url_for('api.iiif_canvas', id_=file_id))
            assert bool(str(file_id) in rv.get_json()['@id'])

            with app.test_request_context():
                app.preprocess_request()
                files[0].link('P2', g.types[get_hierarchy('License').subs[0]])

            rv = self.app.get(url_for('api.licensed_file_overview'))
            assert bool(len(rv.get_json().keys()) == 3)
            rv = self.app.get(
                url_for('api.licensed_file_overview', download=True))
            assert bool(len(rv.get_json().keys()) == 3)
            rv = self.app.get(
                url_for('api.licensed_file_overview', file_id=file_id))
            assert bool(len(rv.get_json().keys()) == 1)

            rv = self.app.get(url_for('view_iiif', id_=file_id))
            assert b'Mirador' in rv.data

            rv = self.app.get(url_for('view_iiif', id_=place.id))
            assert b'Mirador' in rv.data

            rv = self.app.get(url_for('view', id_=place.id))
            assert b'/full/!100,100/0/default.jpg' in rv.data

            rv = self.app.get(url_for('view', id_=place.id))
            assert b'Logo' in rv.data

            rv = self.app.get(url_for('annotation_insert', id_=file_id))
            assert b'Annotate' in rv.data

            rv = self.app.post(
                url_for('annotation_insert', id_=file_id),
                data={
                    'coordinate': '1.5,1.6,1.4,9.6,8.6,9.6,8.6,1.6',
                    'text': 'An interesting annotation'},
                follow_redirects=True)
            assert b'An interesting annotation' in rv.data

            rv = self.app.get(url_for('annotation_update', id_=1))
            assert b'An interesting annotation' in rv.data

            rv = self.app.get(
                url_for('api.iiif_annotation_list', image_id=file_id))
            json = rv.get_json()
            assert bool(str(file_id) in json['@id'])

            annotation_id = json['resources'][0]['@id'].rsplit('/', 1)[-1]
            rv = self.app.get(url_for(
                'api.iiif_annotation',
                annotation_id=annotation_id.replace('.json', '')))
            assert bool(annotation_id in rv.get_json()['@id'])

            rv = self.app.post(
                url_for('annotation_update', id_=1),
                data={'text': 'A boring annotation'},
                follow_redirects=True)
            assert b'A boring annotation' in rv.data

            rv = self.app.get(
                url_for('annotation_delete', id_=1),
                follow_redirects=True)
            assert b'Annotation deleted' in rv.data

            for file in files:
                rv = self.app.get(
                    url_for('delete', id_=file.id),
                    follow_redirects=True)
                assert b'The entry has been deleted' in rv.data
