from dataclasses import dataclass, field
from typing import Any, Tuple

import requests
import svgwrite
from flask import g, url_for, request
from flask_babel import gettext as _

from openatlas.api.api_v1.error_handlers import abort_file_not_found
from openatlas.api.api_v1.formatters.lod_util import get_license_type
from openatlas.display.image_processing import check_iiif_file_exist, \
    get_actual_mime
from openatlas.display.util2 import get_file_path
from openatlas.models.annotation import AnnotationImage
from openatlas.models.entity import Entity


@dataclass
class LicenseInfo:
    name: str = ''
    url: str = ''


@dataclass
class ManifestMetadata:
    items: list[dict[str, Any]] = field(default_factory=list)
    see_also: list[dict[str, Any]] = field(default_factory=list)
    license: LicenseInfo = field(default_factory=LicenseInfo)
    attribution: str = ''


def get_url(entity_id: int) -> str:
    if resolver := g.settings.get('frontend_resolver_url'):
        return f"{resolver}{entity_id}"
    try:
        return url_for('api_v1_lod.get_entity', id=entity_id, _external=True)
    except Exception:
        return f"{request.url_root}api/1/entity/{entity_id}"


def get_license_info(entity: Entity) -> LicenseInfo:
    if type_ := get_license_type(entity):
        license_name = type_.name
        license_url = ''
        for link_ in type_.get_links('P67', inverse=True):
            if link_.domain.class_.name == "external_reference":
                license_url = link_.domain.name
                break
        return LicenseInfo(name=license_name, url=license_url)
    return LicenseInfo()


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


class IIIFBuilder:
    def __init__(self, entity: Entity, version: int):
        self.entity = entity
        self.version = version
        self.manifest_url = url_for(
            'api_v1_files.get_iiif_manifest',
            id=entity.id,
            version=version,
            _external=True)
        self.canvas_url = url_for(
            'api_v1_files.get_iiif_canvas',
            id=entity.id,
            version=version,
            _external=True)
        self.image_resource_url = url_for(
            'api_v1_files.get_iiif_image',
            id=entity.id,
            version=version,
            _external=True)
        self.annotation_list_url = url_for(
            'api_v1_files.get_iiif_annotation_list',
            id=entity.id,
            version=version,
            _external=True)
        self.image_url, self.image_api = self._get_image_metadata()
        self.mime_type = get_actual_mime(get_file_path(entity.id))
        self.common_meta = self._get_common_metadata()

    def _get_image_metadata(self) -> Tuple[str, dict[str, Any]]:
        if self.entity.class_.group.get('name') != 'file' and \
                not check_iiif_file_exist(self.entity.id):
            abort_file_not_found(self.entity.id)
        ext = '.tiff' if g.settings.get('iiif_conversion') else \
            self.entity.get_file_ext()
        image_url = f"{g.settings.get('iiif_url', '')}{self.entity.id}{ext}"
        try:
            resp = requests.get(f"{image_url}/info.json", timeout=30)
            resp.raise_for_status()
        except Exception:
            abort_file_not_found(self.entity.id)
        return image_url, resp.json()

    def _get_common_metadata(self) -> ManifestMetadata:
        items = []
        lic = get_license_info(self.entity)
        attribution = lic.name
        if self.entity.license_holder:
            attribution = f"{attribution}, {', '.join([
                lh.name for lh in self.entity.license_holder])}"

        if references := self.entity.get_links('P67', inverse=True):
            for reference in references:
                url = get_url(reference.domain.id)
                name = reference.domain.description or reference.domain.name
                text = f"{name}, {reference.description}"
                items.append({
                    "label": _('source').capitalize(),
                    "value": f"<a href={url} target=_blank>{text}</a>"})

        if self.entity.creator:
            for c in self.entity.creator:
                items.append({
                    "label": _('creator').capitalize(),
                    "value": c.name})

        see_also = []
        if related_entities := self.entity.get_links('P67'):
            for related_entity in related_entities:
                see_also.append({
                    "id": get_url(related_entity.range.id),
                    "label": related_entity.range.name.capitalize(),
                    "format": related_entity.range.class_.name.capitalize()})

        return ManifestMetadata(
            items=items,
            see_also=see_also,
            license=lic,
            attribution=attribution)

    def build_manifest(self) -> dict[str, Any]:
        raise NotImplementedError

    def build_canvas(self) -> dict[str, Any]:
        raise NotImplementedError

    def build_image(self) -> dict[str, Any]:
        raise NotImplementedError

    def build_annotation(
            self,
            annotation: AnnotationImage) -> dict[str, Any]:
        raise NotImplementedError

    def get_logo(self) -> dict[str, Any]:
        raise NotImplementedError

    def get_selector(self, coordinates_str: str) -> dict[str, Any]:
        coordinates = convert_coordinates(coordinates_str)
        x, y, width, height = calculate_bounding_box(coordinates)

        if self.version == 3:
            return {
                "type": "Choice",
                "default": {
                    "type": "FragmentSelector",
                    "value": f"xywh={x},{y},{width},{height}"},
                "item": {
                    "type": "SvgSelector",
                    "value": generate_svg_path(coordinates)}}

        return {
            "default": {
                "@type": "oa:FragmentSelector",
                "value": f"xywh={x},{y},{width},{height}"},
            "item": {
                "@type": "oa:SvgSelector",
                "value": generate_svg_path(coordinates)},
            "@type": "oa:Choice"}


