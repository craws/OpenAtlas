from operator import attrgetter
from typing import Any, Optional, Union

from flask import g

from openatlas.api.resources.database_mapper import get_all_links_as_dict
from openatlas.api.resources.model_mapper import (
    get_all_links_of_entities_inverse, get_entities_by_ids)
from openatlas.api.resources.util import (
    filter_link_list_by_property_codes, get_geometric_collection,
    get_license, get_reference_systems, remove_duplicate_entities,
    replace_empty_list_values_in_dict_with_none)
from openatlas.display.util import get_file_path
from openatlas.models.entity import Entity
from openatlas.models.link import Link


def get_subunit(data: dict[str, Any]) -> dict[str, Any]:
    return replace_empty_list_values_in_dict_with_none({
        'id': data['entity'].id,
        'rootId': data['root_id'],
        'parentId': get_parent(data['links_inverse']),
        'openatlasClassName': data['entity'].class_.name,
        'crmClass': data['entity'].cidoc_class.code,
        'created': str(data['entity'].created),
        'modified': str(data['entity'].modified),
        'latestModRec': data['latest_modified'],
        'geometry':
            get_geometries_thanados(
                get_geometric_collection(data['entity'], data['links']),
                data['parser']),
        'children': get_children(data),
        'properties': get_properties(data)})


def get_parent(links: list[Link]) -> Optional[int]:
    for link_ in links:
        if link_.property.code == 'P46':
            return link_.domain.id
    return None


def get_children(data: dict[str, Any]) -> list[Union[int, dict[str, Any]]]:
    children = [link_.range.id for link_ in data['links'] if
                link_.property.code == 'P46']
    return [{'child': child} for child in children] \
        if data['parser']['format'] == 'xml' else children


def get_geometries_thanados(
        geom: Union[dict[str, Any], None],
        parser: dict[str, Any]) -> Union[list[Any], None, dict[str, Any]]:
    if parser['format'] == 'xml' and geom:
        if geom['type'] == 'GeometryCollection':
            geometries = []
            for item in geom['geometries']:
                item['coordinates'] = transform_geometries_for_xml(item)
                geometries.append(item)
            geom['geometries'] = [{'geom': item} for item in geometries]
        else:
            geom['coordinates'] = transform_geometries_for_xml(geom)
    return geom


def transform_geometries_for_xml(geom: dict[str, Any]) \
        -> Union[list[list[dict[str, Any]]], list[dict[str, Any]]]:
    output = []
    if geom['type'] == 'Polygon':
        output = [transform_coordinates_for_xml(k)
                  for i in geom['coordinates'] for k in i]
    if geom['type'] == 'LineString':
        output = [
            transform_coordinates_for_xml(k) for k in geom['coordinates']]
    if geom['type'] == 'Point':
        output = transform_coordinates_for_xml(geom['coordinates'])
    return output


def transform_coordinates_for_xml(
        coordinates: list[float]) -> list[dict[str, Any]]:
    return [
        {'coordinate':
            {'longitude': coordinates[0], 'latitude': coordinates[1]}}]


def get_properties(data: dict[str, Any]) -> dict[str, Any]:
    return replace_empty_list_values_in_dict_with_none({
        'name': data['entity'].name,
        'aliases': get_aliases(data),
        'description': data['entity'].description,
        'standardType':
            get_standard_type(data) if data['entity'].standard_type else None,
        'timespan': get_timespans(data['entity']),
        'externalReferences':
            get_ref_system(data['links_inverse'], data['parser']),
        'references': get_references(data['links_inverse'], data['parser']),
        'files': get_file(data),
        'types': get_types(data)})


def get_aliases(data: dict[str, Any]) -> list[Any]:
    aliases = list(data['entity'].aliases.values())
    if data['parser']['format'] == 'xml':
        return [{'alias': alias} for alias in aliases]
    return aliases


def get_ref_system(
        links_inverse: list[Link],
        parser: dict[str, Any]) -> list[dict[str, Any]]:
    ref_sys = get_reference_systems(links_inverse)
    if ref_sys and parser['format'] == 'xml':
        return [{'externalReference': ref} for ref in ref_sys]
    return ref_sys


def get_references(
        links: list[Link],
        parser: dict[str, Any]) -> list[dict[str, Any]]:
    references = []
    for link_ in links:
        if link_.property.code == "P67" and link_.domain.class_.name in \
                ['bibliography', 'edition', 'external_reference']:
            references.append({
                'abbreviation': link_.domain.name,
                'id': link_.domain.id,
                'title': link_.domain.description,
                'pages': link_.description or None})
    if parser['format'] == 'xml':
        return [{'reference': ref} for ref in references]
    return references


