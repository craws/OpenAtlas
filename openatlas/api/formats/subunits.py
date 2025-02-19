from operator import attrgetter
from typing import Any, Optional

from flask import g

from openatlas.api.resources.util import (
    geometry_to_geojson, get_license_name,
    get_reference_systems, remove_duplicate_entities,
    replace_empty_list_values_in_dict_with_none)
from openatlas.display.util import get_file_path
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis


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
                geometry_to_geojson(data['geoms']),
                data['parser']),
        'children': get_children(data),
        'properties': get_properties(data)})


def get_parent(links: list[Link]) -> Optional[int]:
    for link_ in links:
        if link_.property.code == 'P46':
            return link_.domain.id
    return None


def get_children(data: dict[str, Any]) -> list[int | dict[str, Any]]:
    children = [
        link_.range.id for link_ in data['links'] if
        link_.property.code == 'P46']
    return [{'child': child} for child in children] \
        if data['parser']['format'] == 'xml' else children


def get_geometries_thanados(
        geom: Optional[dict[str, Any]],
        parser: dict[str, Any]) -> list[Any] | dict[str, Any] | None:
    if parser['format'] == 'xml' and geom:
        if geom['type'] == 'GeometryCollection':
            geometries = []
            for item in geom['geometries']:
                if not item:
                    continue  # pragma: no cover
                item['coordinates'] = transform_geometries_for_xml(item)
                geometries.append(item)
            geom['geometries'] = [{'geom': item} for item in geometries]
        else:  # pragma: no cover
            geom['coordinates'] = transform_geometries_for_xml(geom)
    return geom


def transform_geometries_for_xml(geom: dict[str, Any]) -> list[Any]:
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


def transform_coordinates_for_xml(coord: list[float]) -> list[Any]:
    return [{'coordinate': {'longitude': coord[0], 'latitude': coord[1]}}]


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
        'earliestBegin': str(entity.begin_from) or None,
        'latestBegin': str(entity.begin_to) or None,
        'earliestEnd': str(entity.end_from) or None,
        'latestEnd': str(entity.end_to) or None}


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
            'license': get_license_name(link.domain),
            'creator': link.domain.creator,
            'licenseHolder': link.domain.license_holder,
            'publicShareable': link.domain.public,
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
        type_ref_link = [
            link for link in data['ext_reference_links']
            if link.range.id == type_.id]
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
    entities = ([entity] +
                entity.get_linked_entities_recursive('P46', types=True))
    entities.sort(key=attrgetter('id'))
    links = Entity.get_links_of_entities([e.id for e in entities])
    links_inverse = (
        Entity.get_links_of_entities([e.id for e in entities], inverse=True))
    latest_modified = max(
        entity.modified for entity in entities if entity.modified)

    link_dict: dict[int, dict[str, list[Any]]] = {}
    for entity_ in entities:
        link_dict[entity_.id] = {
            'links': [],
            'links_inverse': [],
            'geoms': []}
    for link_ in links:
        link_dict[link_.domain.id]['links'].append(link_)
    for link_ in links_inverse:
        link_dict[link_.range.id]['links_inverse'].append(link_)
    for id_, geom in Gis.get_by_entities(entities).items():
        link_dict[id_]['geoms'].extend(geom)
    if parser['centroid']:
        for id_, geom in \
                Gis.get_centroids_by_entities(entities).items():
            link_dict[id_]['geoms'].extend(geom)

    external_reference = get_type_links_inverse(entities)
    entities_dict: dict[int, Any] = {}
    for entity_ in entities:
        entities_dict[entity_.id] = {
            'entity': entity_,
            'links': link_dict[entity_.id]['links'],
            'links_inverse': link_dict[entity_.id]['links_inverse'],
            'geoms': link_dict[entity_.id]['geoms'],
            'ext_reference_links': external_reference,
            'root_id': entity.id,
            'latest_modified': latest_modified,
            'parser': parser}
    return [get_subunit(item) for item in entities_dict.values()]


def get_type_links_inverse(entities: list[Entity]) -> list[Link]:
    types = remove_duplicate_entities(
        [type_ for entity in entities for type_ in entity.types])
    links = Entity.get_links_of_entities(
        [type_.id for type_ in types],
        'P67',
        inverse=True)
    return [link_ for link_ in links if
            link_.domain.class_.name == 'reference_system']
