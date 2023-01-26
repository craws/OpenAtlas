import pathlib

from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, get_hierarchy, insert


class FileTest(TestBaseCase):

    def test_file(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                place = insert('place', 'File keeper')
                reference = insert('edition', 'Ancient Books')
                type_id = get_hierarchy('Sex').subs[0]
                logo = pathlib.Path(app.root_path) \
                    / 'static' / 'images' / 'layout' / 'logo.png'

            with open(logo, 'rb') as img_1, open(logo, 'rb') as img_2:
                rv = self.app.post(
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
                app.preprocess_request()  # type: ignore
                files = Entity.get_by_class('file')
                file_id = files[0].id

            filename = f'{file_id}.png'
            with self.app.get(url_for('display_logo', filename=filename)):
                pass

            with self.app.get(url_for('download_file', filename=filename)):
                pass

            rv = self.app.get(
                url_for('admin_logo'),
                data={'file': file_id},
                follow_redirects=True)
            assert b'OpenAtlas logo' in rv.data

            rv = self.app.get(
                url_for('admin_logo', id_=file_id),
                follow_redirects=True)
            assert b'Remove custom logo' in rv.data

            rv = self.app.get(
                url_for('admin_index', action="remove_logo", id_=0),
                follow_redirects=True)
            assert b'Logo' in rv.data

            with open(
                    pathlib.Path(app.root_path) / 'views' / 'index.py', 'rb') \
                    as invalid_file:
                rv = self.app.post(
                    url_for('insert', class_='file', origin_id=place.id),
                    data={'name': 'Invalid file', 'file': invalid_file},
                    follow_redirects=True)
            assert b'File type not allowed' in rv.data

            rv = self.app.get(
                url_for('file_remove_profile_image', entity_id=place.id),
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
            assert b'Link actor' in rv.data

            rv = self.app.post(
                url_for('file_add', id_=file_id, view='actor'),
                data={'checkbox_values': [place.id]},
                follow_redirects=True)
            assert b'File keeper' in rv.data

            rv = self.app.get(url_for('update', id_=place.id))
            assert b'alt="image"' in rv.data

            rv = self.app.post(
                url_for('entity_add_file', id_=type_id),
                data={'checkbox_values': str([file_id])},
                follow_redirects=True)
            assert b'Updated file' in rv.data

            for file in files:
                rv = self.app.get(
                    url_for('index', view='file', delete_id=file.id))
                assert b'The entry has been deleted' in rv.data
