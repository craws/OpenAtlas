from datetime import datetime
from typing import Any, Optional, Union

from flask import g

from openatlas.api.v03.resources.util import (
    get_all_links, get_all_links_inverse, get_all_subunits_recursive,
    get_geometries, get_license, get_reference_systems,
    remove_duplicate_entities, replace_empty_list_values_in_dict_with_none)
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.type import Type
from openatlas.util.util import get_file_path


def get_subunit(
        entity: Entity,
        links: list[Link],
        links_inverse: list[Link],
        ext_reference_links: list[Link],
        root_id: int,
        latest_mod_rec: datetime,
        parser: dict[str, Any]) -> dict[str, Any]:
    return replace_empty_list_values_in_dict_with_none({
        'id': entity.id,
        'rootId': root_id,
        'parentId': get_parent(links_inverse),
        'openatlasClassName': entity.class_.name,
        'crmClass': entity.cidoc_class.code,
        'created': str(entity.created),
        'modified': str(entity.modified),
        'latestModRec': latest_mod_rec,
        'geometry': get_geometries_thanados(entity, links, parser),
        'children': get_children(links, parser),
        'properties': get_properties(
            entity,
            links,
            links_inverse,
            ext_reference_links,
            parser)})


def get_parent(links: list[Link]) -> Optional[int]:
    for link_ in links:
        if link_.property.code == 'P46':
            return link_.domain.id
    return None


def get_geometries_thanados(
        entity: Entity,
        links: list[Link],
        parser: dict[str, Any]) -> Union[list[Any], None, dict[str, Any]]:
    geom = get_geometries(entity, links)
    if parser['format'] == 'xml' and geom:
        if geom['type'] == 'GeometryCollection':
            geometries = []
            for item in geom['geometries']:  # pragma: no cover
                item['coordinates'] = check_geometries(item)
                geometries.append(item)
            geom['geometries'] = [{'geom': item} for item in geometries]
            return geom
        geom['coordinates'] = check_geometries(geom)
        return geom
    return geom


def check_geometries(geom: dict[str, Any]) \
        -> Union[list[list[dict[str, Any]]], list[dict[str, Any]], None]:
    if geom['type'] == 'Polygon':  # pragma: no cover
        return [transform_coords(k) for i in geom['coordinates'] for k in i]
    if geom['type'] == 'LineString':  # pragma: no cover
        return [transform_coords(k) for k in geom['coordinates']]
    if geom['type'] == 'Point':
        return transform_coords(geom['coordinates'])
    return None  # pragma: no cover


def transform_coords(coords: list[float]) -> list[dict[str, Any]]:
    return [{'coordinate': {'longitude': coords[0], 'latitude': coords[1]}}]


def get_children(
        links: list[Link],
        parser: dict[str, Any]) -> Union[list[int], list[dict[str, Any]]]:
    children = [link_.range.id for link_ in links if
                link_.property.code == 'P46']
    return [{'child': child} for child in children] \
        if parser['format'] == 'xml' else children


def get_properties(
        entity: Entity,
        links: list[Link],
        links_inverse: list[Link],
        ext_reference_links: list[Link],
        parser: dict[str, Any]) -> dict[str, Any]:
    return replace_empty_list_values_in_dict_with_none({
        'name': entity.name,
        'aliases': get_aliases(entity, parser),
        'description': entity.description,
        'standardType':
            get_standard_type(
                entity.standard_type,
                ext_reference_links,
                parser)
            if entity.standard_type else None,
        'timespan': get_timespans(entity),
        'externalReferences': get_ref_system(links_inverse, parser),
        'references': get_references(links_inverse, parser),
        'files': get_file(links_inverse, parser),
        'types': get_types(entity, links, ext_reference_links, parser)})


def get_aliases(entity: Entity, parser: dict[str, Any]) -> list[Any]:
    aliases = list(entity.aliases.values())
    if parser['format'] == 'xml':
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


def get_file(
        links_inverse: list[Link],
        parser: dict[str, Any]) -> list[dict[str, Any]]:
    files = []
    for link in links_inverse:
        if link.domain.class_.name != 'file':
            continue
        path = get_file_path(link.domain.id)
        files.append({
            'id': link.domain.id,
            'name': link.domain.name,
            'fileName': path.name if path else None,
            'license': get_license(link.domain),
            'source': link.domain.description or None})
    if parser['format'] == 'xml':
        return [{'file': file} for file in files]
    return files


def get_standard_type(
        type_: Type,
        ext_reference_links: list[Link],
        parser: dict[str, Any]) -> dict[str, Any]:
    type_ref_link = \
        [link for link in ext_reference_links if link.range.id == type_.id]
    types_dict = {
        'id': type_.id,
        'name': type_.name,
        'externalReferences': get_ref_system(type_ref_link, parser)}
    hierarchy = [g.types[root].name for root in type_.root]
    hierarchy.reverse()
    types_dict['path'] = ' > '.join(map(str, hierarchy))
    types_dict['rootId'] = type_.root[0]
    return types_dict


def get_types(
        entity: Entity,
        links: list[Link],
        ext_reference_links: list[Link],
        parser: dict[str, Any]) -> Optional[list[dict[str, Any]]]:
    types = []
    for type_ in entity.types:
        if type_.category == 'standard':
            continue
        type_ref_link = [link for link in ext_reference_links if
                         link.range.id == type_.id]
        types_dict = {
            'id': type_.id,
            'name': type_.name,
            'externalReferences': get_ref_system(type_ref_link, parser)}
        for link in links:
            if link.range.id == type_.id and link.description:
                types_dict['value'] = link.description
                if link.range.id == type_.id and type_.description:
                    types_dict['unit'] = type_.description
        hierarchy = [g.types[root].name for root in type_.root]
        types_dict['path'] = ' > '.join(map(str, hierarchy))
        types_dict['rootId'] = type_.root[0]
        types.append(types_dict)
    if parser['format'] == 'xml':
        return [{'type': type_} for type_ in types]
    return types


def get_subunits_from_id(
        entity: Entity,
        parser: dict[str, Any]) -> list[dict[str, Any]]:
    root_id = entity.id
    entities = get_all_subunits_recursive(entity, [])
    ext_reference_links = get_type_links_inverse(entities)
    entities_dict: dict[int, Any] = {}
    for entity in entities:
        entities_dict[entity.id] = {
            'entity': entity,
            'links': [],
            'links_inverse': [],
            'ext_reference_links': ext_reference_links}
    for link_ in get_all_links(list(entities_dict.keys())):
        entities_dict[link_.domain.id]['links'].append(link_)
    for link_ in get_all_links_inverse(list(entities_dict.keys())):
        entities_dict[link_.range.id]['links_inverse'].append(link_)
    latest_modified = max(
        entity.modified for entity in entities if entity.modified)
    result = []
    for item in entities_dict.values():
        result.append(
            get_subunit(
                item['entity'],
                item['links'],
                item['links_inverse'],
                item['ext_reference_links'],
                root_id,
                latest_modified,
                parser))
    return result


def get_type_links_inverse(entities: list[Entity]) -> list[Link]:
    types = remove_duplicate_entities(
        [type_ for entity in entities for type_ in entity.types])
    links = get_all_links_inverse([type_.id for type_ in types], 'P67')
    return [link_ for link_ in links if
            link_.domain.class_.name == 'reference_system']
