from dataclasses import dataclass
from typing import Any, Tuple

import requests
import svgwrite
from flask import g, url_for, request
from flask_babel import gettext as _

from openatlas.api.api_v1.error_handlers import abort_file_not_found
from openatlas.display.image_processing import check_iiif_file_exist, get_actual_mime
from openatlas.display.util2 import get_file_path
from openatlas.models.annotation import AnnotationImage
from openatlas.models.entity import Entity


def get_url(entity_id: int) -> str:
    if resolver := g.settings.get('frontend_resolver_url'):
        return f"{resolver}{entity_id}"
    try:
        return url_for('api_v1.get_entity', id=entity_id, _external=True)
    except Exception:
        return f"{request.url_root}api/1/entity/{entity_id}"


def get_license_name(entity: Entity) -> str:
    for type_ in entity.types:
        if type_.root and g.types.get(type_.root[0]) \
                and g.types[type_.root[0]].name == 'License':
            return type_.name
    return ''


def get_license_url(entity: Entity) -> str:
    for type_ in entity.types:
        if type_.root and g.types.get(type_.root[0]) \
                and g.types[type_.root[0]].name == 'License':
            for link_ in type_.get_links('P67', inverse=True):
                if link_.domain.class_.name == "external_reference":
                    return link_.domain.name
            break
    return ''


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


def generate_selector(
        coordinates_str: str,
        version: int = 2) -> dict[str, Any]:
    coordinates = convert_coordinates(coordinates_str)
    x, y, width, height = calculate_bounding_box(coordinates)
    
    if version == 3:
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


def get_metadata(entity: Entity) -> dict[str, Any]:
    if entity.class_.group.get('name') != 'file' and not check_iiif_file_exist(entity.id):
        abort_file_not_found(entity.id)
    ext = '.tiff' if g.settings.get('iiif_conversion') else entity.get_file_ext()
    image_url = f"{g.settings.get('iiif_url', '')}{entity.id}{ext}"

    try:
        resp = requests.get(f"{image_url}/info.json", timeout=30)
        resp.raise_for_status()
    except Exception:
        abort_file_not_found(entity.id)

    return {'entity': entity, 'img_url': image_url, 'img_api': resp.json()}


def get_logo(version: int = 2) -> dict[str, Any]:
    logo_id = url_for(
        'files.display_file',
        id=g.settings.get('logo_file_id', 0),
        _external=True)
    if version == 3:
        return {
            "id": logo_id,
            "type": "Image",
            "format": "image/jpeg",
            "service": [{
                "id": url_for('overview', _external=True),
                "type": "ImageService3",
                "profile": "level2"}]}
    return {
        "@id": logo_id,
        "service": {
            "@context": "http://iiif.io/api/image/2/context.json",
            "@id": url_for('overview', _external=True),
            "profile": "http://iiif.io/api/image/2/level2.json"}}


@dataclass
class ManifestMetadata:
    items: list[dict[str, Any]]
    see_also: list[dict[str, Any]]
    license_name: str
    license_url: str

def _get_common_metadata(entity: Entity) -> ManifestMetadata:
    metadata = []
    license_ = get_license_name(entity)
    if entity.license_holder:
        license_ = f"{license_}, {', '.join([
            lh.name for lh in entity.license_holder])}"
        
    if references := entity.get_links('P67', inverse=True):
        for reference in references:
            url = get_url(reference.domain.id)
            name = reference.domain.name
            if reference.domain.description:
                name = reference.domain.description
            text = f"{name}, {reference.description}"
            metadata.append({
                "label": _('source').capitalize(),
                "value": f"<a href={url} target=_blank>{text}</a>"})
                
    if entity.creator:
        for c in entity.creator:
            metadata.append({
                "label": _('creator').capitalize(),
                "value": c.name})
                
    see_also = []
    if related_entities := entity.get_links('P67'):
        for related_entity in related_entities:
            see_also.append({
                "id": get_url(related_entity.range.id),
                "label": related_entity.range.name.capitalize(),
                "format": related_entity.range.class_.name.capitalize()})
                
    return ManifestMetadata(
        items=metadata,
        see_also=see_also,
        license_name=license_,
        license_url=get_license_url(entity))


def build_annotation(
        annotation: AnnotationImage,
        version: int = 2) -> dict[str, Any]:
    entity_link = ''
    if annotation.entity_id:
        entity = Entity.get_by_id(annotation.entity_id)
        if entity:
            url = get_url(entity.id)
            entity_link = f'<a href={url} target=_blank>{entity.name}</a>'
            
    manifest_url = url_for(
        'files.get_iiif_manifest',
        id=annotation.image_id,
        version=version, _external=True)

    canvas_url = f"{manifest_url}/canvas/{annotation.image_id}"
    
    if version == 3:
        return {
            "id": f"{manifest_url}/annotation/{annotation.id}",
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
                "source": canvas_url,
                "selector": generate_selector(
                    annotation.coordinates, version=3)}}
    
    return {
        "@id": f"{manifest_url}/annotation/{annotation.id}",
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
            "full": canvas_url,
            "selector": generate_selector(annotation.coordinates, version=2),
            "within": {
                "@id": manifest_url,
                "@type": "sc:Manifest"}}}


