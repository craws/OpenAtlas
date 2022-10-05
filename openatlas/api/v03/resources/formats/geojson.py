from typing import Any, Optional, Union

from openatlas.api.v03.resources.util import (
    flatten_list_and_remove_duplicates, link_parser_check,
    replace_empty_list_values_in_dict_with_none)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link


def get_geojson(
        entities: list[Entity],
        parser: dict[str, Any]) -> dict[str, Any]:
    out = []
    for entity in entities:
        if geoms := [get_geojson_dict(entity, parser, geom)
                     for geom in get_geom(entity)]:
            out.extend(geoms)
        else:
            out.append(get_geojson_dict(entity, parser))
    return {'type': 'FeatureCollection', 'features': out}


def get_geom(entity: Entity) -> Union[list[dict[str, Any]], list[Any]]:
    if entity.class_.view == 'place' or entity.class_.name == 'artifact':
        return Gis.get_by_id(
            Link.get_linked_entity_safe(entity.id, 'P53').id)
    if entity.class_.name == 'object_location':
        return Gis.get_by_id(entity.id)
    return []


def get_geojson_v2(
        entities: list[Entity],
        parser: dict[str, Any]) -> dict[str, Any]:
    out = []
    links = [link_ for link_ in link_parser_check(entities, parser)
             if link_.property.code
             in ['P53', 'P74', 'OA8', 'OA9', 'P7', 'P26', 'P27']]
    for entity in entities:
        if geom := get_geoms_as_collection(
                entity,
                [link_.range.id for link_ in links
                 if link_.domain.id == entity.id]):
            out.append(get_geojson_dict(entity, parser, geom))
    return {'type': 'FeatureCollection', 'features': out}


def get_geoms_as_collection(
        entity: Entity,
        links: list[int]) -> Optional[dict[str, Any]]:
    if entity.class_.name == 'object_location':
        return get_geoms_dict(Gis.get_by_id(entity.id))
    if links:
        return get_geoms_dict(flatten_list_and_remove_duplicates(
            [Gis.get_by_id(location) for location in links]))
    return None


def get_geoms_dict(
        geoms: list[dict[str, any]]) -> Optional[dict[str, Any]]:
    if len(geoms) == 0:
        return None
    if len(geoms) == 1:
        return geoms[0]
    return {'type': 'GeometryCollection', 'geometries': geoms}


def get_geojson_dict(
        entity: Entity,
        parser: dict[str, Any],
        geom: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return replace_empty_list_values_in_dict_with_none({
        'type': 'Feature',
        'geometry': geom,
        'properties': {
            '@id': entity.id,
            'systemClass': entity.class_.name,
            'name': entity.name,
            'description': entity.description
            if 'description' in parser['show'] else None,
            'begin_earliest': entity.begin_from
            if 'when' in parser['show'] else None,
            'begin_latest': entity.begin_to
            if 'when' in parser['show'] else None,
            'begin_comment': entity.begin_comment
            if 'when' in parser['show'] else None,
            'end_earliest': entity.end_from
            if 'when' in parser['show'] else None,
            'end_latest': entity.end_to
            if 'when' in parser['show'] else None,
            'end_comment': entity.end_comment
            if 'when' in parser['show'] else None,
            'types': [{'typeName': type_.name, 'typeId': type_.id}
                      for type_ in entity.types]
            if 'types' in parser['show'] else None}})
