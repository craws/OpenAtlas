import mimetypes
from typing import Any

import requests
from flask import jsonify, Response, url_for, g
from flask_restful import Resource

from openatlas.api.resources.model_mapper import get_entity_by_id
from openatlas.api.resources.util import get_license_name
from openatlas.models.entity import Entity


class IIIFSequenceV2(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFSequenceV2.build_sequence(get_metadata(get_entity_by_id(id_))))

    @staticmethod
    def build_sequence(metadata: dict[str, Any]) -> dict[str, Any]:
        return {
            "@id": url_for(
                'api.iiif_sequence',
                id_=metadata['entity'].id,
                version=2,
                _external=True),
            "@type": "sc:Sequence",
            "label": [{
                "@value": "Normal Sequence",
                "@language": "en"}],
            "canvases": [
                IIIFCanvasV2.build_canvas(metadata)]}


class IIIFCanvasV2(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFCanvasV2.build_canvas(get_metadata(get_entity_by_id(id_))))

    @staticmethod
    def build_canvas(metadata: dict[str, Any]) -> dict[str, Any]:
        entity = metadata['entity']
        mime_type, _ = mimetypes.guess_type(g.files[entity.id])
        return {
            "@id": url_for(
                'api.iiif_canvas', id_=entity.id, version=2, _external=True),
            "@type": "sc:Canvas",
            "label": entity.name,
            "height": metadata['img_api']['height'],
            "width": metadata['img_api']['width'],
            "description": {
                "@value": entity.description,
                "@language": "en"},
            "images": [IIIFImageV2.build_image(metadata)],
            "related": "",
            "thumbnail": {
                "@id": f'{metadata["img_url"]}/full/!200,200/0/default.jpg',
                "@type": "dctypes:Image",
                "format": mime_type,
                "height": 200,
                "width": 200,
                "service": {
                    "@context": "https://iiif.io/api/image/2/context.json",
                    "@id": metadata['img_url'],
                    "profile": metadata['img_api']['profile']}}}


class IIIFImageV2(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            IIIFImageV2.build_image(get_metadata(get_entity_by_id(id_))))

    @staticmethod
    def build_image(metadata: dict[str, Any]) -> dict[str, Any]:
        id_ = metadata['entity'].id
        mime_type, _ = mimetypes.guess_type(g.files[id_])
        return {
            "@context": "https://iiif.io/api/presentation/2/context.json",
            "@id":
                url_for('api.iiif_image', id_=id_, version=2, _external=True),
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "resource": {
                "@id": metadata['img_url'],
                "@type": "dctypes:Image",
                "format": mime_type,
                "service": {
                    "@context": "https://iiif.io/api/image/2/context.json",
                    "@id": metadata['img_url'],
                    "profile": metadata['img_api']['profile']},
                "height": metadata['img_api']['height'],
                "width": metadata['img_api']['width']},
            "on":
                url_for('api.iiif_canvas', id_=id_, version=2, _external=True)}


class IIIFManifest(Resource):
    @staticmethod
    def get(version: int, id_: int) -> Response:
        operation = getattr(IIIFManifest, f'get_manifest_version_{version}')
        return jsonify(operation(id_))

    @staticmethod
    def get_manifest_version_2(id_: int) -> dict[str, Any]:
        entity = get_entity_by_id(id_)
        return {
            "@context": "https://iiif.io/api/presentation/2/context.json",
            "@id":
                url_for(
                    'api.iiif_manifest',
                    id_=id_,
                    version=2,
                    _external=True),
            "@type": "sc:Manifest",
            "label": entity.name,
            "metadata": [],
            "description": [{
                "@value": entity.description,
                "@language": "en"}],
            "license": get_license_name(entity),
            "logo": get_logo(),
            "sequences": [
                IIIFSequenceV2.build_sequence(get_metadata(entity))],
            "structures": []}


def get_metadata(entity: Entity) -> dict[str, Any]:
    ext = '.tiff' if g.settings['iiif_conversion'] else entity.get_file_ext()
    image_url = f"{g.settings['iiif_url']}{entity.id}{ext}"
    req = requests.get(f"{image_url}/info.json", timeout=30)
    image_api = req.json()
    return {'entity': entity, 'img_url': image_url, 'img_api': image_api}


def get_logo() -> dict[str, Any]:
    return {
        "@id": url_for(
            'api.display',
            filename=g.settings['logo_file_id'],
            _external=True),
        "service": {
            "@context": "https://iiif.io/api/image/2/context.json",
            "@id": url_for('overview', _external=True),
            "profile": "https://iiif.io/api/image/2/level2.json"}}
