import functools
import json
import pathlib
import re
from collections import defaultdict
from collections.abc import Callable
from typing import Any, Optional
from uuid import UUID

from flask import Response, g, request, url_for
from rdflib import Graph

from openatlas import app
from openatlas.api.api_v1.entity import (
    get_by_system_class, get_count_by_system_class)
from openatlas.api.api_v1.error_handlers import abort_not_found
from openatlas.api.api_v1.util.pagination import get_pagination_lod
from openatlas.database.api import get_wkts_by_ids
from openatlas.display.image_processing import (
    check_iiif_activation, check_iiif_file_exist)
from openatlas.models.entity import Entity, Link


_DATE_PARTS_RE = re.compile(
    r'^(-?\d{4,})-(\d{2})-(\d{2})'
    r'(?:[T ](\d{2}):(\d{2}):(\d{2})(?:\.\d+)?)?Z?$')


def date_to_utc_iso_str(date: Any) -> str | None:
    if not date:
        return None
    match = _DATE_PARTS_RE.match(str(date))
    if not match:
        return str(date)
    year, month, day, hour, minute, second = match.groups()
    if hour and (int(hour) or int(minute) or int(second)):
        return f'{year}-{month}-{day}T{hour}:{minute}:{second}Z'
    return f'{year}-{month}-{day}'


def get_license_type(entity: Entity) -> Optional[Entity]:
    license_ = None
    for type_ in entity.types:
        if g.types[type_.root[0]].name == 'License':
            license_ = type_
            break
    return license_


def get_iiif_manifest_and_path(img_id: int) -> dict[str, str]:
    iiif_manifest = ''
    iiif_base_path = ''
    if check_iiif_activation() and check_iiif_file_exist(img_id):
        iiif_manifest = url_for(
            'api.iiif_manifest',
            version=g.settings['iiif_version'],
            id_=img_id,
            _external=True)
        if g.files.get(img_id):
            iiif_base_path = (
                f"{g.settings['iiif_url']}{img_id}{g.files[img_id].suffix}")
    return {'IIIFManifest': iiif_manifest, 'IIIFBasePath': iiif_base_path}


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def remove_spaces_dashes(string: str) -> str:
    return string.replace(' ', '').replace('-', '')


def get_links_for_entities(entities: list[Entity]) -> dict[Any, Any]:
    entities_with_links = {}
    preloaded = {e.id: e for e in entities}
    preloaded.update(g.types)
    preloaded.update(g.reference_systems)

    for entity in entities:
        entities_with_links[entity.id] = {
            'entity': entity,
            'links': [],
            'links_inverse': [],
            'geometries': {}}

    geom_ids = set(e.id for e in entities)
    for link_ in Entity.get_links_of_entities(
            [entity.id for entity in entities],
            preloaded_entities=preloaded):
        entities_with_links[link_.domain.id]['links'].append(link_)
        preloaded[link_.range.id] = link_.range
        if link_.property.code == 'P53':
            geom_ids.add(link_.range.id)

    for link_ in Entity.get_links_of_entities(
            [entity.id for entity in entities],
            inverse=True,
            preloaded_entities=preloaded):
        entities_with_links[link_.range.id]['links_inverse'].append(link_)
        preloaded[link_.domain.id] = link_.domain

    if geom_ids:
        wkts = get_wkts_by_ids(list(geom_ids))
        for id_ in entities_with_links:
            entities_with_links[id_]['geometries'] = wkts

    return entities_with_links


def get_type_references() -> dict[int, list[Link]]:
    if hasattr(g, 'type_references'):
        return g.type_references

    type_links = Entity.get_links_of_entities(
        list(g.types.keys()),
        'P67',
        inverse=True,
        preloaded_entities=g.types)

    out: dict[int, list[Link]] = defaultdict(list)
    for link_ in type_links:
        if link_.domain.class_.name in \
                ['external_reference', 'reference_system']:
            out[link_.range.id].append(link_)

    g.type_references = out
    return out


@functools.lru_cache
def get_lod_context() -> dict[str, Any]:
    file_path = pathlib.Path(app.root_path) / 'api' / 'linked-art.json'
    with file_path.open('r', encoding='utf-8') as f:
        return json.load(f)


@functools.lru_cache
def parse_lod_context() -> dict[str, str]:
    context = get_lod_context().get('@context', {})
    inverted: dict[str, str] = {}
    for term, definition in context.items():
        if not isinstance(definition, dict):
            continue
        inverted[definition['@id']] = term
        for nested_term, nested_def in definition.get('@context', {}).items():
            if isinstance(nested_def, dict):
                inverted[nested_def['@id']] = nested_term
    return inverted


def set_accept_header(extension: str | None = None) -> None:
    if not extension:
        return
    ext_map = {
        'json': 'application/ld+json',
        'ttl': 'text/turtle',
        'xml': 'application/rdf+xml',
        'nt': 'application/n-triples'}
    if extension in ext_map:
        request.environ['HTTP_ACCEPT'] = ext_map[extension]


def make_lod_response(data: dict[str, Any]) -> Response:
    accepted = request.accept_mimetypes.best_match(app.config['LOD_HEADER'])
    json_str = app.json.dumps(data)
    if accepted not in [
        'text/turtle', 'application/rdf+xml', 'application/n-triples']:
        return Response(json_str, mimetype='application/ld+json')

    graph = Graph()
    graph.parse(data=json_str, format='json-ld')

    match accepted:
        case 'text/turtle':
            turtle_output = graph.serialize(format='turtle')
            return Response(turtle_output, mimetype='text/turtle')

        case 'application/rdf+xml':
            xml_output = graph.serialize(format='xml')
            return Response(xml_output, mimetype='application/rdf+xml')

        case 'application/n-triples':
            nt_output = graph.serialize(format='nt')
            return Response(nt_output, mimetype='application/n-triples')


def get_entity_response(
        entity_id: UUID,
        formatter: Callable[[Entity], dict[str, Any]],
        ext: str | None = None) -> dict[str, Any] | Response:
    entity = Entity.get_by_uuid(entity_id, types=True, aliases=True)
    if not entity:
        abort_not_found(entity_id)
    if ext:
        set_accept_header(ext)
    return make_lod_response(formatter(entity))


def get_entities_response(
        path: Any,
        query: Any,
        endpoint: str,
        formatter: Callable[..., dict[str, Any]]) -> dict[str, Any] | Response:
    entity_class_name = (
        path.entity_class.value
        if hasattr(path.entity_class, 'value') else str(path.entity_class))

    order_by = f'{query.sort_by}_{query.sort}'
    offset = (query.page - 1) * query.limit

    filter_kwargs = {
        'search': query.search,
        'start_date': query.start_date,
        'end_date': query.end_date,
        'type_id': query.type_id,
        'case_study': query.case_study}

    total_items = get_count_by_system_class(
        entity_class_name,
        **filter_kwargs)
    entities = get_by_system_class(
        entity_class_name,
        order_by=order_by,
        limit=query.limit,
        offset=offset,
        **filter_kwargs)

    pagination = get_pagination_lod(
        endpoint,
        total_items=total_items,
        page=query.page,
        limit=query.limit,
        entity_class=entity_class_name)

    return make_lod_response(
        formatter(entities, pagination=pagination))
