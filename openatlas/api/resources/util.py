import ast
from typing import Any, Optional, Union

from flask import g, json

from openatlas.api.resources.error import (
    InvalidSearchSyntax)
from openatlas.api.resources.model_mapper import get_entities_by_ids, \
    get_all_links_of_entities, get_all_links_of_entities_inverse
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem


def get_license(entity: Entity) -> Optional[str]:
    for type_ in entity.types:
        if g.types[type_.root[0]].name == 'License':
            return type_.name
    return None


def to_camel_case(i: str) -> str:
    return (i[0] + i.title().translate(" ")[1:] if i else i).replace(" ", "")


def parser_str_to_dict(parser: list[str]) -> list[dict[str, Any]]:
    try:
        return [ast.literal_eval(p) for p in parser]
    except Exception as e:
        raise InvalidSearchSyntax from e


def get_all_subunits_recursive(
        entity: Entity,
        data: list[Entity]) -> list[Entity]:
    data.append(entity)
    if entity.class_.name not in ['artifact', 'human_remains']:
        if sub_entities := entity.get_linked_entities('P46', types=True):
            for e in sub_entities:
                get_all_subunits_recursive(e, data)
    return data


def replace_empty_list_values_in_dict_with_none(
        data: dict[str, Any]) -> dict[str, Any]:
    for key, value in data.items():
        if isinstance(value, list) and not data[key]:
            data[key] = None
    return data


def get_linked_entities_api(id_: Union[int, list[int]]) -> list[Entity]:
    domain_entity = [link_.range for link_ in get_all_links_of_entities(id_)]
    range_entity = [link_.domain for link_ in get_all_links_of_entities_inverse(id_)]
    return [*range_entity, *domain_entity]


def get_linked_entities_id_api(id_: int) -> list[Entity]:
    domain_ids = [link_.range.id for link_ in get_all_links_of_entities(id_)]
    range_ids = [link_.domain.id for link_ in get_all_links_of_entities_inverse(id_)]
    return [*range_ids, *domain_ids]


def get_entities_linked_to_special_type(id_: int) -> list[Entity]:
    domain_ids = [link_['domain_id'] for link_ in
                  Link.get_links_by_type(g.types[id_])]
    range_ids = [link_['range_id'] for link_ in
                 Link.get_links_by_type(g.types[id_])]
    return get_entities_by_ids(range_ids + domain_ids)


def get_entities_linked_to_special_type_recursive(
        id_: int,
        data: list[int]) -> list[int]:
    for link_ in Link.get_links_by_type(g.types[id_]):
        data.append(link_['domain_id'])
        data.append(link_['range_id'])
    for sub_id in g.types[id_].subs:
        get_entities_linked_to_special_type_recursive(sub_id, data)
    return data


def get_entities_linked_to_type_recursive_(
        id_: int,
        data: list[int]) -> list[int]:
    for sub_id in g.types[id_].subs:
        data.append(sub_id)
        get_entities_linked_to_type_recursive_(sub_id, data)
    return data


def get_entities_from_type_with_subs(id_: int) -> list[Entity]:
    type_ids = get_entities_linked_to_type_recursive_(id_, [id_])
    entity_ids = Link.get_entity_ids_by_type_ids(type_ids)
    return get_entities_by_ids(
        [link_ for link_ in entity_ids if link_ not in type_ids])


def get_entities_by_type(
        entities: list[Entity],
        parser: dict[str, Any]) -> list[Entity]:
    new_entities = []
    for entity in entities:
        if any(ids in [key.id for key in entity.types]
               for ids in parser['type_id']):
            new_entities.append(entity)
    return new_entities


def get_key(entity: Entity, parser: str) -> str:
    if parser == 'cidoc_class':
        return entity.cidoc_class.name
    if parser == 'system_class':
        return entity.class_.name
    return getattr(entity, parser)


