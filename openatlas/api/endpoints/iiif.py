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
        img_url = f"{app.config['IIIF']['url']}{id_}"
        req = requests.get(f"{img_url}/info.json")
        img_api = req.json()
        entity = get_entity_by_id(id_)
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFSequence.build_sequence(entity, img_url, img_api))

    @staticmethod
    def build_sequence(entity: Entity, img_url: str, img_api: dict[str, Any]):
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
                IIIFCanvas.build_canvas(entity, img_url, img_api)]}


class IIIFCanvas(Resource):
    @staticmethod
    def get(version: int, id_: int) -> Response:
        img_url = f"{app.config['IIIF']['url']}{id_}"
        req = requests.get(f"{img_url}/info.json")
        img_api = req.json()
        entity = get_entity_by_id(id_)
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFCanvas.build_canvas(entity, img_url, img_api))

    @staticmethod
    def build_canvas(entity: Entity, img_url: str, img_api: dict[str, Any]):
        return {
            "@id": url_for(
                'api.iiif_canvas', id_=entity.id, version=2, _external=True),
            "@type": "sc:Canvas",
            "label": entity.name,
            "height": img_api['height'],
            "width": img_api['width'],
            "description": {
                "@value": entity.description,
                "@language": "en"},
            "images": [
                IIIFImage.build_image(entity.id, img_url, img_api)],
            "related": "",
            "thumbnail": {
                "@id": f'{img_url}/full/!200,200/0/default.jpg',
                "@type": "dctypes:Image",
                "format": "image/jpeg",
                "height": 200,
                "width": 200,
                "service": {
                    "@context": "http://iiif.io/api/image/2/context.json",
                    "@id": img_url,
                    "profile": img_api['profile']},
            },
        }


class IIIFImage(Resource):
    @staticmethod
    def get(version: int, id_: int) -> Response:
        image_url = f"{app.config['IIIF']['url']}{id_}"
        req = requests.get(f"{image_url}/info.json")
        image_api = req.json()
        return jsonify(IIIFImage.build_image(id_, image_url, image_api))

    @staticmethod
    def build_image(id_: int, img_url: str, img_api: dict[str, Any]):
        return {
            "@context": "https://iiif.io/api/presentation/2/context.json",
            "@id":
                url_for('api.iiif_image', id_=id_, version=2, _external=True),
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "resource": {
                "@id": img_url,
                "@type": "dctypes:Image",
                "format": "image/jpeg",
                "service": {
                    "@context": "http://iiif.io/api/image/2/context.json",
                    "@id": img_url,
                    "profile": img_api['profile']},
                "height": img_api['height'],
                "width": img_api['width']},
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
        image_url = f"{app.config['IIIF']['url']}{id_}"
        req = requests.get(f"{image_url}/info.json")
        image_api = req.json()
        return {
            "@context": "http://iiif.io/api/presentation/2/context.json",
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
                IIIFSequence.build_sequence(entity, image_url, image_api)],
            "structures": []}