class V2Builder(IIIFBuilder):
    def build_manifest(self) -> dict[str, Any]:
        v2_see_also = [
            {"@id": sa["id"], "label": sa["label"], "format": sa["format"]}
            for sa in self.common_meta.see_also]

        return {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": self.manifest_url,
            "@type": "sc:Manifest",
            "label": self.entity.name,
            "description": [{"@value": self.entity.description,
                             "@language": "en"}] \
                if self.entity.description else "",
            "metadata": self.common_meta.items,
            "seeAlso": v2_see_also,
            "attribution": self.common_meta.attribution,
            "license": self.common_meta.license.url,
            "logo": self.get_logo(),
            "sequences": [{
                "@id": f"{self.manifest_url}/sequence/normal",
                "@type": "sc:Sequence",
                "canvases": [self.build_canvas()]}]}

    def build_canvas(self) -> dict[str, Any]:
        return {
            "@id": self.canvas_url,
            "@type": "sc:Canvas",
            "label": self.entity.name,
            "height": self.image_api['height'],
            "width": self.image_api['width'],
            "description": "",
            "images": [self.build_image()],
            "otherContent": [{
                "@id": self.annotation_list_url,
                "@type": "sc:AnnotationList"}],
            "thumbnail": {
                "@id": f"{self.image_url}/full/!200,200/0/default.jpg",
                "@type": "dctypes:Image",
                "format": self.mime_type,
                "height": 200,
                "width": 200,
                "service": {
                    "@context": "http://iiif.io/api/image/2/context.json",
                    "@id": self.image_url,
                    "profile": self.image_api['profile']}}}

    def build_image(self) -> dict[str, Any]:
        return {
            "@id": self.image_resource_url,
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "resource": {
                "@id": self.image_url,
                "@type": "dctypes:Image",
                "format": self.mime_type,
                "service": {
                    "@context": "http://iiif.io/api/image/2/context.json",
                    "@id": self.image_url,
                    "profile": self.image_api['profile']},
                "height": self.image_api['height'],
                "width": self.image_api['width']},
            "on": self.canvas_url}

    def build_annotation(
            self,
            annotation: AnnotationImage) -> dict[str, Any]:
        entity_link = ''
        if annotation.entity_id:
            entity = Entity.get_by_id(annotation.entity_id)
            if entity:
                url = get_url(entity.id)
                entity_link = f'<a href={url} target=_blank>{entity.name}</a>'

        annotation_url = url_for(
            'files.get_iiif_annotation',
            id=annotation.id,
            version=self.version,
            _external=True)

        return {
            "@id": annotation_url,
            "@type": "oa:Annotation",
            "motivation": ["oa:commenting"],
            "resource": [{
                "@type": "dctypes:Dataset",
                "chars": entity_link,
                "format": "text/html"}, {
                "@type": "dctypes:Text",
                "chars": annotation.text,
                "format": "text/plain"}],
            "on": {
                "@type": "oa:SpecificResource",
                "full": self.canvas_url,
                "selector": self.get_selector(annotation.coordinates),
                "within": {
                    "@id": self.manifest_url,
                    "@type": "sc:Manifest"}}}

    def get_logo(self) -> dict[str, Any]:
        logo_id = url_for(
            'files.display_file',
            id=g.settings.get('logo_file_id', 0),
            _external=True)
        return {
            "@id": logo_id,
            "service": {
                "@context": "http://iiif.io/api/image/2/context.json",
                "@id": url_for('overview', _external=True),
                "profile": "http://iiif.io/api/image/2/level2.json"}}


