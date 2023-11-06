from pathlib import Path as Pathlib_path
from typing import Any

from flask import Response, g, send_file, url_for
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.resources.error import (
    DisplayFileNotFoundError, NoLicenseError)
from openatlas.api.resources.model_mapper import (
    get_entities_by_ids, get_entities_by_system_classes, get_entity_by_id)
from openatlas.api.resources.parser import files, image
from openatlas.api.resources.resolve_endpoints import download
from openatlas.api.resources.templates import licensed_file_template
from openatlas.api.resources.util import get_license_name
from openatlas.display.util import (
    check_iiif_activation, check_iiif_file_exist, get_file_path)


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
                    iiif_manifest = ''
                    if check_iiif_activation() and \
                            check_iiif_file_exist(entity.id):
                        iiif_manifest = url_for(
                            'api.iiif_manifest',
                            version=g.settings['iiif_version'],
                            id_=entity.id,
                            _external=True)
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
                        'license': license_,
                        'IIIFManifest': iiif_manifest}
        if parser['download']:
            download(files_dict, licensed_file_template(entities), 'files')
        return marshal(files_dict, licensed_file_template(entities)), 200
