import ast
from dataclasses import dataclass, field
from functools import cached_property
from html import escape
from typing import Any
from urllib.parse import urlparse

import requests
import svgwrite
from flask import g, url_for
from flask_babel import gettext as _
from werkzeug.exceptions import ImATeapot

from openatlas import app
from openatlas.api.api_v1.entity import get_entity_by_id
from openatlas.api.api_v1.error_handlers import (
    abort_file_not_found, abort_georeference_not_found)
from openatlas.api.api_v1.models.files import LicenseItem
from openatlas.api.api_v1.responses.iiif import (
    IIIF_GEOREF_CONTEXT, IIIF_PRESENTATION_CONTEXT)
from openatlas.api.api_v1.util.files import (
    get_cached_file_path, get_iiif_redirect_url, get_license_item,
    get_license_type, has_file_access, iiif_file_exists,
    resolve_rights_holders)
from openatlas.database import overlay as db_overlay
from openatlas.display.image_processing import get_actual_mime
from openatlas.models.annotation import AnnotationImage
from openatlas.models.entity import Entity


@dataclass
class ManifestMetadata:
    items: list[dict[str, Any]] = field(default_factory=list)
    see_also: list[dict[str, Any]] = field(default_factory=list)
    license: LicenseItem | None = None
    attribution: str = ''


def get_url(entity: Entity) -> str:
    if resolver := g.settings.get('frontend_resolver_url'):
        return f'{resolver}{entity.id}'
    return url_for(  # pragma: no cover
        'api_v1_lod.get_entity',
        uuid=entity.uuid,
        _external=True)


def get_license_info(entity: Entity) -> LicenseItem | None:
    if type_ := get_license_type(entity):
        return get_license_item(type_)
    return None  # pragma: no cover


def convert_coordinates(coordinates_str: str) -> list[list[int]]:
    coordinates = [int(float(c)) for c in coordinates_str.split(',')]
    return [
        [coordinates[i], coordinates[i + 1]]
        for i in range(0, len(coordinates), 2)]


def generate_svg_path(coordinates: list[list[int]]) -> str:
    dwg = svgwrite.Drawing(size=('100%', '100%'))
    points = 'L'.join(f'{x},{y}' for x, y in coordinates)
    path = dwg.path(
        d=f'M{points}z',
        fill='none',
        stroke='#0d6efd',
        stroke_width=1)
    dwg.add(path)
    return dwg.tostring()


def calculate_bounding_box(
        coordinates: list[list[int]]) -> tuple[int, int, int, int]:
    x_values = [x for x, _ in coordinates]
    y_values = [y for _, y in coordinates]
    x = min(x_values)
    y = min(y_values)
    return x, y, max(x_values) - x, max(y_values) - y


def format_html_link(url: str, text: str) -> str:
    safe_text = str(escape(text))
    if urlparse(url).scheme.lower() not in {'http', 'https'}:
        return safe_text
    return (
        f'<a href="{escape(url)}" target="_blank" '
        f'rel="noopener noreferrer">{safe_text}</a>')


def get_overlay_corners(bounding_box: Any) -> list[list[float]] | None:
    # Overlays are stored as [latitude, longitude], GeoJSON needs [lon, lat]
    try:
        coordinates = (
            ast.literal_eval(bounding_box)
            if isinstance(bounding_box, str) else bounding_box)
        points = [(float(lat), float(lon)) for lat, lon in coordinates]
    except (SyntaxError, TypeError, ValueError):
        return None
    match points:
        case [(lat_a, lon_a), (lat_b, lon_b)]:  # Legacy bounds, any order
            north, south = max(lat_a, lat_b), min(lat_a, lat_b)
            west, east = min(lon_a, lon_b), max(lon_a, lon_b)
            return [[west, north], [east, north], [west, south]]
        case [_, _, _]:  # Top left, top right, bottom left
            return [[lon, lat] for lat, lon in points]
    return None


def _is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _fetch_image_info(entity_id: int, image_url: str) -> dict[str, Any]:
    try:
        resp = requests.get(
            f'{image_url}/info.json',
            proxies=app.config['PROXIES'],
            timeout=10)
        resp.raise_for_status()
        image_api = resp.json()
    except (requests.exceptions.RequestException, ValueError):
        abort_file_not_found(entity_id)
    if (not isinstance(image_api, dict)
            or not _is_positive_int(image_api.get('width'))
            or not _is_positive_int(image_api.get('height'))):
        abort_file_not_found(entity_id)
    return image_api


