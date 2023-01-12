from pathlib import Path as Pathlib_path

from flask import Response, send_file, send_from_directory
from flask_restful import Resource

from openatlas import app
from openatlas.api.resources.error import AccessDeniedError
from openatlas.api.resources.parser import image
from openatlas.api.resources.util import get_license
from openatlas.api.resources.model_mapper import get_entity_by_id
from openatlas.display.image_processing import check_processed_image


class DisplayImage(Resource):

    @staticmethod
    def get(filename: str) -> Response:
        entity = get_entity_by_id(int(Pathlib_path(filename).stem))
        license_ = get_license(entity)
        if not license_:
            raise AccessDeniedError
        parser = image.parse_args()
        if parser['download']:
            return send_file(
                f"{app.config['UPLOAD_DIR']}/{filename}",
                as_attachment=True)
        directory = app.config['UPLOAD_DIR']
        if parser['image_size'] \
                and check_processed_image(filename):
            size = app.config['IMAGE_SIZE'][parser['image_size']]
            directory = f"{app.config['RESIZED_IMAGES']}/{size}"
        return send_from_directory(directory, filename)
