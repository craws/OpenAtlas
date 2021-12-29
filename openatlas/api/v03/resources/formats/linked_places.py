from typing import Any, Dict, List, Optional

from flask import url_for

from openatlas import app
from openatlas.api.v03.resources.formats.linked_places_helper import get_file, \
    get_geoms_by_entity, get_links, \
    get_location_id, get_node, get_reference_systems, get_time
from openatlas.models.entity import Entity
from openatlas.models.link import Link


def get_entity(
        entity: Entity,
        links: List[Link],
        links_inverse: List[Link],
        parser: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'type': 'FeatureCollection',
        '@context': app.config['API_SCHEMA'],
        'features': [build_feature(entity, links, links_inverse, parser)]}


def build_feature(
        entity: Entity,
        links: List[Link],
        links_inverse: List[Link],
        parser: Dict[str, Any]) -> Dict[str, Any]:
    return {'@id': url_for('view', id_=entity.id, _external=True),
            'type': 'Feature',
            'crmClass': get_crm_class(entity),
            'systemClass': entity.class_.name,
            'properties': {'title': entity.name},
            'types': get_types(entity, links, parser),
            'depictions': get_depictions(links_inverse, parser),
            'when': get_timespans(entity, parser),
            'links': get_reference_links(links_inverse, parser),
            'description': get_description(entity),
            'names': get_names(entity, parser),
            'geometry': get_geometries(entity, links)
                if 'geometry' in parser['show'] else None,
            'relations': get_relations(links, links_inverse, parser)}


def get_description(entity: Entity) -> Optional[List[Dict[str, Any]]]:
    return [{'value': entity.description}] if entity.description else None


def get_relations(
        links: List[Link],
        links_inverse: List[Link],
        parser: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
    return get_links(links, links_inverse) \
        if 'relations' in parser['show'] else None


def get_types(
        entity: Entity,
        links: List[Link],
        parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    return get_node(entity, links) if 'types' in parser['show'] else None


def get_depictions(
        links_inverse: List[Link],
        parser: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
    return get_file(links_inverse) if 'depictions' in parser['show'] else None


def get_timespans(
        entity: Entity,
        parser: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return {'timespans': [get_time(entity)]} \
        if 'when' in parser['show'] else None


def get_reference_links(
        links_inverse: List[Link],
        parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    return get_reference_systems(links_inverse) \
        if 'links' in parser['show'] else None


def get_geometries(
        entity: Entity,
        links: List[Link]) -> Dict[str, Any]:
    if entity.class_.view == 'place' or entity.class_.name in ['artifact']:
        return get_geoms_by_entity(get_location_id(links))
    if entity.class_.name == 'object_location':
        return get_geoms_by_entity(entity.id)


def get_names(
        entity: Entity,
        parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    return [{"alias": value} for value in entity.aliases.values()] \
        if entity.aliases and 'names' in parser['show'] else None


def get_crm_class(entity: Entity) -> str:
    return f"crm:{entity.cidoc_class.code} {entity.cidoc_class.i18n['en']}"
