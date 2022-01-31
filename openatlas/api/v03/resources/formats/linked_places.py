from typing import Any, Optional, Union

from flask import g, url_for

from openatlas import app
from openatlas.api.v03.resources.util import \
    get_license, replace_empty_list_values_in_dict_with_none, to_camel_case
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.util import get_file_path


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


def get_location_id(links: list[Link]) -> int:
    return [l_.range.id for l_ in links if l_.property.code == 'P53'][0]


def relation_type(link_: Link, inverse: bool = False) -> str:
    property_ = f"i {link_.property.i18n_inverse['en']}" \
        if inverse and link_.property.i18n_inverse['en'] \
        else f" {link_.property.i18n['en']}"
    return f"crm:{link_.property.code}{property_}"


def link_dict(link_: Link, inverse: bool = False) -> dict[str, Any]:
    return {
        'label': link_.domain.name if inverse else link_.range.name,
        'relationTo':
            url_for(
                'api_03.entity',
                id_=link_.domain.id if inverse else link_.range.id,
                _external=True),
        'relationType': relation_type(link_, inverse),
        'relationSystemClass':
            link_.domain.class_.name if inverse else link_.range.class_.name,
        'type': to_camel_case(link_.type.name) if link_.type else None,
        'relationDescription': link_.description,
        'when': {'timespans': [
            get_time(link_.domain if inverse else link_.range)]}}


def get_links(
        links: list[Link],
        links_inverse: list[Link]) -> list[dict[str, str]]:
    out = []
    for link_ in links:
        out.append(link_dict(link_))
    for link_ in links_inverse:
        out.append(link_dict(link_, inverse=True))
    return out


def get_file(links_inverse: list[Link]) -> list[dict[str, str]]:
    files = []
    for link in links_inverse:
        if link.domain.class_.name != 'file':
            continue
        path = get_file_path(link.domain.id)
        files.append({
            '@id': url_for('api_03.entity', id_=link.domain.id, _external=True),
            'title': link.domain.name,
            'license': get_license(link.domain),
            'url': url_for(
                'api.display',
                filename=path.name,
                _external=True) if path else "N/A"})
    return files


def get_node(entity: Entity, links: list[Link]) -> list[dict[str, Any]]:
    nodes = []
    for node in entity.types:
        nodes_dict = {
            'identifier': url_for(
                'api_03.entity',
                id_=node.id,
                _external=True),
            'label': node.name}
        for link in links:
            if link.range.id == node.id and link.description:
                nodes_dict['value'] = link.description
                if link.range.id == node.id and node.description:
                    nodes_dict['unit'] = node.description
        hierarchy = [g.types[root].name for root in node.root]
        nodes_dict['hierarchy'] = ' > '.join(map(str, hierarchy))
        nodes.append(nodes_dict)
    return nodes


def get_time(entity: Union[Entity, Link]) -> Optional[dict[str, Any]]:
    return {
        'start': {
            'earliest': str(entity.begin_from),
            'latest': str(entity.begin_to),
            'comment': entity.begin_comment},
        'end': {
            'earliest': str(entity.end_from),
            'latest': str(entity.end_to),
            'comment': entity.end_comment}}


def get_geoms_by_entity(entity_id: int) -> dict[str, Any]:
    geoms = Gis.get_by_id(entity_id)
    if len(geoms) == 1:
        return geoms[0]
    return {'type': 'GeometryCollection', 'geometries': geoms}


def get_reference_systems(
        links_inverse: list[Link]) -> list[dict[str, Any]]:
    ref = []
    for link_ in links_inverse:
        if not isinstance(link_.domain, ReferenceSystem):
            continue
        system = g.reference_systems[link_.domain.id]
        identifier = system.resolver_url if system.resolver_url else ''
        ref.append({
            'identifier': f"{identifier}{link_.description}",
            'type': to_camel_case(g.types[link_.type.id].name),
            'referenceSystem': system.name})
    return ref
