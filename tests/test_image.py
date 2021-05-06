import pathlib
from shutil import copyfile

from flask import url_for

from openatlas import app
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
                file_name = f'{file.id}.png'
                src = pathlib.Path(app.root_path) / 'static' / 'images' / 'layout' / 'logo.png'
                dst = pathlib.Path(app.config['UPLOAD_DIR'] / file_name)
                copyfile(src, dst)


            rv = self.app.get(url_for('index', view='file'))
            assert b'Test_File' in rv.data
            rv = self.app.get(url_for('entity_view', id_=file.id))
            assert b'Test_File' in rv.data

            dst.unlink()
            for dir in app.config['IMAGE_SIZE'].values():
                pathlib.Path(app.config['RESIZED_IMAGES'] / dir / file_name).unlink()
