import json
import pathlib
from collections import defaultdict
from typing import Any

from flask import g

from openatlas import app
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import  get_gis_by_entities


def get_links_for_entities(entities: list[Entity]) -> dict[Any, Any]:
    entities_with_links = {}
    for entity in entities:
        entities_with_links[entity.id] = {
            'entity': entity,
            'links': [],
            'links_inverse': [],
            'geometry': []}
    for link_ in Entity.get_links_of_entities([entity.id for entity in entities]):
        entities_with_links[link_.domain.id]['links'].append(link_)
    for link_ in Entity.get_links_of_entities(
            [entity.id for entity in entities],
            inverse=True):
        entities_with_links[
            link_.range.id]['links_inverse'].append(link_)
    for id_, geom in get_gis_by_entities(entities).items():
        entities_with_links[id_]['geometry'].extend(geom)
    return entities_with_links



def get_type_references() -> dict[int, list[Link]]:
    type_links = Entity.get_links_of_entities(
        list(g.types.keys()),
        'P67',
        inverse=True)
    out: dict[int, list[Link]] = defaultdict(list)
    for link_ in type_links:
        if link_.domain.class_.name in \
                ['external_reference', 'reference_system']:
            out[link_.range.id].append(link_)
    return out



def get_loud_context() -> dict[str, Any]:
    file_path = pathlib.Path(app.root_path) / 'api' / 'linked-art.json'

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_loud_context() -> dict[str, str]:
    context = get_loud_context().get('@context', {})
    inverted: dict[str, str] = {}
    for term, definition in context.items():
        if not isinstance(definition, dict):
            continue
        inverted[definition['@id']] = term
        for nested_term, nested_def in definition.get('@context', {}).items():
            if isinstance(nested_def, dict):
                inverted[nested_def['@id']] = nested_term
    return inverted
