from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from flask import g, url_for

from openatlas.database.api import get_wkts_by_ids
from openatlas.models.entity import Entity, Link


def entity_uri(entity: Entity) -> str:
    base = getattr(g, 'entity_base_url', None)
    if base is None:
        base = url_for(
            'api.entity_uuid',
            uuid='00000000-0000-0000-0000-000000000000',
            _external=True).replace('00000000-0000-0000-0000-000000000000', '')
        g.entity_base_url = base
    return f"{base}{entity.uuid}"


@dataclass
class EntityLinks:
    entity: Entity
    links: list[Link] = field(default_factory=list)
    links_inverse: list[Link] = field(default_factory=list)
    geometries: dict[int, Any] = field(default_factory=dict)


def get_links_for_entities(
        entities: list[Entity],
        codes: str | list[str] | None = None,
        classes: list[str] | None = None,
        inverse_codes: str | list[str] | None = None,
        inverse_classes: list[str] | None = None,
        include_forward: bool = True,
        include_inverse: bool = True,
        include_geometries: bool = True) -> dict[int, EntityLinks]:
    entities_with_links: dict[int, EntityLinks] = {}
    preloaded = {e.id: e for e in entities}
    preloaded.update(g.types)
    preloaded.update(g.reference_systems)

    for entity in entities:
        entities_with_links[entity.id] = EntityLinks(entity=entity)

    entity_ids = [entity.id for entity in entities]
    geom_ids = set(entity_ids) if include_geometries else set()

    if include_forward:
        for link_ in Entity.get_links_of_entities(
                entity_ids,
                codes=codes,
                classes=classes,
                preloaded_entities=preloaded):
            entities_with_links[link_.domain.id].links.append(link_)
            preloaded[link_.range.id] = link_.range
            if include_geometries and link_.property.code == 'P53':
                geom_ids.add(link_.range.id)

    if include_inverse:
        for link_ in Entity.get_links_of_entities(
                entity_ids,
                codes=inverse_codes or codes,
                classes=inverse_classes or classes,
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