def remove_duplicate_entities(entities: list[Entity]) -> list[Entity]:
    seen = set()  # type: ignore
    seen_add = seen.add  # Do not change, faster than always call seen.add()
    return [
        entity for entity in entities
        if not (entity.id in seen or seen_add(entity.id))]


def link_parser_check(
        entities: list[Entity],
        parser: dict[str, Any]) -> list[Link]:
    if any(i in ['relations', 'types', 'depictions', 'links', 'geometry']
           for i in parser['show']):
        return get_all_links_of_entities(
            [entity.id for entity in entities],
            get_properties_for_links(parser))
    return []


def link_parser_check_inverse(
        entities: list[Entity],
        parser: dict[str, Any]) -> list[Link]:
    if any(i in ['relations', 'types', 'depictions', 'links', 'geometry']
           for i in parser['show']):
        return get_all_links_of_entities_inverse(
            [entity.id for entity in entities],
            get_properties_for_links(parser))
    return []


def get_properties_for_links(parser: dict[str, Any]) -> Optional[list[str]]:
    if parser['relation_type']:
        codes = parser['relation_type']
        if 'geometry' in parser['show']:
            codes.append('P53')
        if 'types' in parser['show']:
            codes.append('P2')
        if any(i in ['depictions', 'links'] for i in parser['show']):
            codes.append('P67')
        return codes
    return None


def get_reference_systems(
        links_inverse: list[Link]) -> list[dict[str, Any]]:
    ref = []
    for link_ in links_inverse:
        if not isinstance(link_.domain, ReferenceSystem):
            continue
        system = g.reference_systems[link_.domain.id]
        ref.append({
            'referenceURL': system.website_url,
            'id': link_.description,
            'resolverURL': system.resolver_url,
            'identifier': f"{system.resolver_url or ''}{link_.description}",
            'type': to_camel_case(g.types[link_.type.id].name),
            'referenceSystem': system.name})
    return ref


def get_geometric_collection(
        entity: Entity,
        links: list[Link]) -> Union[dict[str, Any], None]:
    if entity.class_.view == 'place' or entity.class_.name == 'artifact':
        return get_geoms_by_entity(get_location_id(links))
    if entity.class_.name == 'object_location':
        return get_geoms_by_entity(entity.id)
    if entity.class_.view == 'actor':
        geoms = [Gis.get_by_id(link_.range.id) for link_ in links
                 if link_.property.code in ['P74', 'OA8', 'OA9']]
        return {
            'type': 'GeometryCollection',
            'geometries': [geom for sublist in geoms for geom in sublist]}
    if entity.class_.view == 'event':
        geoms = [Gis.get_by_id(link_.range.id) for link_ in links
                 if link_.property.code in ['P7', 'P26', 'P27']]
        return {
            'type': 'GeometryCollection',
            'geometries': [geom for sublist in geoms for geom in sublist]}
    return None


def get_location_id(links: list[Link]) -> int:
    return [l_.range.id for l_ in links if l_.property.code == 'P53'][0]


def get_geoms_by_entity(location_id: int) -> dict[str, Any]:
    geoms = Gis.get_by_id(location_id)
    if len(geoms) == 1:
        return geoms[0]
    return {'type': 'GeometryCollection', 'geometries': geoms}


def get_geometries(parser: dict[str, Any]) -> list[dict[str, Any]]:
    choices = [
        'gisPointAll', 'gisPointSupers', 'gisPointSubs',
        'gisPointSibling', 'gisLineAll', 'gisPolygonAll']
    all_geoms = Gis.get_all()
    out = []
    for item in choices \
            if parser['geometry'] == 'gisAll' else parser['geometry']:
        for geom in json.loads(all_geoms[item]):
            out.append(geom)
    return out


def filter_link_list_by_property_codes(
        links: list[dict[str, Any]],
        codes: list[str]) -> list[dict[str, str]]:
    data = []
    for link_ in links:
        if link_['property_code'] in codes:
            data.append({
                'domain_id': link_['domain_id'],
                'range_id': link_['range_id']})
    return data