from flask import Response, send_file, send_from_directory
from flask_restful import Resource

from openatlas import app
from openatlas.api.v02.resources.error import AccessDeniedError
from openatlas.api.v02.resources.parser import image
from openatlas.models.entity import Entity
from openatlas.models.node import Node


class DisplayImage(Resource):
    @staticmethod
    def get(filename: str) -> Response:
        from pathlib import Path as Pathlib_path
        entity = Entity.get_by_id(int(Pathlib_path(filename).stem), nodes=True)
        license_ = None
        for node in entity.nodes:
            if node.root and node.root[-1] == Node.get_hierarchy('License').id:
                license_ = node.name
        if not license_:
            raise AccessDeniedError
        parser = image.parse_args()
        if parser['download']:
            return send_file(
                f"{app.config['UPLOAD_DIR']}/{filename}",
                as_attachment=True)
        if parser['image_size']:
            size = app.config['IMAGE_SIZE'][parser['image_size']]
            return send_from_directory(
                f"{app.config['RESIZED_IMAGES']}/{size}",
                filename)
        return send_from_directory(app.config['UPLOAD_DIR'], filename)
