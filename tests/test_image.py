import pathlib
import shutil
from shutil import copyfile

from flask import g, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.node import Node
from tests.base import TestBaseCase, insert_entity


class ImageTest(TestBaseCase):

    def test_image(self) -> None:
        app.config['IMAGE_PROCESSING'] = True
        app.config['IMAGE_PREVIEW'] = True
        app.config['IMAGE_SIZE']['tmp'] = '1'
        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                # Needed for coverage
                place = insert_entity('Nostromos', 'place', description='That is the Nostromos')
                logo = pathlib.Path(app.root_path) / 'static' / 'images' / 'layout' / 'logo.png'
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

            # Set and unset as main image
            self.app.get(
                url_for('set_profile_image', id_=file_id, origin_id=place.id),
                follow_redirects=True)
            self.app.get(url_for('file_remove_profile_image', entity_id=place.id))

            # Delete
            rv = self.app.get(url_for('index', view='file', delete_id=file_id))
            assert b'The entry has been deleted' in rv.data

            # Create entities for file
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                pathless_file = insert_entity('Pathless_File', 'file')
                # pathless_name = f'{file_without_path.id}.png'

                file = insert_entity('Test_File', 'file')
                file.link('P2', g.nodes[Node.get_hierarchy('License').subs[0]])
                file_name = f'{file.id}.png'
                src_png = pathlib.Path(app.root_path) / 'static' / 'images' / 'layout' / 'logo.png'
                dst_png = pathlib.Path(app.config['UPLOAD_DIR'] / file_name)
                copyfile(src_png, dst_png)

                file_py = insert_entity('Test_Py', 'file')
                file_name_py = f'{file_py.id}.py'
                src_py = pathlib.Path(app.root_path) / 'views' / 'index.py'
                dst_py = pathlib.Path(app.config['UPLOAD_DIR'] / file_name_py)
                copyfile(src_py, dst_py)

            rv = self.app.get(url_for('entity_view', id_=file.id))
            assert b'Test_File' in rv.data

            rv = self.app.get(url_for('index', view='file'))
            assert b'Test_File' in rv.data

            # Display file
            rv = self.app.get(url_for('display_file_api', filename=file_name, image_size=200))
            assert b'PNG' in rv.data
            rv = self.app.get(url_for('display_thumbnail', filename=file_name))
            assert b'PNG' in rv.data
            rv = self.app.get(url_for('display_icon', filename=file_name))
            assert b'PNG' in rv.data

            rv = self.app.get(url_for('display_thumbnail', filename=file_name_py))
            assert b'404' in rv.data

            # Make directory if not exist
            rv = self.app.get(url_for('entity_view', id_=file.id))
            assert b'Test_File' in rv.data

            # Cleanup
            for dir_ in app.config['IMAGE_SIZE'].values():
                pathlib.Path(app.config['RESIZED_IMAGES'] / dir_ / file_name).unlink()
                # pathlib.Path(app.config['RESIZED_IMAGES'] / dir_ / file_name_py).unlink()
            # pathlib.Path(app.config['RESIZED_IMAGES'] / app.config['IMAGE_SIZE']['tmp']).rmdir()

            # temporary solution, path.rmdir() should be the way to go, but dir has to be empty
            shutil.rmtree(
                pathlib.Path(app.config['RESIZED_IMAGES'] / app.config['IMAGE_SIZE']['tmp']))

            dst_png.unlink()
            dst_py.unlink()
            del app.config['IMAGE_SIZE']['tmp']
            app.config['IMAGE_PROCESSING'] = False
            app.config['IMAGE_PREVIEW'] = False
