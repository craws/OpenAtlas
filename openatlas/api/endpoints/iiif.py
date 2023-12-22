import mimetypes
from typing import Any

import requests
from flask import Response, g, jsonify, url_for
from flask_restful import Resource

from openatlas.api.resources.model_mapper import get_entity_by_id
from openatlas.api.resources.util import get_license_name
from openatlas.models.annotation import AnnotationImage
from openatlas.models.entity import Entity


class IIIFSequenceV2(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            {"@context": "http://iiif.io/api/presentation/2/context.json"} |
            IIIFSequenceV2.build_sequence(get_metadata(get_entity_by_id(id_))))

    @staticmethod
    def build_sequence(metadata: dict[str, Any]) -> dict[str, Any]:
        return {
            "@id": url_for(
                'api.iiif_sequence',
                id_=metadata['entity'].id,
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
            {"@context": "http://iiif.io/api/presentation/2/context.json"} |
            IIIFCanvasV2.build_canvas(get_metadata(get_entity_by_id(id_))))

    @staticmethod
    def build_canvas(metadata: dict[str, Any]) -> dict[str, Any]:
        entity = metadata['entity']
        mime_type, _ = mimetypes.guess_type(g.files[entity.id])
        return {
            "@id": url_for('api.iiif_canvas', id_=entity.id, _external=True),
            "@type": "sc:Canvas",
            "label": entity.name,
            "height": metadata['img_api']['height'],
            "width": metadata['img_api']['width'],
            "description": {
                "@value": entity.description or '',
                "@language": "en"},
            "images": [IIIFImageV2.build_image(metadata)],
            "related": "",
            "otherContent": [{
                "@id": url_for(
                    'api.iiif_annotation_list',
                    id_=entity.id,
                    _external=True),
                "@type": "sc:AnnotationList"}],
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
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id":
                url_for('api.iiif_image', id_=id_, _external=True),
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
                url_for('api.iiif_canvas', id_=id_, _external=True)}


class IIIFAnnotationListV2(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            IIIFAnnotationListV2.build_annotation_list(
                get_metadata(get_entity_by_id(id_))))

    @staticmethod
    def build_annotation_list(metadata: dict[str, Any]) -> dict[str, Any]:
        id_ = metadata['entity'].id
        return {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": url_for(
                'api.iiif_annotation_list',
                id_=id_,
                _external=True),
            "@type": "sc:AnnotationList",
            "resources":
                [IIIFAnnotationV2.build_annotation(metadata, anno)
                 for anno in AnnotationImage.get_by_file(id_)]}


class IIIFAnnotationV2(Resource):
    @staticmethod
    def get(id_: int, annotation_id: int) -> Response:
        return jsonify(
            IIIFImageV2.build_annotation(
                get_metadata(get_entity_by_id(id_)),
                AnnotationImage.get_by_file(annotation_id)))

    @staticmethod
    def build_annotation(
            metadata: dict[str, Any],
            anno: dict[str, Any]) -> dict[str, Any]:
        id_ = metadata['entity'].id
        selector = generate_selector(anno)
        return {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": url_for(
                'api.iiif_annotation',
                id_=id_,
                annotation_id=anno['id'],
                _external=True),
            "@type": "oa:Annotation",
            "motivation": ["oa:commenting"],
            "resource": [{
                "@type": "dctypes:Text",
                "chars": anno['annotation'],
                "format": "text/html"
            }],
            "on": {
                "@type": "oa:SpecificResource",
                "full": url_for('api.iiif_canvas', id_=id_, _external=True),
                "selector": selector,
                "within": {
                    "@id": url_for(
                        'api.iiif_manifest',
                        id_=id_, version=2,
                        _external=True),
                    "@type": "sc:Manifest"}}}


def calculate_fragment_selector_coordinates(coordinates):
    coordinates_str = coordinates['coordinates']
    # Splitting the coordinates string into individual values
    coordinates_list = list(map(float, coordinates_str.split(',')))

    # Extracting x, y, width, and height from the coordinates
    x_min, y_min,x_max, y_max = (
        min(coordinates_list[::2]),
        min(coordinates_list[1::2]),
        max(coordinates_list[::2]),
        max(coordinates_list[1::2]))
    x = x_min
    y = y_min
    width = x_max - x_min
    height = y_max - y_min
    return x, y, width, height


def generate_selector(annotation):
    x, y, width, height = calculate_fragment_selector_coordinates(annotation)
    return {
        "@type": "oa:FragmentSelector",
        "value": f"xywh={x},{y},{width},{height}"}


class IIIFManifest(Resource):
    @staticmethod
    def get(version: int, id_: int) -> Response:
        operation = getattr(IIIFManifest, f'get_manifest_version_{version}')
        return jsonify(operation(id_))

    @staticmethod
    def get_manifest_version_2(id_: int) -> dict[str, Any]:
        entity = get_entity_by_id(id_)
        return {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id":
                url_for(
                    'api.iiif_manifest',
                    id_=id_,
                    version=2,
                    _external=True),
            "@type": "sc:Manifest",
            "label": entity.name,
            "metadata": [{
                "label": "Title",
                "value": entity.name}],
            "description": [{
                "@value": entity.description or '',
                "@language": "en"}],
            "license": get_license_name(entity),
            "attribution": "By OpenAtlas",
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
            "@context": "http://iiif.io/api/image/2/context.json",
            "@id": url_for('overview', _external=True),
            "profile": "http://iiif.io/api/image/2/level2.json"}}
