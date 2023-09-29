from pathlib import Path as Pathlib_path
from typing import Any

from flask import Response, send_file, url_for
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.resources.error import DisplayFileNotFoundError, \
    NoLicenseError
from openatlas.api.resources.parser import image, files
from openatlas.api.resources.templates import licensed_file_template
from openatlas.api.resources.util import get_license_name
from openatlas.api.resources.model_mapper import get_entity_by_id, \
    get_entities_by_system_classes, get_entities_by_ids
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
        return send_file(filepath, as_attachment=bool(parser['download']))


class LicensedFileOverview(Resource):
    @staticmethod
    def get() -> tuple[Any, int]:
        parser = files.parse_args()
        if parser['file_id']:
            entities = get_entities_by_ids(parser['file_id'])
        else:
            entities = get_entities_by_system_classes(['file'])
        files_dict = {}
        for entity in entities:
            if license_ := get_license_name(entity):
                if path := get_file_path(entity):
                    files_dict[path.stem] = {
                        'extension': path.suffix,
                        'display': url_for(
                            'api.display',
                            filename=path.stem,
                            _external=True),
                        'thumbnail': url_for(
                            'api.display',
                            image_size='thumbnail',
                            filename=path.stem,
                            _external=True),
                        'license': license_}
        return marshal(files_dict, licensed_file_template(entities)), 200
