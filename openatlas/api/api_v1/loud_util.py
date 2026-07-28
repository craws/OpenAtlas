from typing import Any

from openatlas.models.entity import Entity
from openatlas.models.gis import  get_gis_by_entities


def get_links_for_entities(entities: list[Entity]) -> dict[Any, Any] | None:
    entities_with_links = {}
    if not entities:
        return None
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