def get_timespans(entity: Entity) -> dict[str, Any]:
    return {
        'earliestBegin': str(entity.begin_from) if entity.begin_from else None,
        'latestBegin': str(entity.begin_to) if entity.begin_to else None,
        'earliestEnd': str(entity.end_from) if entity.end_from else None,
        'latestEnd': str(entity.end_to) if entity.end_to else None}


def get_file(data: dict[str, Any]) -> list[dict[str, Any]]:
    files = []
    for link in data['links_inverse']:
        if link.domain.class_.name != 'file':
            continue
        path = get_file_path(link.domain.id)
        files.append({
            'id': link.domain.id,
            'name': link.domain.name,
            'fileName': path.name if path else None,
            'license': get_license(link.domain),
            'source': link.domain.description or None})
    if data['parser']['format'] == 'xml':
        return [{'file': file} for file in files]
    return files


def get_standard_type(data: dict[str, Any]) -> dict[str, Any]:
    type_ = data['entity'].standard_type
    type_ref_link = \
        [link for link in data['ext_reference_links'] if
         link.range.id == type_.id]
    types_dict = {
        'id': type_.id,
        'name': type_.name,
        'externalReferences': get_ref_system(type_ref_link, data['parser'])}
    hierarchy = [g.types[root].name for root in type_.root]
    hierarchy.reverse()
    types_dict['path'] = ' > '.join(map(str, hierarchy))
    types_dict['rootId'] = type_.root[0]
    return types_dict


def get_types(data: dict[str, Any]) -> Optional[list[dict[str, Any]]]:
    types = []
    for type_ in data['entity'].types:
        if type_.category == 'standard':
            continue
        type_ref_link = [link for link in data['ext_reference_links'] if
                         link.range.id == type_.id]
        types_dict = {
            'id': type_.id,
            'name': type_.name,
            'externalReferences':
                get_ref_system(type_ref_link, data['parser'])}
        for link in data['links']:
            if link.range.id == type_.id and link.description:
                types_dict['value'] = link.description
                if link.range.id == type_.id and type_.description:
                    types_dict['unit'] = type_.description
        hierarchy = [g.types[root].name for root in type_.root]
        types_dict['path'] = ' > '.join(map(str, hierarchy))
        types_dict['rootId'] = type_.root[0]
        types.append(types_dict)
    if data['parser']['format'] == 'xml':
        return [{'type': type_} for type_ in types]
    return types


def get_subunits_from_id(
        entity: Entity,
        parser: dict[str, Any]) -> list[dict[str, Any]]:
    all_links = get_all_links_as_dict()
    entity_ids = get_all_subs_linked_to_place(entity, all_links)
    entities = get_entities_by_ids(entity_ids)
    entities.sort(key=attrgetter('id'))
    links = get_links_from_list_of_links(entity_ids, all_links)
    ext_reference_links = get_type_links_inverse(entities)
    latest_modified = max(
        entity.modified for entity in entities if entity.modified)
    entities_dict: dict[int, Any] = {}
    for entity_ in entities:
        entities_dict[entity_.id] = {
            'entity': entity_,
            'links':
                [Link(link_) for link_ in links['links']
                 if link_['domain_id'] == entity_.id],
            'links_inverse':
                [Link(link_) for link_ in links['links_inverse']
                 if link_['range_id'] == entity_.id],
            'ext_reference_links': ext_reference_links,
            'root_id': entity.id,
            'latest_modified': latest_modified,
            'parser': parser}
    return [get_subunit(item) for item in entities_dict.values()]


def get_links_from_list_of_links(
        entities: list[int],
        links: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[Any]] = {'links': [], 'links_inverse': []}
    for link_ in links:
        if link_['domain_id'] in entities:
            data['links'].append(link_)
        if link_['range_id'] in entities:
            data['links_inverse'].append(link_)
    return data


def get_all_subs_linked_to_place(
        entity: Entity,
        links: list[dict[str, Any]]) -> list[int]:
    links_ = filter_link_list_by_property_codes(links, ['P46'])
    return get_all_subs_linked_to_place_recursive(entity.id, links_, [])


def get_all_subs_linked_to_place_recursive(
        id_: int,
        links: list[dict[str, Any]],
        data: list[int]) -> list[int]:
    data.append(id_)
    for link_ in links:
        if link_['domain_id'] == id_:
            get_all_subs_linked_to_place_recursive(
                link_['range_id'], links, data)
    return data


def get_type_links_inverse(entities: list[Entity]) -> list[Link]:
    types = remove_duplicate_entities(
        [type_ for entity in entities for type_ in entity.types])
    links = get_all_links_of_entities_inverse(
        [type_.id for type_ in types], 'P67')
    return [link_ for link_ in links if
            link_.domain.class_.name == 'reference_system']
