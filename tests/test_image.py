import pathlib
from shutil import copyfile

from flask import g, url_for

from openatlas import app
from openatlas.models.node import Node
from tests.base import TestBaseCase, insert_entity


class ImageTest(TestBaseCase):

    def test_image(self) -> None:
        app.config['IMAGE_PROCESSING'] = True
        app.config['IMAGE_PREVIEW'] = True
        with app.app_context():  # type: ignore
            # Create entities for file
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                file = insert_entity('Test_File', 'file')
                file.link('P2', g.nodes[Node.get_hierarchy('License').subs[0]])
                file_name = f'{file.id}.png'
                src = pathlib.Path(app.root_path) / 'static' / 'images' / 'layout' / 'logo.png'
                dst = pathlib.Path(app.config['UPLOAD_DIR'] / file_name)
                copyfile(src, dst)

            rv = self.app.get(url_for('index', view='file'))
            assert b'Test_File' in rv.data
            rv = self.app.get(url_for('entity_view', id_=file.id))
            print(rv.data)
            assert b'Test_File' in rv.data

            # Display file
            rv = self.app.get(url_for('display_file_api', filename=file_name, image_size=200))
            assert b'PNG' in rv.data

            for dir_ in app.config['IMAGE_SIZE'].values():
                pathlib.Path(app.config['RESIZED_IMAGES'] / dir_ / file_name).unlink()

            # Make directory if not exist
            app.config['IMAGE_SIZE']['tmp'] = '1'
            rv = self.app.get(url_for('entity_view', id_=file.id))
            assert b'Test_File' in rv.data

            for dir_ in app.config['IMAGE_SIZE'].values():
                pathlib.Path(app.config['RESIZED_IMAGES'] / dir_ / file_name).unlink()
            pathlib.Path(app.config['RESIZED_IMAGES'] / app.config['IMAGE_SIZE']['tmp']).rmdir()
            del app.config['IMAGE_SIZE']['tmp']
            dst.unlink()
