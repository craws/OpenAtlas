from pathlib import Path
from shutil import copyfile
from typing import Any

from flask import g, url_for

from openatlas import app
from openatlas.display.image_processing import safe_resize_image
from openatlas.display.util import profile_image
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, get_hierarchy, insert


class ImageTest(TestBaseCase):
    def test_image(self) -> None:
        c = self.client
        app.config['IMAGE_SIZE']['tmp'] = '1'
        logo_path = \
            Path(app.root_path) / 'static' / 'images' / 'layout' / 'logo.png'
        with app.test_request_context():
            app.preprocess_request()
            place = insert('place', 'Nostromos')

        with open(logo_path, 'rb') as img:
            rv: Any = c.post(
                url_for(
                    'insert',
                    class_='file',
                    origin_id=place.id,
                    relation='file'),
                data={'name': 'OpenAtlas logo', 'file': img},
                follow_redirects=True)
        assert b'An entry has been created' in rv.data

        with open(logo_path, 'rb') as img:
            rv = c.post(
                url_for(
                    'insert',
                    class_='file',
                    origin_id=place.id,
                    relation='file'),
                data={'name': 'OpenAtlas logo2', 'file': img},
                follow_redirects=True)
        assert b'An entry has been created' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            files = Entity.get_by_class('file')

        rv = c.get(
            url_for('set_profile_image', id_=files[0].id, origin_id=place.id),
            follow_redirects=True)
        assert b'Remove' in rv.data

        rv = c.get(url_for('delete', id_=files[0].id), follow_redirects=True)
        assert b'The entry has been deleted' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            file_pathless = insert('file', 'Pathless_File')
            file = insert('file', 'Test_File')
            file.link('P2', g.types[get_hierarchy('License').subs[0]])
            filename = f'{file.id}.jpeg'
            copyfile(
                Path(app.root_path)
                / 'static' / 'images' / 'layout' / 'logo.png',
                Path(app.config['UPLOAD_PATH'] / filename))
            file2 = insert('file', 'Test_File2')
            file2.link('P2', g.types[get_hierarchy('License').subs[0]])
            copyfile(
                Path(app.root_path)
                / 'static' / 'images' / 'layout' / 'logo.png',
                Path(app.config['UPLOAD_PATH'] / f'{file2.id}.jpeg'))
            file_json = insert('file', 'Test')
            copyfile(
                Path(app.root_path) / 'static' / 'manifest.json',
                Path(app.config['UPLOAD_PATH'] / f'{file_json.id}.json'))
            safe_resize_image(str(file2.id), '.png', size="???")
            profile_image(file_pathless)

        rv = c.get(url_for('view', id_=file_json.id))
        assert b'No preview available' in rv.data

        rv = c.get(url_for('view', id_=file_pathless.id))
        assert b'Missing file' in rv.data

        rv = c.get(url_for('index', group='file'))
        assert b'Test_File' in rv.data

        with c.get(url_for('display_file', name=filename)) as rv:
            assert b'\xff' in rv.data

        with c.get(
            url_for(
                'display_file',
                name=filename,
                size=app.config['IMAGE_SIZE']['thumbnail'])) as _rv:
            assert b'\xff' in rv.data

        rv = c.get(url_for('display_file', name=filename, size='500'))
        assert b'400 Bad Request' in rv.data

        rv = c.get(
            url_for('api.display', filename=filename, image_size='thumbnail'))
        assert b'This file is not public shareable' in rv.data

        app.config['IMAGE_SIZE']['tmp'] = '<'
        rv = c.get(url_for('view', id_=file.id))
        assert b'Test_File' in rv.data

        app.config['IMAGE_SIZE']['tmp'] = '1'
        rv = c.get(url_for('resize_images'), follow_redirects=True)
        assert b'Images were created' in rv.data

        rv = c.get(
            url_for('delete_orphaned_resized_images'),
            follow_redirects=True)
        assert b'Resized orphaned images were deleted' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            files = Entity.get_by_class('file')

        for file in files:
            rv = c.get(url_for('delete', id_=file.id), follow_redirects=True)
            assert b'The entry has been deleted' in rv.data
