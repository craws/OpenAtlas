from pathlib import Path as Pathlib_path

from flask import Response, send_file
from flask_restful import Resource

from openatlas import app
from openatlas.api.resources.error import DisplayFileNotFoundError, \
    NoLicenseError
from openatlas.api.resources.parser import image
from openatlas.api.resources.util import get_license_name
from openatlas.api.resources.model_mapper import get_entity_by_id
from openatlas.display.util import get_file_path


class DisplayImage(Resource):
    @staticmethod
    def get(filename: str) -> Response:
        entity = get_entity_by_id(int(Pathlib_path(filename).stem))
        if not get_license_name(entity):
            raise NoLicenseError
        parser = image.parse_args()
        filepath = get_file_path(
            entity,
            app.config['IMAGE_SIZE'][parser['image_size']]
            if parser['image_size'] else None)
        if not filepath:
            raise DisplayFileNotFoundError
        return send_file(
            filepath,
            as_attachment=bool(parser['download']))
