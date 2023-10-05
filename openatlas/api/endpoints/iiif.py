from typing import Any

import requests
from flask import jsonify, Response, url_for
from flask_restful import Resource

from openatlas.api.resources.model_mapper import get_entity_by_id
from openatlas.api.resources.util import get_license_name
from openatlas import app
from openatlas.models.entity import Entity


class IIIFSequence(Resource):
    @staticmethod
    def get(version: int, id_: int) -> Response:
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFSequence.build_sequence(
                get_entity_by_id(id_),
                get_iiif_metadata(id_)))

    @staticmethod
    def build_sequence(entity: Entity, metadata: dict[str, Any]):
        return {
            "@id": url_for(
                'api.iiif_sequence',
                id_=entity.id,
                version=2,
                _external=True),
            "@type": "sc:Sequence",
            "label": [{
                "@value": "Normal Sequence",
                "@language": "en"}],
            "canvases": [
                IIIFCanvas.build_canvas(entity, metadata)]}


class IIIFCanvas(Resource):
    @staticmethod
    def get(version: int, id_: int) -> Response:
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFCanvas.build_canvas(
                get_entity_by_id(id_),
                get_iiif_metadata(id_)))

    @staticmethod
    def build_canvas(entity: Entity, metadata: dict[str, Any]):
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
            "images": [
                IIIFImage.build_image(entity.id, metadata)],
            "related": "",
            "thumbnail": {
                "@id": f'{metadata["img_url"]}/full/!200,200/0/default.jpg',
                "@type": "dctypes:Image",
                "format": "image/jpeg",
                "height": 200,
                "width": 200,
                "service": {
                    "@context": "http://iiif.io/api/image/2/context.json",
                    "@id": metadata['img_url'],
                    "profile": metadata['img_api']['profile']},
            },
        }


class IIIFImage(Resource):
    @staticmethod
    def get(version: int, id_: int) -> Response:
        return jsonify(IIIFImage.build_image(id_, get_iiif_metadata(id_)))

    @staticmethod
    def build_image(id_: int, metadata: dict[str, Any]):
        return {
            "@context": "https://iiif.io/api/presentation/2/context.json",
            "@id":
                url_for('api.iiif_image', id_=id_, version=2, _external=True),
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "resource": {
                "@id": metadata['img_url'],
                "@type": "dctypes:Image",
                "format": "image/jpeg",
                "service": {
                    "@context": "http://iiif.io/api/image/2/context.json",
                    "@id":  metadata['img_url'],
                    "profile": metadata['img_api']['profile']},
                "height":  metadata['img_api']['height'],
                "width":  metadata['img_api']['width']},
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
            "@id": url_for('api.iiif_manifest', id_=id_, version=2),
            "@type": "sc:Manifest",
            "label": entity.name,
            "metadata": [],
            "description": [{
                "@value": entity.description,
                "@language": "en"}],
            "license": get_license_name(entity),
            "attribution": "By OpenAtlas",
            "sequences": [
                IIIFSequence.build_sequence(entity, get_iiif_metadata(id_))],
            "structures": []}


def get_iiif_metadata(id_: int) -> dict[str, Any]:
    image_url = f"{app.config['IIIF']['url']}{id_}.tiff"
    req = requests.get(f"{image_url}/info.json")
    image_api = req.json()
    return {'img_url': image_url, 'img_api': image_api}
