from typing import Any, Optional, Union

from flask import g, url_for

from openatlas import app
from openatlas.api.resources.util import (
    get_geometric_collection, get_license_name, get_reference_systems,
    replace_empty_list_values_in_dict_with_none, to_camel_case)
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.display.util import get_file_path


def get_linked_places_entity(
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
            'types': get_lp_types(entity, links)
            if 'types' in parser['show'] else None,
            'depictions': get_lp_file(links_inverse)
            if 'depictions' in parser['show'] else None,
            'when': {'timespans': [get_lp_time(entity)]}
            if 'when' in parser['show'] else None,
            'links': get_reference_systems(links_inverse)
            if 'links' in parser['show'] else None,
            'descriptions': [{'value': entity.description}]
            if 'description' in parser['show'] else None,
            'names': [{"alias": value} for value in entity.aliases.values()]
            if entity.aliases and 'names' in parser['show'] else None,
            'geometry': get_geometric_collection(entity, links)
            if 'geometry' in parser['show'] else None,
            'relations': get_lp_links(links, links_inverse, parser)
            if 'relations' in parser['show'] else None})]}


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
            get_lp_time(link_.domain if inverse else link_.range)]}}


def get_lp_links(
        links: list[Link],
        links_inverse: list[Link],
        parser: dict[str, Any]) -> list[dict[str, str]]:
    properties = parser['relation_type'] or list(g.properties)
    out = []
    for link_ in links:
        if link_.property.code in properties:
            out.append(link_dict(link_))
        continue
    for link_ in links_inverse:
        if link_.property.code in properties:
            out.append(link_dict(link_, inverse=True))
        continue
    return out


def get_lp_file(links_inverse: list[Link]) -> list[dict[str, str]]:
    files = []
    for link in links_inverse:
        if link.domain.class_.name != 'file':
            continue
        path = get_file_path(link.domain.id)
        files.append({
            '@id': url_for(
                'api_03.entity',
                id_=link.domain.id,
                _external=True),
            'title': link.domain.name,
            'license': get_license_name(link.domain),
            'url': url_for(
                'api.display',
                filename=path.name,
                _external=True) if path else "N/A"})
    return files


def get_lp_types(entity: Entity, links: list[Link]) -> list[dict[str, Any]]:
    types = []
    for type_ in entity.types:
        type_dict = {
            'identifier': url_for(
                'api_03.entity', id_=type_.id, _external=True),
            'label': type_.name,
            'hierarchy': ' > '.join(map(
                str, [g.types[root].name for root in type_.root]))}
        for link in links:
            if link.range.id == type_.id and link.description:
                type_dict['value'] = link.description
                if link.range.id == type_.id and type_.description:
                    type_dict['unit'] = type_.description
        types.append(type_dict)
    return types


def get_lp_time(entity: Union[Entity, Link]) -> Optional[dict[str, Any]]:
    return {
        'start': {
            'earliest': entity.begin_from,
            'latest': entity.begin_to,
            'comment': entity.begin_comment},
        'end': {
            'earliest': entity.end_from,
            'latest': entity.end_to,
            'comment': entity.end_comment}}
