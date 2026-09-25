import functools
import json
import pathlib
import re
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Final, Optional
from uuid import UUID

from flask import Response, g, url_for

from openatlas import app
from openatlas.api.api_v04.resources.util import to_camel_case
from openatlas.api.api_v1.entity import (
    get_by_system_class, get_count_by_system_class)
from openatlas.api.api_v1.error_handlers import abort_not_found
from openatlas.api.api_v1.models.util import (
    ExternalReferenceSystemModel, MatchTypeEnum)
from openatlas.api.api_v1.util.content_negotiation import (
    make_lod_response)
from openatlas.api.api_v1.util.pagination import get_pagination_lod
from openatlas.database.api import get_wkts_by_ids
from openatlas.display.image_processing import (
    check_iiif_activation, check_iiif_file_exist)
from openatlas.models.entity import Entity, Link

DATE_PARTS_RE: Final = re.compile(
    r'^(-?\d{4,})-(\d{2})-(\d{2})'
    r'(?:[T ](\d{2}):(\d{2}):(\d{2})(?:\.\d+)?)?Z?$')


@dataclass
class EntityLinks:
    entity: Entity
    links: list[Link] = field(default_factory=list)
    links_inverse: list[Link] = field(default_factory=list)
    geometries: dict[int, Any] = field(default_factory=dict)


def date_to_utc_iso_str(date: Any) -> str | None:
    if not date:
        return None
    match = DATE_PARTS_RE.match(str(date))
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

# todo: rewrite without using g.files!
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


def get_links_for_entities(entities: list[Entity]) -> dict[int, EntityLinks]:
    entities_with_links: dict[int, EntityLinks] = {}
    preloaded = {e.id: e for e in entities}
    preloaded.update(g.types)
    preloaded.update(g.reference_systems)

    for entity in entities:
        entities_with_links[entity.id] = EntityLinks(entity=entity)

    geom_ids = set(e.id for e in entities)
    for link_ in Entity.get_links_of_entities(
            [entity.id for entity in entities],
            preloaded_entities=preloaded):
        entities_with_links[link_.domain.id].links.append(link_)
        preloaded[link_.range.id] = link_.range
        if link_.property.code == 'P53':
            geom_ids.add(link_.range.id)

    for link_ in Entity.get_links_of_entities(
            [entity.id for entity in entities],
            inverse=True,
            preloaded_entities=preloaded):
        entities_with_links[link_.range.id].links_inverse.append(link_)
        preloaded[link_.domain.id] = link_.domain

    if geom_ids:
        wkts = get_wkts_by_ids(list(geom_ids))
        for id_ in entities_with_links:
            entities_with_links[id_].geometries = wkts

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


def _get_match_type(link_: Link) -> MatchTypeEnum:
    assert link_.type
    return MatchTypeEnum(to_camel_case(g.types[link_.type.id].name))


def _get_external_reference_item(
        link_: Link,
        entity: Entity) -> ExternalReferenceSystemModel:
    return ExternalReferenceSystemModel(
        id=entity.id,
        name=entity.name,
        match_type=_get_match_type(link_),
        identifier=f'{entity.resolver_url or ""}{link_.description}',
        description=entity.description,
        system_url=entity.website_url,
        url=entity.resolver_url)


def get_external_reference_items(
        inverse_links: list[Link]) -> list[ExternalReferenceSystemModel]:
    external_references = []
    for link_ in inverse_links:
        if link_.type and \
                (entity := g.reference_systems.get(link_.domain.id)):
            external_references.append(
                _get_external_reference_item(link_, entity))
    return external_references


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


def get_entity_response(
        entity_id: UUID,
        formatter: Callable[[Entity], dict[str, Any]],
        ext: str | None = None) -> dict[str, Any] | Response:
    entity = Entity.get_by_uuid(entity_id, types=True, aliases=True)
    if not entity:
        abort_not_found(entity_id)
    return make_lod_response(formatter(entity), ext=ext)


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
