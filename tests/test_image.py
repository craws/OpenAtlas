import pathlib
import shutil
from shutil import copyfile

from flask import g, url_for

from openatlas import app
from openatlas.display.image_processing import safe_resize_image
from openatlas.display.util import profile_image
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, get_hierarchy, insert_entity


class ImageTest(TestBaseCase):

    def test_image(self) -> None:
        app.config['IMAGE_SIZE']['tmp'] = '1'
        with app.app_context():
            place = insert_entity('place', 'Nostromos')
            logo = pathlib.Path(app.root_path) \
                / 'static' / 'images' / 'layout' / 'logo.png'

            # Resizing through UI insert
            with open(logo, 'rb') as img:
                rv = self.app.post(
                    url_for('insert', class_='file', origin_id=place.id),
                    data={'name': 'OpenAtlas logo', 'file': img},
                    follow_redirects=True)
            assert b'An entry has been created' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                files = Entity.get_by_class('file')
                file_id = files[0].id

            rv = self.app.get(
                url_for('set_profile_image', id_=file_id, origin_id=place.id),
                follow_redirects=True)
            assert b'Remove' in rv.data

            rv = self.app.get(url_for('index', view='file', delete_id=file_id))
            assert b'The entry has been deleted' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                file_pathless = insert_entity('file', 'Pathless_File')
                file = insert_entity('file', 'Test_File', )
                file.link('P2', g.types[get_hierarchy('License').subs[0]])
                file_name = f'{file.id}.jpeg'
                copyfile(
                    pathlib.Path(app.root_path)
                    / 'static' / 'images' / 'layout' / 'logo.png',
                    pathlib.Path(app.config['UPLOAD_DIR'] / file_name))
                file2 = insert_entity('file', 'Test_File2')
                file2.link('P2', g.types[get_hierarchy('License').subs[0]])
                copyfile(
                    pathlib.Path(app.root_path) / 'static' / 'images'
                    / 'layout' / 'logo.png',
                    pathlib.Path(
                        app.config['UPLOAD_DIR'] / f'{file2.id}.jpeg'))
                file_py = insert_entity('file', 'Test_Py')
                dst_py = \
                    pathlib.Path(app.config['UPLOAD_DIR'] / f'{file_py.id}.py')
                copyfile(
                    pathlib.Path(app.root_path) / 'views' / 'index.py',
                    dst_py)
                safe_resize_image(file2.id, '.png', size="???")
                profile_image(file_pathless)

            # Resizing images (don't change order!)
            rv = self.app.get(url_for('view', id_=file_py.id))
            assert b'No preview available' in rv.data

            rv = self.app.get(url_for('view', id_=file_pathless.id))
            assert b'missing file' in rv.data

            rv = self.app.get(url_for('index', view='file'))
            assert b'Test_File' in rv.data

            # Display file
            rv = self.app.get(url_for('display_file', filename=file_name))
            assert b'\xff' in rv.data

            rv = self.app.get(
                url_for(
                    'display_file',
                    filename=file_name,
                    size=app.config['IMAGE_SIZE']['thumbnail']))
            assert b'\xff' in rv.data

            rv = self.app.get(url_for(
                'api_03.display',
                filename=file_name,
                image_size='thumbnail'))
            assert b'\xff' in rv.data

            app.config['IMAGE_SIZE']['tmp'] = '<'
            rv = self.app.get(url_for('view', id_=file.id))
            assert b'Test_File' in rv.data

            app.config['IMAGE_SIZE']['tmp'] = '1'
            rv = self.app.get(
                url_for('admin_resize_images'),
                follow_redirects=True)
            assert b'Images were created' in rv.data

            rv = self.app.get(
                url_for('admin_delete_orphaned_resized_images'),
                follow_redirects=True)
            assert b'Resized orphaned images were deleted' in rv.data

            shutil.rmtree(
                pathlib.Path(
                    app.config['RESIZED_IMAGES'] /
                    app.config['IMAGE_SIZE']['tmp']))
            dst_py.unlink()
            del app.config['IMAGE_SIZE']['tmp']
