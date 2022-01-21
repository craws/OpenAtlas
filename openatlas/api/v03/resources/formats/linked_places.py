from typing import Any, Union

from flask import url_for

from openatlas import app
from openatlas.api.v03.resources.formats.linked_places_helper import get_file, \
    get_geoms_by_entity, get_links, \
    get_location_id, get_node, get_reference_systems, get_time
from openatlas.api.v03.resources.util import \
    replace_empty_list_values_in_dict_with_none
from openatlas.models.entity import Entity
from openatlas.models.link import Link


def get_entity(
        entity: Entity,
        links: list[Link],
        links_inverse: list[Link],
        parser: dict[str, Any]) -> dict[str, Any]:
    return {
        'type': 'FeatureCollection',
        '@context': app.config['API_SCHEMA'],
        'features': [replace_empty_list_values_in_dict_with_none({
            '@id': url_for('view', id_=entity.id, _external=True),
            'type': 'Feature',
            'crmClass': f'crm:{entity.cidoc_class.code} '
                        f"{entity.cidoc_class.i18n['en']}",
            'systemClass': entity.class_.name,
            'properties': {'title': entity.name},
            'types': get_node(entity, links)
                if 'types' in parser['show'] else None,
            'depictions': get_file(links_inverse)
                if 'depictions' in parser['show'] else None,
            'when': {'timespans': [get_time(entity)]}
                if 'when' in parser['show'] else None,
            'links': get_reference_systems(links_inverse)
                if 'links' in parser['show'] else None,
            'descriptions': [{'value': entity.description}],
            'names': [{"alias": value} for value in entity.aliases.values()]
                if entity.aliases and 'names' in parser['show'] else None,
            'geometry': get_geometries(entity, links)
                if 'geometry' in parser['show'] else None,
            'relations': get_links(links, links_inverse)
                if 'relations' in parser['show'] else None})]}


def get_geometries(
        entity: Entity,
        links: list[Link]) -> Union[dict[str, Any], None]:
    if entity.class_.view == 'place' or entity.class_.name in ['artifact']:
        return get_geoms_by_entity(get_location_id(links))
    if entity.class_.name == 'object_location':
        return get_geoms_by_entity(entity.id)
    return None
