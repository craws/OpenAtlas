from typing import Any, Optional

from flask import g

from openatlas.api.resources.util import (
    get_location_link, link_parser_check,
    replace_empty_list_values_in_dict_with_none)
from openatlas.api.resources.model_mapper import (
    flatten_list_and_remove_duplicates)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis


def get_geojson(
        entities: list[Entity],
        parser: dict[str, Any]) -> dict[str, Any]:
    out = []
    links = Entity.get_links_of_entities([e.id for e in entities], 'P53')
    for entity in entities:
        if entity.class_.view == 'place':
            entity_links = [l_ for l_ in links if l_.domain.id == entity.id]
            entity.types.update(get_location_link(entity_links).range.types)
        if geoms := [get_geojson_dict(entity, parser, geom)
                     for geom in get_geom(entity, parser)]:
            out.extend(geoms)
        else:
            out.append(get_geojson_dict(entity, parser))
    return {'type': 'FeatureCollection', 'features': out}


def get_geom(entity: Entity, parser: dict[str, Any]) -> list[Any]:
    if entity.class_.view == 'place' or entity.class_.name == 'artifact':
        id_ = entity.get_linked_entity_safe('P53').id
        geoms = Gis.get_by_id(id_)
        if parser['centroid']:
            geoms.extend(Gis.get_centroids_by_id(id_))
        return geoms
    if entity.class_.name == 'object_location':
        geoms = Gis.get_by_id(entity.id)
        if parser['centroid']:
            geoms.extend(Gis.get_centroids_by_id(entity.id))
        return geoms
    return []


def get_geojson_v2(
        entities: list[Entity],
        parser: dict[str, Any]) -> dict[str, Any]:
    out = []
    links = [link_ for link_ in link_parser_check(entities, parser)
             if link_.property.code
             in ['P53', 'P74', 'OA8', 'OA9', 'P7', 'P26', 'P27']]
    for entity in entities:
        entity_links = [
            link_ for link_ in links if link_.domain.id == entity.id]
        if entity.class_.view == 'place':
            entity.types.update(get_location_link(entity_links).range.types)
        if geom := get_geoms_as_collection(
                entity,
                [l_.range.id for l_ in entity_links],
                parser):
            out.append(get_geojson_dict(entity, parser, geom))
    return {'type': 'FeatureCollection', 'features': out}


def get_geoms_as_collection(
        entity: Entity,
        links: list[int],
        parser: dict[str, Any]) -> Optional[dict[str, Any]]:
    if entity.class_.name == 'object_location':
        geoms: list[Any] = Gis.get_by_id(entity.id)
        if parser['centroid']:
            geoms.extend(Gis.get_centroids_by_id(entity.id))
        return get_geoms_dict(geoms)
    if links:
        geoms = [Gis.get_by_id(id_) for id_ in links]
        if parser['centroid']:
            geoms.extend([Gis.get_centroids_by_id(id_) for id_ in links])
        return get_geoms_dict(flatten_list_and_remove_duplicates(geoms))
    return None


def get_geoms_dict(geoms: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
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
            'types': [{
                'typeName': type_.name,
                'typeId': type_.id,
                'typeHierarchy': ' > '.join(
                    map(str, [g.types[root].name for root in type_.root]))}
                for type_ in entity.types]
            if 'types' in parser['show'] else None}})
