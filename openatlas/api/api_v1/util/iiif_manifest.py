import ast
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any

import requests
import svgwrite
from flask import g, url_for
from flask_babel import gettext as _

from openatlas.api.api_v1.entity import get_entity_by_id
from openatlas.api.api_v1.error_handlers import (
    abort_file_not_found, abort_not_found)
from openatlas.api.api_v1.models.files import LicenseItem
from openatlas.api.api_v1.util.files import (
    get_cached_file_path, get_license_item, get_license_type, iiif_file_exists,
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


class IIIFBuilder:
    def __init__(self, entity: Entity) -> None:
        self.entity = entity
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
        self.file_path = get_cached_file_path(entity.id)

    @cached_property
    def image_metadata(self) -> tuple[str, dict[str, Any]]:
        if (self.entity.class_.group.get('name') != 'file'
                and not iiif_file_exists(self.entity.id)):
            abort_file_not_found(self.entity.id)  # pragma: no cover
        ext = (
            '.tiff' if g.settings.get('iiif_conversion')
            else (self.file_path.suffix if self.file_path else 'N/A'))
        image_url = f"{g.settings.get('iiif_url', '')}{self.entity.id}{ext}"
        try:
            resp = requests.get(f'{image_url}/info.json', timeout=30)
            resp.raise_for_status()
        except Exception:  # pragma: no cover
            abort_file_not_found(self.entity.id)
        image_api = resp.json()
        image_url = image_api.get('id') or image_api.get('@id') or image_url
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

    def overlay_corners(self) -> list[list[float]] | None:
        overlays = db_overlay.get_by_object([self.entity.id])
        if not overlays:
            return None
        return get_overlay_corners(overlays[0]['bounding_box'])

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
                    'value': f'<a href={url} target=_blank>{text}</a>'})

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

    def get_annotation_details(
            self,
            annotation: AnnotationImage) -> tuple[str, str]:
        entity_link = ''
        if annotation.entity_id:
            entity = get_entity_by_id(annotation.entity_id)
            url = get_url(entity)
            entity_link = f'<a href={url} target=_blank>{entity.name}</a>'
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
                'https://iiif.io/api/extension/georef/1/context.json',
                'https://iiif.io/api/presentation/3/context.json'],
            'id': self.manifest_url,
            'type': 'Manifest',
            'label': {'en': [self.entity.name]},
            'metadata': v3_metadata,
            'items': [self.build_canvas()]}
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

    def build_canvas(self) -> dict[str, Any]:
        annotations_ = AnnotationImage.get_by_file_id(self.entity.id)
        canvas: dict[str, Any] = {
            '@context': 'https://iiif.io/api/presentation/3/context.json',
            'id': self.canvas_url,
            'type': 'Canvas',
            'label': {'en': [self.entity.name]},
            'height': self.image_api['height'],
            'width': self.image_api['width'],
            'items': [{
                'id': f'{self.canvas_url}#page-1',
                'type': 'AnnotationPage',
                'items': [self.build_image()]}],
            'thumbnail': [{
                'id': f'{self.image_url}/full/!200,200/0/default.jpg',
                'type': 'Image',
                'format': 'image/jpeg',
                'service': [self.image_service]}]}
        canvas_annotations = []
        if annotations_:
            canvas_annotations.append({
                'id': self.annotation_list_url,
                'type': 'AnnotationPage',
                'items': [
                    self.build_annotation(a) for a in annotations_]})
        if self.overlay_corners:
            canvas_annotations.append({
                'id': self.georeference_url,
                'type': 'AnnotationPage'})
        if canvas_annotations:
            canvas['annotations'] = canvas_annotations
        return canvas

    def build_georeference(self) -> dict[str, Any]:
        if not (coordinates := self.overlay_corners):
            abort_not_found(self.entity.id)
        width = self.image_api['width']
        height = self.image_api['height']
        resource_coordinates = [[0, 0], [width, 0], [0, height]]
        features = [{
            'type': 'Feature',
            'properties': {'resourceCoords': resource_coords},
            'geometry': {
                'type': 'Point',
                'coordinates': georeference_coords}}
            for resource_coords, georeference_coords
            in zip(resource_coordinates, coordinates, strict=True)]
        return {
            '@context': [
                'https://iiif.io/api/extension/georef/1/context.json',
                'https://iiif.io/api/presentation/3/context.json'],
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
                            f'<svg width="{width}" height="{height}">'
                            f'<polygon points="0,0 {width},0 '
                            f'{width},{height} 0,{height}" /></svg>')}},
                'body': {
                    'type': 'FeatureCollection',
                    'transformation': {
                        'type': 'polynomial',
                        'options': {'order': 1}},
                    'features': features}}]}

    def build_image(self) -> dict[str, Any]:
        return {
            '@context': 'https://iiif.io/api/presentation/3/context.json',
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
            'target': self.canvas_url}

    def build_annotation(
            self,
            annotation: AnnotationImage) -> dict[str, Any]:
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
        return {
            '@context': 'https://iiif.io/api/presentation/3/context.json',
            'id': annotation_url,
            'type': 'Annotation',
            'motivation': 'commenting',
            'body': body,
            'target': {
                'type': 'SpecificResource',
                'source': self.canvas_url,
                'selector': self.get_selector(annotation.coordinates)}}

    def get_logo(self) -> dict[str, Any]:
        logo_id = g.settings.get('logo_file_id')
        if not logo_id or not str(logo_id).isdigit():
            return {}  # pragma: no cover
        if not (logo_path := get_cached_file_path(int(logo_id))):
            return {}  # pragma: no cover
        logo_url = url_for(
            'api_v1_files.display_file',
            id=int(logo_id),
            _external=True)
        return {
            'id': logo_url,
            'type': 'Image',
            'format': get_actual_mime(logo_path)}


def build_manifest(entity: Entity) -> dict[str, Any]:
    return IIIFBuilder(entity).build_manifest()


def build_canvas(entity: Entity) -> dict[str, Any]:
    return IIIFBuilder(entity).build_canvas()


def build_image(entity: Entity) -> dict[str, Any]:
    return IIIFBuilder(entity).build_image()


def build_annotation(annotation: AnnotationImage) -> dict[str, Any]:
    entity = get_entity_by_id(annotation.image_id)
    return IIIFBuilder(entity).build_annotation(annotation)


def build_annotation_list(entity: Entity) -> dict[str, Any]:
    annotations_ = AnnotationImage.get_by_file_id(entity.id)
    builder = IIIFBuilder(entity)
    return {
        '@context': 'https://iiif.io/api/presentation/3/context.json',
        'id': builder.annotation_list_url,
        'type': 'AnnotationPage',
        'items': [builder.build_annotation(a) for a in annotations_]}


def build_georeference(entity: Entity) -> dict[str, Any]:
    return IIIFBuilder(entity).build_georeference()
