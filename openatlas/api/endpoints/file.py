import mimetypes
from collections import defaultdict
from pathlib import Path as Pathlib_path
from typing import Any, Optional

from flask import Response, g, jsonify, send_file, url_for
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.database_mapper import get_links_by_id_network
from openatlas.api.resources.error import (
    DisplayFileNotFoundError, FileIdNotInteger, NoLicenseError, NotPublicError)
from openatlas.api.resources.parser import files, image
from openatlas.api.resources.resolve_endpoints import download
from openatlas.api.resources.templates import licensed_file_template
from openatlas.api.resources.util import get_iiif_manifest_and_path, \
    get_license_name
from openatlas.database.overlay import get_by_object
from openatlas.display.util import (
    check_iiif_activation, check_iiif_file_exist, get_file_path)
from openatlas.models.entity import Entity
from openatlas.models.overlay import Overlay


class DisplayImage(Resource):
    @staticmethod
    def get(filename: str) -> Response:
        try:
            id_ = int(Pathlib_path(filename).stem)
        except ValueError:
            raise FileIdNotInteger
        entity = ApiEntity.get_by_id(id_, types=True)
        if not entity.public:
            raise NotPublicError
        if not get_license_name(entity):
            raise NoLicenseError
        parser = image.parse_args()
        size = None
        if parser['image_size']:
            size = app.config['IMAGE_SIZE'][parser['image_size']]
        filepath = get_file_path(entity, size)
        if not filepath:
            raise DisplayFileNotFoundError
        return send_file(filepath, as_attachment=bool(parser['download']))


class LicensedFileOverview(Resource):
    @staticmethod
    def get() -> Response | tuple[Any, int]:
        parser = files.parse_args()
        if parser['file_id']:
            entities = ApiEntity.get_by_ids(parser['file_id'], types=True)
        else:
            entities = ApiEntity.get_by_system_classes(['file'])
        files_dict = {}
        for entity in entities:
            if not (license_ := get_license_name(entity)):
                continue
            if not (path := get_file_path(entity)):
                continue
            iiif_manifest = ''
            if check_iiif_activation() and check_iiif_file_exist(entity.id):
                iiif_manifest = url_for(
                    'api.iiif_manifest',
                    version=g.settings['iiif_version'],
                    id_=entity.id,
                    _external=True)
            mime_type, _ = mimetypes.guess_type(path)
            files_dict[path.stem] = {
                'extension': path.suffix,
                'mimetype': mime_type,
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
                'creator': entity.creator,
                'licenseHolder': entity.license_holder,
                'publicShareable': entity.public,
                'IIIFManifest': iiif_manifest}
        if parser['download']:
            return download(files_dict, licensed_file_template(entities))
        return marshal(files_dict, licensed_file_template(entities)), 200


class EntityFiles(Resource):
    @staticmethod
    def get() -> Response:
        files_ = ApiEntity.get_by_system_classes(['file'])
        file_ids = [file.id for file in files_]
        overlays = {
            row['image_id']: Overlay(row)
            for row in get_by_object(file_ids)}
        files_dict = {
            file.id: EntityFiles.get_file_dict(
                file,
                overlays.get(file.id)) for file in files_}
        links = get_links_by_id_network(set(file_ids))
        entity_file_dict = defaultdict(list)
        for link_ in links:
            if link_['property_code'] != 'P67' or link_[
                'domain_system_class'] != 'file':
                continue
            entity_file_dict[link_['range_id']].append(
                files_dict.get(link_['domain_id']))
        return jsonify(entity_file_dict)

    @staticmethod
    def get_file_dict(
            entity: Entity,
            overlay: Optional[Overlay] = None) -> dict[str, Any]:
        path = get_file_path(entity.id)
        mime_type = None
        if path:
            mime_type, _ = mimetypes.guess_type(path)  # pragma: no cover
        data = {
            'id': entity.id,
            'title': entity.name,
            'license': get_license_name(entity),
            'creator': entity.creator,
            'licenseHolder': entity.license_holder,
            'publicShareable': entity.public,
            'mimetype': mime_type,
            'url': url_for(
                'api.display',
                filename=path.stem,
                _external=True) if path else 'N/A'}
        data.update(get_iiif_manifest_and_path(entity.id))
        if overlay:
            data.update({'overlay': overlay.bounding_box})
        return data