def build_image(metadata: dict[str, Any], version: int = 2) -> dict[str, Any]:
    id_ = metadata['entity'].id
    mime_type = get_actual_mime(get_file_path(id_))
    manifest_url = url_for(
        'files.get_iiif_manifest',
        id=id_,
        version=version,
        _external=True)
    canvas_url = f"{manifest_url}/canvas/{id_}"
    
    if version == 3:
        return {
            "id": f"{manifest_url}/image/{id_}",
            "type": "Annotation",
            "motivation": "painting",
            "body": {
                "id": metadata['img_url'],
                "type": "Image",
                "format": mime_type,
                "service": [{
                    "id": metadata['img_url'],
                    "type": "ImageService3",
                    "profile": "level2"}],
                "height": metadata['img_api']['height'],
                "width": metadata['img_api']['width']},
            "target": canvas_url}
    
    return {
        "@id": f"{manifest_url}/image/{id_}",
        "@type": "oa:Annotation",
        "motivation": "sc:painting",
        "resource": {
            "@id": metadata['img_url'],
            "@type": "dctypes:Image",
            "format": mime_type,
            "service": {
                "@context": "http://iiif.io/api/image/2/context.json",
                "@id": metadata['img_url'],
                "profile": metadata['img_api']['profile']},
            "height": metadata['img_api']['height'],
            "width": metadata['img_api']['width']},
        "on": canvas_url}


def build_canvas(metadata: dict[str, Any], version: int = 2) -> dict[str, Any]:
    entity = metadata['entity']
    mime_type = get_actual_mime(get_file_path(entity.id))
    manifest_url = url_for(
        'files.get_iiif_manifest',
        id=entity.id,
        version=version,
        _external=True)
    
    if version == 3:
        annotations_ = AnnotationImage.get_by_file_id(entity.id)
        canvas = {
            "id": f"{manifest_url}/canvas/{entity.id}",
            "type": "Canvas",
            "label": {"en": [entity.name]},
            "height": metadata['img_api']['height'],
            "width": metadata['img_api']['width'],
            "items": [{
                "id": f"{manifest_url}/canvas/{entity.id}/annotation_page/1",
                "type": "AnnotationPage",
                "items": [build_image(metadata, version=3)]}],
            "thumbnail": [{
                "id": f"{metadata['img_url']}/full/!200,200/0/default.jpg",
                "type": "Image",
                "format": mime_type,
                "service": [{
                    "id": metadata['img_url'],
                    "type": "ImageService3",
                    "profile": "level2"}]}]}
        if annotations_:
            canvas["annotations"] = [{
                "id": f"{manifest_url}/annotation_page/{entity.id}",
                "type": "AnnotationPage",
                "items": [
                    build_annotation(a, version=3) for a in annotations_]}]
        return canvas

    canvas = {
        "@id": f"{manifest_url}/canvas/{entity.id}",
        "@type": "sc:Canvas",
        "label": entity.name,
        "height": metadata['img_api']['height'],
        "width": metadata['img_api']['width'],
        "description": "",
        "images": [build_image(metadata, version=2)],
        "otherContent": [{
            "@id": f"{manifest_url}/annotation_list/{entity.id}",
            "@type": "sc:AnnotationList"}],
        "thumbnail": {
            "@id": f"{metadata['img_url']}/full/!200,200/0/default.jpg",
            "@type": "dctypes:Image",
            "format": mime_type,
            "height": 200,
            "width": 200,
            "service": {
                "@context": "http://iiif.io/api/image/2/context.json",
                "@id": metadata['img_url'],
                "profile": metadata['img_api']['profile']}}}
    return canvas


def build_manifest_v2(entity: Entity) -> dict[str, Any]:
    meta = _get_common_metadata(entity)
    manifest_url = url_for(
        'files.get_iiif_manifest',
        id=entity.id,
        version=2,
        _external=True)

    v2_see_also = [
        {"@id": sa["id"], "label": sa["label"], "format": sa["format"]}
        for sa in meta.see_also]
    
    return {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": manifest_url,
        "@type": "sc:Manifest",
        "label": entity.name,
        "description": [{"@value": entity.description, "@language": "en"}] \
            if entity.description else "",
        "metadata": meta.items,
        "seeAlso": v2_see_also,
        "attribution": meta.license_name,
        "license": meta.license_url,
        "logo": get_logo(version=2),
        "sequences": [{
            "@id": f"{manifest_url}/sequence/normal",
            "@type": "sc:Sequence",
            "canvases": [build_canvas(get_metadata(entity), version=2)]}]}


def build_manifest_v3(entity: Entity) -> dict[str, Any]:
    meta = _get_common_metadata(entity)
    manifest_url = url_for(
        'files.get_iiif_manifest',
        id=entity.id,
        version=3,
        _external=True)
    
    v3_metadata = [
        {"label": {"en": [item["label"]]}, "value": {"en": [item["value"]]}} \
        for item in meta.items]
    v3_see_also = [{
        "id": sa["id"],
        "type": "Dataset",
        "label": {"en": [sa["label"]]},
        "format": sa["format"]} for sa in meta.see_also]
    
    manifest = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": manifest_url,
        "type": "Manifest",
        "label": {"en": [entity.name]},
        "metadata": v3_metadata,
        "items": [build_canvas(get_metadata(entity), version=3)]}
        
    if entity.description:
        manifest["summary"] = {"en": [entity.description]}
    if meta.see_also:
        manifest["seeAlso"] = v3_see_also
    if meta.license_name:
        manifest["requiredStatement"] = {
            "label": {"en": ["Attribution"]},
            "value": {"en": [meta.license_name]}}
    if meta.license_url:
        manifest["rights"] = meta.license_url
    if g.settings.get('logo_file_id'):
        manifest["provider"] = [{
            "id": url_for('overview', _external=True),
            "type": "Agent",
            "label": {"en": ["Provider"]},
            "logo": [get_logo(version=3)]}]
            
    return manifest
