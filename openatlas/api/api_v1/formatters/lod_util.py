import re
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, Optional
from uuid import UUID

from flask import Response, g, url_for

from openatlas.api.api_v04.resources.util import to_camel_case
from openatlas.api.api_v1.entity import (
    get_by_system_class, get_count_by_system_class, get_entity_by_uuid)
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


def entity_uri(entity: Entity) -> str:
    base = getattr(g, 'entity_base_url', None)
    if base is None:
        base = url_for(
            'api.entity_uuid',
            uuid='00000000-0000-0000-0000-000000000000',
            _external=True).replace('00000000-0000-0000-0000-000000000000', '')
        g.entity_base_url = base
    return f"{base}{entity.uuid}"


def date_to_utc_iso_str(date: Any) -> str | None:
    if not date:
        return None  # pragma: no cover
    match = DATE_PARTS_RE.match(str(date))
    if not match:
        return str(date)  # pragma: no cover
    year, month, day, hour, minute, second = match.groups()
    if hour and (int(hour) or int(minute) or int(second)):
        return (f'{year}-{month}-'
                f'{day}T{hour}:{minute}:{second}Z')  # pragma: no cover
    return f'{year}-{month}-{day}'


def get_license_type(entity: Entity) -> Optional[Entity]:
    license_ = None
    for type_ in entity.types:
        if g.types[type_.root[0]].name == 'License':
            license_ = type_
            break
    return license_


def get_iiif_manifest_and_path(
        img_id: int,
        file_paths: dict[int, Path] | None = None) -> dict[str, str]:
    iiif_manifest = ''
    iiif_base_path = ''
    if not check_iiif_activation():
        return {'IIIFManifest': iiif_manifest, 'IIIFBasePath': iiif_base_path}
    file_ = (file_paths if file_paths is not None else g.files).get(img_id)
    if file_paths is None:
        exists = check_iiif_file_exist(img_id)
    elif g.settings['iiif_conversion']:
        exists = (Path(g.settings['iiif_path']) / f'{img_id}.tiff').is_file()
    else:
        exists = file_ is not None
    if exists:
        iiif_manifest = url_for(
            'api.iiif_manifest',
            version=g.settings['iiif_version'],
            id_=img_id,
            _external=True)
        if file_:
            iiif_base_path = (
                f"{g.settings['iiif_url']}{img_id}{file_.suffix}")
    return {'IIIFManifest': iiif_manifest, 'IIIFBasePath': iiif_base_path}


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:  # pragma: no cover
        return False


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
        for item in entities_with_links.values():
            item.geometries = wkts

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


def get_entity_response(
        entity_id: UUID,
        formatter: Callable[[Entity], dict[str, Any]],
        ext: str | None = None) -> dict[str, Any] | Response:
    entity = get_entity_by_uuid(entity_id, types=True, aliases=True)
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
