import pathlib
import shutil
from shutil import copyfile

from flask import g, url_for

from openatlas import app
from openatlas.display.image_processing import safe_resize_image
from openatlas.display.util import profile_image
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from tests.base import TestBaseCase, insert_entity


class ImageTest(TestBaseCase):

    def test_image(self) -> None:
        app.config['IMAGE_SIZE']['tmp'] = '1'
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                place = insert_entity(
                    'Nostromos',
                    'place',
                    'That is the Nostromos')
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

            self.app.get(
                url_for('set_profile_image', id_=file_id, origin_id=place.id),
                follow_redirects=True)
            rv = self.app.get(url_for('index', view='file', delete_id=file_id))
            assert b'The entry has been deleted' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                file_pathless = insert_entity('Pathless_File', 'file')
                file = insert_entity('Test_File', 'file')
                file.link('P2', g.types[Type.get_hierarchy('License').subs[0]])
                file_name = f'{file.id}.jpeg'
                src_png = \
                    pathlib.Path(app.root_path) \
                    / 'static' / 'images' / 'layout' / 'logo.png'
                dst_png = \
                    pathlib.Path(app.config['UPLOAD_DIR'] / file_name)
                copyfile(src_png, dst_png)
                file2 = insert_entity('Test_File2', 'file')
                file2.link(
                    'P2',
                    g.types[Type.get_hierarchy('License').subs[0]])
                file2_name = f'{file2.id}.jpeg'
                src2_png = \
                    pathlib.Path(app.root_path) \
                    / 'static' / 'images' / 'layout' / 'logo.png'
                dst2_png = pathlib.Path(app.config['UPLOAD_DIR'] / file2_name)
                copyfile(src2_png, dst2_png)
                file_py = insert_entity('Test_Py', 'file')
                file_name_py = f'{file_py.id}.py'
                src_py = pathlib.Path(app.root_path) / 'views' / 'index.py'
                dst_py = pathlib.Path(app.config['UPLOAD_DIR'] / file_name_py)
                copyfile(src_py, dst_py)
                safe_resize_image(file2.id, '.png', size="???")
                profile_image(file_pathless)

            # Resizing images (don't change order!)
            rv = self.app.get(url_for('view', id_=file.id))
            assert b'Test_File' in rv.data

            rv = self.app.get(url_for('view', id_=file_py.id))
            assert b'No preview available' in rv.data

            rv = self.app.get(url_for('view', id_=file_pathless.id))
            assert b'Missing file' in rv.data

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

            rv = self.app.get(
                url_for(
                    'display_file',
                    filename=file_name,
                    size=app.config['IMAGE_SIZE']['table']))
            assert b'\xff' in rv.data

            rv = self.app.get(
                url_for(
                    'display_file',
                    filename=file_name_py,
                    size=app.config['IMAGE_SIZE']['table']))
            assert b'404' in rv.data

            # Make directory if not exist
            rv = self.app.get(url_for('view', id_=file.id))
            assert b'Test_File' in rv.data

            # API display image
            rv = self.app.get(url_for(
                'api_03.display',
                filename=file_name,
                image_size='thumbnail'))
            assert b'\xff' in rv.data

            # Exception
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

            rv = self.app.get(
                url_for('index', view='file', delete_id=file.id))
            assert b'The entry has been deleted' in rv.data

            rv = self.app.get(
                url_for('index', view='file', delete_id=file2.id))
            assert b'The entry has been deleted' in rv.data

            shutil.rmtree(
                pathlib.Path(
                    app.config['RESIZED_IMAGES'] /
                    app.config['IMAGE_SIZE']['tmp']))
            dst_py.unlink()
            del app.config['IMAGE_SIZE']['tmp']
