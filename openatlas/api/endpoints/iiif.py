from __future__ import annotations

import mimetypes
from typing import Any, Tuple

import requests
import svgwrite
from flask import Response, g, jsonify, url_for
from flask_babel import lazy_gettext as _
from flask_restful import Resource

from openatlas.api.endpoints.parser import Parser
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.error import DisplayFileNotFoundError
from openatlas.api.resources.parser import iiif
from openatlas.api.resources.util import get_license_name, get_license_url
from openatlas.display.util import check_iiif_file_exist
from openatlas.models.annotation import AnnotationImage
from openatlas.models.entity import Entity


class IIIFSequence(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFSequence.build_sequence(get_metadata(
                ApiEntity.get_by_id(id_)),
                Parser(iiif.parse_args())))

    @staticmethod
    def build_sequence(
            metadata: dict[str, Any],
            parser: Parser) -> dict[str, Any]:
        return {
            "@id": url_for(
                'api.iiif_sequence',
                id_=metadata['entity'].id,
                _external=True),
            "@type": "sc:Sequence",
            "label": [{
                "@value": "Normal Sequence",
                "@language": "en"}],
            "canvases": [IIIFCanvas.build_canvas(metadata, parser)]}


class IIIFCanvas(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        return jsonify(
            {"@context": "https://iiif.io/api/presentation/2/context.json"} |
            IIIFCanvas.build_canvas(get_metadata(
                ApiEntity.get_by_id(id_)),
                Parser(iiif.parse_args())))

    @staticmethod
    def build_canvas(
            metadata: dict[str, Any],
            parser: Parser) -> dict[str, Any]:
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
                    url=parser.url,
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
            IIIFImage.build_image(get_metadata(ApiEntity.get_by_id(id_))))

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
        return jsonify(IIIFAnnotationList.build_annotation_list
                       (image_id,
                        Parser(iiif.parse_args())))

    @staticmethod
    def build_annotation_list(image_id: int, parser: Parser) -> dict[str, Any]:
        annotations_ = AnnotationImage.get_by_file(image_id)
        return {
            "@context": "https://iiif.io/api/presentation/2/context.json",
            "@id": url_for(
                'api.iiif_annotation_list',
                image_id=image_id,
                _external=True),
            "@type": "sc:AnnotationList",
            "resources": [
                IIIFAnnotation.build_annotation(annotation, parser)
                for annotation in annotations_]}


class IIIFAnnotation(Resource):
    @staticmethod
    def get(annotation_id: int) -> Response:
        return jsonify(
            IIIFAnnotation.build_annotation(
                AnnotationImage.get_by_id(annotation_id),
                Parser(iiif.parse_args())))

    @staticmethod
    def build_annotation(
            annotation: AnnotationImage,
            parser: Parser) -> dict[str, Any]:
        entity_link = ''
        if annotation.entity_id:
            entity = ApiEntity.get_by_id(annotation.entity_id)
            url = get_url(entity.id, parser.url)
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


def get_url(entity_id: int, parser_url: str) -> str:
    url = url_for('api.entity', id_=entity_id, _external=True)
    if resolver := g.settings['frontend_resolver_url']:
        url = resolver + str(entity_id)
    if parser_url:
        url = parser_url + str(entity_id)
    return url


class IIIFManifest(Resource):
    @staticmethod
    def get(version: int, id_: int) -> Response:
        operation = getattr(IIIFManifest, f'get_manifest_version_{version}')
        return jsonify(operation(id_, Parser(iiif.parse_args())))

    @staticmethod
    def get_manifest_version_2(id_: int, parser: Parser) -> dict[str, Any]:
        entity = ApiEntity.get_by_id(id_, types=True)
        if entity.class_.view != 'file' and not check_iiif_file_exist(id_):
            raise DisplayFileNotFoundError
        license_ = get_license_name(entity)
        if entity.license_holder:
            license_ = f'{license_}, {entity.license_holder}'
        metadata = []
        if references := entity.get_links('P67', inverse=True):
            for reference in references:
                url = get_url(reference.domain.id, parser.url)
                name = reference.domain.name
                if reference.domain.description:
                    name = reference.domain.description
                text = f'{name}, {reference.description}'
                metadata.append({
                    "label": _('source').capitalize(),
                    "value": f"<a href={url} target=_blank>{text}</a>"})
        if entity.creator:
            metadata.append({
                "label": _('creator').capitalize(), "value": entity.creator})
        see_also = []
        if related_entities := entity.get_links('P67'):
            for related_entity in related_entities:
                see_also.append({
                    "@id": get_url(related_entity.range.id, parser.url),
                    "label": related_entity.range.name.capitalize(),
                    "format": related_entity.range.class_.name.capitalize()})
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
            "metadata": metadata,
            "seeAlso": see_also,
            "description": [{
                "@value": entity.description or '',
                "@language": "en"}],
            "attribution": license_,
            "license": get_license_url(entity),
            "logo": get_logo(),
            "sequences": [
                IIIFSequence.build_sequence(get_metadata(entity), parser)],
            "structures": []}


def get_metadata(entity: Entity) -> dict[str, Any]:
    if entity.class_.view != 'file' and not check_iiif_file_exist(entity.id):
        raise DisplayFileNotFoundError
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