class V3Builder(IIIFBuilder):
    def build_manifest(self) -> dict[str, Any]:
        v3_metadata = [{
            "label": {"en": [item["label"]]},
             "value": {"en": [item["value"]]}} \
            for item in self.common_meta.items]
        v3_see_also = [{
            "id": sa["id"],
            "type": "Dataset",
            "label": {"en": [sa["label"]]},
            "format": sa["format"]} for sa in self.common_meta.see_also]

        manifest = {
            "@context": "http://iiif.io/api/presentation/3/context.json",
            "id": self.manifest_url,
            "type": "Manifest",
            "label": {"en": [self.entity.name]},
            "metadata": v3_metadata,
            "items": [self.build_canvas()]}

        if self.entity.description:
            manifest["summary"] = {"en": [self.entity.description]}
        if self.common_meta.see_also:
            manifest["seeAlso"] = v3_see_also
        if self.common_meta.attribution:
            manifest["requiredStatement"] = {
                "label": {"en": ["Attribution"]},
                "value": {"en": [self.common_meta.attribution]}}
        if self.common_meta.license.url:
            manifest["rights"] = self.common_meta.license.url
        if g.settings.get('logo_file_id'):
            manifest["provider"] = [{
                "id": url_for('overview', _external=True),
                "type": "Agent",
                "label": {"en": ["Provider"]},
                "logo": [self.get_logo()]}]

        return manifest

    def build_canvas(self) -> dict[str, Any]:
        annotations_ = AnnotationImage.get_by_file_id(self.entity.id)
        canvas = {
            "id": self.canvas_url,
            "type": "Canvas",
            "label": {"en": [self.entity.name]},
            "height": self.image_api['height'],
            "width": self.image_api['width'],
            "items": [{
                "id": f"{self.canvas_url}/annotation_page/1",
                "type": "AnnotationPage",
                "items": [self.build_image()]}],
            "thumbnail": [{
                "id": f"{self.image_url}/full/!200,200/0/default.jpg",
                "type": "Image",
                "format": self.mime_type,
                "service": [{
                    "id": self.image_url,
                    "type": "ImageService3",
                    "profile": "level2"}]}]}
        if annotations_:
            canvas["annotations"] = [{
                "id": self.annotation_list_url,
                "type": "AnnotationPage",
                "items": [
                    self.build_annotation(a) for a in annotations_]}]
        return canvas

    def build_image(self) -> dict[str, Any]:
        return {
            "id": self.image_resource_url,
            "type": "Annotation",
            "motivation": "painting",
            "body": {
                "id": self.image_url,
                "type": "Image",
                "format": self.mime_type,
                "service": [{
                    "id": self.image_url,
                    "type": "ImageService3",
                    "profile": "level2"}],
                "height": self.image_api['height'],
                "width": self.image_api['width']},
            "target": self.canvas_url}

    def build_annotation(
            self,
            annotation: AnnotationImage) -> dict[str, Any]:
        entity_link = ''
        if annotation.entity_id:
            entity = Entity.get_by_id(annotation.entity_id)
            if entity:
                url = get_url(entity.id)
                entity_link = f'<a href={url} target=_blank>{entity.name}</a>'

        annotation_url = url_for(
            'files.get_iiif_annotation',
            id=annotation.id,
            version=self.version,
            _external=True)

        return {
            "id": annotation_url,
            "type": "Annotation",
            "motivation": "commenting",
            "body": [{
                "type": "Dataset",
                "value": entity_link,
                "format": "text/html"}, {
                "type": "TextualBody",
                "value": annotation.text,
                "format": "text/plain"}],
            "target": {
                "source": self.canvas_url,
                "selector": self.get_selector(annotation.coordinates)}}

    def get_logo(self) -> dict[str, Any]:
        logo_id = url_for(
            'files.display_file',
            id=g.settings.get('logo_file_id', 0),
            _external=True)
        return {
            "id": logo_id,
            "type": "Image",
            "format": "image/jpeg",
            "service": [{
                "id": url_for('overview', _external=True),
                "type": "ImageService3",
                "profile": "level2"}]}


def build_manifest_v2(entity: Entity) -> dict[str, Any]:
    return V2Builder(entity, version=2).build_manifest()


def build_manifest_v3(entity: Entity) -> dict[str, Any]:
    return V3Builder(entity, version=3).build_manifest()


def build_canvas(entity: Entity, version: int = 2) -> dict[str, Any]:
    builder = V3Builder(entity, 3) if version == 3 else V2Builder(entity, 2)
    return builder.build_canvas()


def build_image(entity: Entity, version: int = 2) -> dict[str, Any]:
    builder = V3Builder(entity, 3) if version == 3 else V2Builder(entity, 2)
    return builder.build_image()


def build_annotation(
        annotation: AnnotationImage,
        version: int = 2) -> dict[str, Any]:
    entity = Entity.get_by_id(annotation.image_id)
    builder = V3Builder(entity, 3) if version == 3 else V2Builder(entity, 2)
    return builder.build_annotation(annotation)


def build_annotation_list(entity: Entity, version: int = 2) -> dict[str, Any]:
    annotations_ = AnnotationImage.get_by_file_id(entity.id)
    builder = V3Builder(entity, 3) if version == 3 else V2Builder(entity, 2)

    if version == 3:
        return {
            "id": builder.annotation_list_url,
            "type": "AnnotationPage",
            "items": [builder.build_annotation(a) for a in annotations_]}

    return {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": builder.annotation_list_url,
        "@type": "sc:AnnotationList",
        "resources": [builder.build_annotation(a) for a in annotations_]}
