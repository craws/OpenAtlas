from __future__ import annotations

import mimetypes
from typing import Any, Tuple

import requests
import svgwrite
from flask import Response, g, jsonify, url_for
from flask_restful import Resource

from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.util import get_license_name
from openatlas.models.annotation import Annotation
from openatlas.models.entity import Entity


class IIIFSequence(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFSequence.build_sequence(
                get_metadata(ApiEntity.get_entity_by_id_safe(id_))))

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
            "canvases": [IIIFCanvas.build_canvas(metadata)]}


class IIIFCanvas(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFCanvas.build_canvas(
                get_metadata(ApiEntity.get_entity_by_id_safe(id_))))

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
            "images": [IIIFImage.build_image(metadata)],
            "related": "",
            "otherContent": [{
                "@id": url_for(
                    'api.iiif_annotation_list',
                    image_id=entity.id,
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


class IIIFImage(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            IIIFImage.build_image(
                get_metadata(ApiEntity.get_entity_by_id_safe(id_))))

    @staticmethod
    def build_image(metadata: dict[str, Any]) -> dict[str, Any]:
        id_ = metadata['entity'].id
        mime_type, _ = mimetypes.guess_type(g.files[id_])
        return {
            "@context": "https://iiif.io/api/presentation/2/context.json",
            "@id": url_for('api.iiif_image', id_=id_, _external=True),
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
            "on": url_for('api.iiif_canvas', id_=id_, _external=True)}


class IIIFAnnotationList(Resource):
    @staticmethod
    def get(image_id: int) -> Response:
        return jsonify(IIIFAnnotationList.build_annotation_list(image_id))

    @staticmethod
    def build_annotation_list(image_id: int) -> dict[str, Any]:
        annotations_ = Annotation.get_by_file(image_id)
        return {
            "@context": "https://iiif.io/api/presentation/2/context.json",
            "@id": url_for(
                'api.iiif_annotation_list',
                image_id=image_id,
                _external=True),
            "@type": "sc:AnnotationList",
            "resources": [
                IIIFAnnotation.build_annotation(annotation)
                for annotation in annotations_]}


class IIIFAnnotation(Resource):
    @staticmethod
    def get(annotation_id: int) -> Response:
        return jsonify(
            IIIFAnnotation.build_annotation(
                Annotation.get_by_id(annotation_id)))

    @staticmethod
    def build_annotation(annotation: Annotation) -> dict[str, Any]:
        entity_link = ''
        if annotation.entity_id:
            entity = ApiEntity.get_entity_by_id_safe(annotation.entity_id)
            url = url_for('api.entity', id_=entity.id, _external=True)
            if resolver := g.settings['frontend_resolver_url']:
                url = resolver + str(entity.id)
            entity_link = f"<a href={url} target=_blank>{entity.name}</a>"
        return {
            "@context": "https://iiif.io/api/presentation/2/context.json",
            "@id": url_for(
                'api.iiif_annotation',
                annotation_id=annotation.id,
                _external=True),
            "@type": "oa:Annotation",
            "motivation": ["oa:commenting"],
            "resource": [{
                "@type": "dctypes:Dataset",
                "chars": entity_link,
                "format": "text/html"}, {
                "@type": "dctypes:Text",
                "chars": annotation.text,
                "format": "text/plain"}
            ],
            "on": {
                "@type": "oa:SpecificResource",
                "full": url_for(
                    'api.iiif_canvas',
                    id_=annotation.image_id,
                    _external=True),
                "selector": generate_selector(annotation.coordinates),
                "within": {
                    "@id": url_for(
                        'api.iiif_manifest',
                        id_=annotation.image_id,
                        version=2,
                        _external=True),
                    "@type": "sc:Manifest"}}}


def convert_coordinates(coordinates_str: str) -> list[list[int]]:
    coordinates = list(map(float, coordinates_str.split(',')))
    return [[int(coordinates[i]), int(coordinates[i + 1])]
            for i in range(0, len(coordinates), 2)]


def generate_svg_path(coordinates: list[list[int]]) -> str:
    dwg = svgwrite.Drawing(size=("100%", "100%"))
    path = dwg.path(
        d=f"M{'L'.join([f'{x},{y}' for x, y in coordinates])}z",
        fill="none", stroke="#0d6efd", stroke_width=1)
    dwg.add(path)
    return dwg.tostring()


def calculate_bounding_box(
        coordinates: list[list[int]]) -> Tuple[int, int, int, int]:
    x_values = [x for x, y in coordinates]
    y_values = [y for x, y in coordinates]
    x = min(x_values)
    y = min(y_values)
    width = max(x_values) - x
    height = max(y_values) - y
    return x, y, width, height


def generate_selector(coordinates_str: str) -> dict[str, Any]:
    coordinates = convert_coordinates(coordinates_str)
    x, y, width, height = calculate_bounding_box(coordinates)
    return {
        "default": {
            "@type": "oa:FragmentSelector",
            "value": f"xywh={x},{y},{width},{height}"},
        "item": {
            "@type": "oa:SvgSelector",
            "value": generate_svg_path(coordinates)},
        "@type": "oa:Choice"}


class IIIFManifest(Resource):
    @staticmethod
    def get(version: int, id_: int) -> Response:
        operation = getattr(IIIFManifest, f'get_manifest_version_{version}')
        return jsonify(operation(id_))

    @staticmethod
    def get_manifest_version_2(id_: int) -> dict[str, Any]:
        entity = ApiEntity.get_entity_by_id_safe(id_)
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
            "metadata": [{
                "label": "Title",
                "value": entity.name}],
            "description": [{
                "@value": entity.description or '',
                "@language": "en"}],
            "license": get_license_name(entity),
            "logo": get_logo(),
            "sequences": [
                IIIFSequence.build_sequence(get_metadata(entity))],
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