class IIIFBuilder:
    def __init__(self, entity: Entity) -> None:
        self.entity = entity
        self._annotation_entities: dict[int, Entity] = {}
        self.manifest_url = url_for(
            'api_v1_iiif.get_iiif_manifest',
            id=entity.id,
            _external=True)
        self.canvas_url = url_for(
            'api_v1_iiif.get_iiif_canvas',
            id=entity.id,
            _external=True)
        self.image_resource_url = url_for(
            'api_v1_iiif.get_iiif_image',
            id=entity.id,
            _external=True)
        self.annotation_list_url = url_for(
            'api_v1_iiif.get_iiif_annotation_list',
            id=entity.id,
            _external=True)
        self.georeference_url = url_for(
            'api_v1_iiif.get_iiif_georeference',
            id=entity.id,
            _external=True)

    @cached_property
    def image_metadata(self) -> tuple[str, dict[str, Any]]:
        if (not g.settings.get('iiif')
                or not g.settings.get('iiif_url')
                or not iiif_file_exists(self.entity.id)):
            abort_file_not_found(self.entity.id)
        if g.settings.get('iiif_conversion'):
            ext = '.tiff'
        elif file_path := get_cached_file_path(self.entity.id):
            ext = file_path.suffix
        else:  # pragma: no cover
            abort_file_not_found(self.entity.id)
        image_url = f"{g.settings.get('iiif_url', '')}{self.entity.id}{ext}"
        image_api = _fetch_image_info(self.entity.id, image_url)
        resolved = image_api.get('id') or image_api.get('@id')
        if isinstance(resolved, str) and resolved:
            image_url = resolved
        return image_url, image_api

    @property
    def image_url(self) -> str:
        return self.image_metadata[0]

    @property
    def image_api(self) -> dict[str, Any]:
        return self.image_metadata[1]

    @cached_property
    def image_service(self) -> dict[str, Any]:
        profile = self.image_api.get('profile')
        if isinstance(profile, list):
            profile = profile[0] if profile else ''
        return {
            'id': self.image_url,
            'type': 'ImageService2',
            'profile': profile}

    @cached_property
    def overlay_corners(self) -> list[list[float]] | None:
        overlays = db_overlay.get_by_object([self.entity.id])
        if not overlays:
            return None
        return get_overlay_corners(overlays[0]['bounding_box'])

    @cached_property
    def common_meta(self) -> ManifestMetadata:
        items = []
        lic = get_license_info(self.entity)
        attribution = lic.name if lic else ''
        rights = resolve_rights_holders([self.entity.id])[self.entity.id]
        if rights['license_holder']:
            holders = ', '.join(lh.name for lh in rights['license_holder'])
            attribution = (
                f'{attribution}, {holders}' if attribution else holders)

        if references := self.entity.get_links('P67', inverse=True):
            for reference in references:
                url = get_url(reference.domain)
                name = reference.domain.description or reference.domain.name
                text = (
                    f'{name}, {reference.description}'
                    if reference.description else name)
                items.append({
                    'label': _('source').capitalize(),
                    'value': format_html_link(url, text)})

        if rights['creator']:
            for creator in rights['creator']:
                items.append({
                    'label': _('creator').capitalize(),
                    'value': creator.name})

        see_also = []
        if related_entities := self.entity.get_links('P67'):
            for related_entity in related_entities:
                see_also.append({
                    'id': get_url(related_entity.range),
                    'label': related_entity.range.name.capitalize(),
                    'format': related_entity.range.class_.name.capitalize()})

        return ManifestMetadata(
            items=items,
            see_also=see_also,
            license=lic,
            attribution=attribution)

    @cached_property
    def site_provider(self) -> dict[str, Any]:
        site_url = url_for('overview', _external=True)
        site_name = g.settings.get('site_name') or 'OpenAtlas'
        provider: dict[str, Any] = {
            'id': site_url,
            'type': 'Agent',
            'label': {'en': [site_name]},
            'homepage': [{
                'id': site_url,
                'type': 'Text',
                'label': {'en': [site_name]},
                'format': 'text/html'}]}
        if logo := self.get_logo():
            provider['logo'] = [logo]
        return provider

    def preload_annotation_entities(
            self,
            annotations: list[AnnotationImage]) -> None:
        missing_ids = [
            id_ for id_ in {a.entity_id for a in annotations if a.entity_id}
            if id_ not in self._annotation_entities]
        if missing_ids:
            for entity in Entity.get_by_ids(missing_ids):
                self._annotation_entities[entity.id] = entity

    def get_annotation_details(
            self,
            annotation: AnnotationImage) -> tuple[str, str]:
        entity_link = ''
        if annotation.entity_id:
            if not (entity := self._annotation_entities.get(
                    annotation.entity_id)):
                entity = get_entity_by_id(
                    annotation.entity_id,
                    with_location=False)
                self._annotation_entities[entity.id] = entity
            entity_link = format_html_link(get_url(entity), entity.name)
        annotation_url = url_for(
            'api_v1_iiif.get_iiif_annotation',
            id=annotation.id,
            _external=True)
        return annotation_url, entity_link

    def get_selector(self, coordinates_str: str) -> dict[str, Any]:
        coordinates = convert_coordinates(coordinates_str)
        x, y, width, height = calculate_bounding_box(coordinates)

        return {
            'type': 'Choice',
            'default': {
                'type': 'FragmentSelector',
                'value': f'xywh={x},{y},{width},{height}'},
            'item': {
                'type': 'SvgSelector',
                'value': generate_svg_path(coordinates)}}

    def build_manifest(self) -> dict[str, Any]:
        v3_metadata = [{
            'label': {'en': [item['label']]},
            'value': {'en': [item['value']]}}
            for item in self.common_meta.items]
        v3_see_also = [{
            'id': sa['id'],
            'type': 'Dataset',
            'label': {'en': [sa['label']]},
            'format': sa['format']}
            for sa in self.common_meta.see_also]

        manifest: dict[str, Any] = {
            '@context': [
                IIIF_GEOREF_CONTEXT,
                IIIF_PRESENTATION_CONTEXT],
            'id': self.manifest_url,
            'type': 'Manifest',
            'label': {'en': [self.entity.name]},
            'metadata': v3_metadata,
            'items': [self.build_canvas(include_context=False)]}
        if self.entity.description:
            manifest['summary'] = {'en': [self.entity.description]}
        if self.common_meta.see_also:
            manifest['seeAlso'] = v3_see_also
        if self.common_meta.attribution:
            manifest['requiredStatement'] = {
                'label': {'en': ['Attribution']},
                'value': {'en': [self.common_meta.attribution]}}
        if self.common_meta.license and self.common_meta.license.url:
            manifest['rights'] = self.common_meta.license.url
        manifest['provider'] = [self.site_provider]

        return manifest

    def build_canvas(self, include_context: bool = True) -> dict[str, Any]:
        annotations_ = AnnotationImage.get_by_file_id(self.entity.id)
        canvas: dict[str, Any] = (
            {'@context': IIIF_PRESENTATION_CONTEXT}
            if include_context else {})
        canvas.update({
            'id': self.canvas_url,
            'type': 'Canvas',
            'label': {'en': [self.entity.name]},
            'height': self.image_api['height'],
            'width': self.image_api['width'],
            'items': [{
                'id': f'{self.canvas_url}#page-1',
                'type': 'AnnotationPage',
                'items': [self.build_image(include_context=False)]}],
            'thumbnail': [{
                'id': f'{self.image_url}/full/!200,200/0/default.jpg',
                'type': 'Image',
                'format': 'image/jpeg',
                'service': [self.image_service]}]})
        canvas_annotations = []
        if annotations_:
            self.preload_annotation_entities(annotations_)
            canvas_annotations.append({
                'id': self.annotation_list_url,
                'type': 'AnnotationPage',
                'items': [
                    self.build_annotation(a, include_context=False)
                    for a in annotations_]})
        if self.overlay_corners:
            canvas_annotations.append({
                'id': self.georeference_url,
                'type': 'AnnotationPage'})
        if canvas_annotations:
            canvas['annotations'] = canvas_annotations
        return canvas

    def build_georeference(self) -> dict[str, Any]:
        if not (coordinates := self.overlay_corners):
            abort_georeference_not_found(self.entity.id)
        width = self.image_api['width']
        height = self.image_api['height']
        resource_coordinates = [[0, 0], [width, 0], [0, height]]
        features = [{
            'type': 'Feature',
            'properties': {'resourceCoords': resource_coordinates_item},
            'geometry': {
                'type': 'Point',
                'coordinates': georeference_coords}}
            for resource_coordinates_item, georeference_coords
            in zip(resource_coordinates, coordinates, strict=True)]
        return {
            '@context': [
                IIIF_GEOREF_CONTEXT,
                IIIF_PRESENTATION_CONTEXT],
            'id': self.georeference_url,
            'type': 'AnnotationPage',
            'items': [{
                'id': f'{self.georeference_url}#annotation',
                'type': 'Annotation',
                'motivation': 'georeferencing',
                'target': {
                    'type': 'SpecificResource',
                    'source': {
                        **self.image_service,
                        'width': width,
                        'height': height,
                        'partOf': [{
                            'id': self.manifest_url,
                            'type': 'Manifest'}],
                        'provider': [self.site_provider]},
                    'selector': {
                        'type': 'SvgSelector',
                        'value': (
                            '<svg xmlns="http://www.w3.org/2000/svg" '
                            f'width="{width}" height="{height}">'
                            f'<polygon points="0,0 {width},0 '
                            f'{width},{height} 0,{height}" /></svg>')}},
                'body': {
                    'type': 'FeatureCollection',
                    'transformation': {
                        'type': 'polynomial',
                        'options': {'order': 1}},
                    'features': features}}]}

    def build_image(self, include_context: bool = True) -> dict[str, Any]:
        image: dict[str, Any] = (
            {'@context': IIIF_PRESENTATION_CONTEXT}
            if include_context else {})
        image.update({
            'id': self.image_resource_url,
            'type': 'Annotation',
            'motivation': 'painting',
            'body': {
                'id': f'{self.image_url}/full/full/0/default.jpg',
                'type': 'Image',
                'format': 'image/jpeg',
                'service': [self.image_service],
                'height': self.image_api['height'],
                'width': self.image_api['width']},
            'target': self.canvas_url})
        return image

    def build_annotation(
            self,
            annotation: AnnotationImage,
            include_context: bool = True) -> dict[str, Any]:
        annotation_url, entity_link = self.get_annotation_details(annotation)
        body = []
        if entity_link:
            body.append({
                'type': 'TextualBody',
                'value': entity_link,
                'format': 'text/html'})
        if annotation.text:
            body.append({
                'type': 'TextualBody',
                'value': annotation.text,
                'format': 'text/plain'})
        result: dict[str, Any] = (
            {'@context': IIIF_PRESENTATION_CONTEXT}
            if include_context else {})
        result.update({
            'id': annotation_url,
            'type': 'Annotation',
            'motivation': 'commenting',
            'body': body,
            'target': {
                'type': 'SpecificResource',
                'source': self.canvas_url,
                'selector': self.get_selector(annotation.coordinates)}})
        return result

    def build_annotation_list(self) -> dict[str, Any]:
        annotations_ = AnnotationImage.get_by_file_id(self.entity.id)
        self.preload_annotation_entities(annotations_)
        return {
            '@context': IIIF_PRESENTATION_CONTEXT,
            'id': self.annotation_list_url,
            'type': 'AnnotationPage',
            'items': [
                self.build_annotation(a, include_context=False)
                for a in annotations_]}

    def get_logo(self) -> dict[str, Any]:
        logo_id = g.settings.get('logo_file_id')
        if not logo_id or not str(logo_id).isdigit():
            return {}
        logo_int = int(logo_id)
        if not (logo_path := get_cached_file_path(logo_int)):
            return {}
        try:
            if self.entity.id == logo_int and has_file_access(self.entity):
                logo_entity = self.entity
            else:
                logo_entity = Entity.get_by_id(
                    logo_int,
                    types=True,
                    with_location=False)
        except ImATeapot:
            return {}
        if logo_entity.class_.name != 'file' or not has_file_access(
                logo_entity):
            return {}
        logo_url = url_for(
            'api_v1_files.display_file',
            id=logo_int,
            _external=True)
        logo_format = (
            'image/jpeg' if get_iiif_redirect_url(logo_int, logo_path)
            else get_actual_mime(logo_path))
        return {
            'id': logo_url,
            'type': 'Image',
            'format': logo_format}


def build_manifest(entity: Entity) -> dict[str, Any]:
    return IIIFBuilder(entity).build_manifest()


def build_canvas(entity: Entity) -> dict[str, Any]:
    return IIIFBuilder(entity).build_canvas()


def build_image(entity: Entity) -> dict[str, Any]:
    return IIIFBuilder(entity).build_image()


def build_annotation(
        annotation: AnnotationImage,
        entity: Entity | None = None) -> dict[str, Any]:
    image_entity = entity or get_entity_by_id(
        annotation.image_id,
        types=True,
        with_location=False)
    return IIIFBuilder(image_entity).build_annotation(annotation)


def build_annotation_list(entity: Entity) -> dict[str, Any]:
    return IIIFBuilder(entity).build_annotation_list()


def build_georeference(entity: Entity) -> dict[str, Any]:
    return IIIFBuilder(entity).build_georeference()
