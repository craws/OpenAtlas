from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from flask import g

from openatlas.api.v03.resources.formats.linked_places import get_geometries
from openatlas.api.v03.resources.formats.linked_places_helper import \
    get_reference_systems
from openatlas.api.v03.resources.util import get_license
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.type import Type
from openatlas.util.util import get_file_path


def get_subunits(
        entity: Entity,
        children: List[Entity],
        links: List[Link],
        links_inverse: List[Link],
        root: Entity,
        latest_mod_rec: datetime,
        parser: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'id': entity.id,
        'rootId': root.id,
        'parentId':
            entity.get_linked_entity_safe('P46', inverse=True).id
            if entity.id != root.id else None,
        'openatlasClassName': entity.class_.name,
        'crmClass': entity.cidoc_class.code,
        'created': str(entity.created),
        'modified': str(entity.modified),
        'latestModRec': latest_mod_rec,
        'geometry': get_geometries_thanados(entity, links, parser),
        'children': get_children(children, parser),
        'properties': get_properties(entity, links, links_inverse, parser)}


def get_geometries_thanados(
        entity: Entity,
        links: List[Link],
        parser: Dict[str, Any]) -> Union[List[Any], None, Dict[str, Any]]:
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


def check_geometries(geom: Dict[str, Any]) \
        -> Union[List[List[Dict[str, Any]]], List[Dict[str, Any]], None]:
    if geom['type'] == 'Polygon':  # pragma: no cover
        return [transform_coords(k) for i in geom['coordinates'] for k in i]
    if geom['type'] == 'LineString':  # pragma: no cover
        return [transform_coords(k) for k in geom['coordinates']]
    if geom['type'] == 'Point':
        return transform_coords(geom['coordinates'])
    return None  # pragma: no cover


def transform_coords(coords: List[float]) -> List[Dict[str, Any]]:
    return [{'coordinate': {'longitude': coords[0], 'latitude': coords[1]}}]


def get_children(
        children: List[Entity],
        parser: Dict[str, Any]) -> \
        Optional[Union[List[int], List[Dict[str, Any]]]]:
    if parser['format'] == 'xml':
        return [{'child': child.id} for child in children] if children else None
    return [child.id for child in children] if children else None


def get_properties(
        entity: Entity,
        links: List[Link],
        links_inverse: List[Link],
        parser: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'name': entity.name,
        'aliases': get_aliases(entity, parser),
        'description': entity.description,
        'standardType':
            get_standard_type(entity.standard_type)
            if entity.standard_type else None,
        'timespan': get_timespans(entity),
        'externalReferences': get_ref_system(links_inverse, parser),
        'references': get_references(links_inverse, parser),
        'files': get_file(links_inverse, parser),
        'types': get_types(entity, links, parser)}


def get_standard_type(type_: Type) -> Dict[str, Any]:
    types_dict = {
        'id': type_.id,
        'name': type_.name}
    hierarchy = [g.types[root].name for root in type_.root]
    hierarchy.reverse()
    types_dict['path'] = ' > '.join(map(str, hierarchy))
    types_dict['rootId'] = type_.root[0]
    return types_dict


def get_aliases(entity: Entity, parser: Dict[str, Any]) -> Optional[List[Any]]:
    aliases = list(entity.aliases.values()) if entity.aliases.values() else None
    if parser['format'] == 'xml':
        return [{'alias': alias} for alias in aliases] if aliases else None
    return aliases


def get_ref_system(
        links_inverse: List[Link],
        parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    ref_sys = get_reference_systems(links_inverse)
    if ref_sys and parser['format'] == 'xml':
        return [{'externalReference': ref} for ref in ref_sys]
    return ref_sys


def get_references(
        links: List[Link],
        parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    references = []
    for link_ in links:
        if link_.property.code == "P67" and link_.domain.class_.name in \
                ['bibliography', 'edition', 'external_reference']:
            references.append({
                'abbreviation': link_.domain.name,
                'id': link_.domain.id,
                'title': link_.domain.description,
                'pages': link_.description if link_.description else None})
    if parser['format'] == 'xml':
        return [
            {'reference': ref} for ref in references] if references else None
    return references if references else None


def get_timespans(entity: Entity) -> Dict[str, Any]:
    return {
        'earliestBegin': str(entity.begin_from) if entity.begin_from else None,
        'latestBegin': str(entity.begin_to) if entity.begin_to else None,
        'earliestEnd': str(entity.end_from) if entity.end_from else None,
        'latestEnd': str(entity.end_to) if entity.end_to else None}


def get_file(
        links_inverse: List[Link],
        parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
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
            'source':
                link.domain.description if link.domain.description else None})
    if parser['format'] == 'xml':
        return [{'file': file} for file in files] if files else None
    return files if files else None


def get_types(
        entity: Entity,
        links: List[Link],
        parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    types = []
    for type_ in entity.types:
        if type_.category == 'standard':
            continue
        types_dict = {
            'id': type_.id,
            'name': type_.name}
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
        return [{'type': type_} for type_ in types] if types else None
    return types if types else None
