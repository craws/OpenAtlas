from typing import Any, Optional, Union

from openatlas.api.v03.resources.util import \
    replace_empty_list_values_in_dict_with_none
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link


def get_geojson(entities: list[Entity]) -> dict[str, Any]:
    out = []
    for entity in entities:
        if geoms := [
            get_geojson_dict(entity, geom)
            for geom in get_geom(entity)]:
            out.extend(geoms)
        else:
            out.append(get_geojson_dict(entity))
    return {'type': 'FeatureCollection', 'features': out}


def get_geom(entity: Entity) -> Union[list[dict[str, Any]], list[Any]]:
    if entity.class_.view == 'place' or entity.class_.name in ['artifact']:
        return Gis.get_by_id(
            Link.get_linked_entity_safe(entity.id, 'P53').id)
    if entity.class_.name == 'object_location':
        return Gis.get_by_id(entity.id)
    return []


def get_geojson_dict(
        entity: Entity,
        geom: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return replace_empty_list_values_in_dict_with_none({
        'type': 'Feature',
        'geometry': geom,
        'properties': {
            '@id': entity.id,
            'systemClass': entity.class_.name,
            'name': entity.name,
            'description': entity.description,
            'begin_earliest': entity.begin_from,
            'begin_latest': entity.begin_to,
            'begin_comment': entity.begin_comment,
            'end_earliest': entity.end_from,
            'end_latest': entity.end_to,
            'end_comment': entity.end_comment,
            'types': [': '.join([type_.name]) for type_ in entity.types]}})
