import ast
from typing import Any, Optional, Union

from flask import g

from openatlas.api.v03.resources.error import EntityDoesNotExistError, \
    InvalidCidocClassCode, InvalidCodeError, InvalidSearchSyntax, \
    InvalidSystemClassError
from openatlas.models.entity import Entity
from openatlas.models.link import Link


def get_entity_by_id(id_: int) -> Entity:
    try:
        entity = Entity.get_by_id(id_, types=True, aliases=True)
    except Exception as e:
        raise EntityDoesNotExistError from e
    return entity


def get_entities_by_ids(ids: list[int]) -> list[Entity]:
    return Entity.get_by_ids(ids, types=True, aliases=True)


def get_all_links(entities: Union[int, list[int]]) -> list[Link]:
    return Link.get_links(entities, list(g.properties))


def get_all_links_inverse(entities: Union[int, list[int]]) -> list[Link]:
    return Link.get_links(entities, list(g.properties), inverse=True)


def get_license(entity: Entity) -> Optional[str]:
    for node in entity.types:
        if g.types[node.root[0]].name == 'License':
            return node.name
    return None


def to_camel_case(i: str) -> str:
    return (i[0] + i.title().translate(" ")[1:] if i else i).replace(" ", "")


def parser_str_to_dict(parser: list[str]) -> list[dict[str, Any]]:
    try:
        return [ast.literal_eval(p) for p in parser]
    except Exception as e:
        raise InvalidSearchSyntax from e


def link_builder(
        new_entities: list[Entity],
        inverse: bool = False) -> list[Link]:
    e = [e.id for e in new_entities]
    return get_all_links_inverse(e) if inverse else get_all_links(e)


def get_all_subunits_recursive(
        entity: Entity,
        data: list[dict[Entity, Any]]) -> list[dict[Any, Any]]:
    if entity.class_.name not in ['artifact', 'human_remains']:
        sub_entities = entity.get_linked_entities('P46', types=True)
        data[-1] = {entity: sub_entities if sub_entities else None}
        if sub_entities:
            for e in sub_entities:
                data.append({e: []})
        if sub_entities:
            for e in sub_entities:
                get_all_subunits_recursive(e, data)
    return data


def replace_empty_list_values_in_dict_with_none(
        data: dict[str, Any]) -> dict[str, Any]:
    for key, value in data.items():
        if isinstance(value, list) and not data[key]:
            data[key] = None
    return data


def get_by_cidoc_classes(class_codes: list[str]) -> list[Entity]:
    if not all(cc in g.cidoc_classes for cc in class_codes):
        raise InvalidCidocClassCode
    return Entity.get_by_cidoc_class(class_codes, types=True, aliases=True)


def get_entities_by_view_classes(codes: list[str]) -> list[Entity]:
    codes = list(g.view_class_mapping.keys()) if 'all' in codes else codes
    if not all(c in g.view_class_mapping for c in codes):
        raise InvalidCodeError
    view_classes = flatten_list_and_remove_duplicates(
        [g.view_class_mapping[view] for view in codes])
    return Entity.get_by_class(view_classes, types=True, aliases=True)


def get_entities_by_system_classes(system_classes: list[str]) -> list[Entity]:
    system_classes = list(g.classes.keys()) \
        if 'all' in system_classes else system_classes
    if not all(sc in g.classes for sc in system_classes):
        raise InvalidSystemClassError
    return Entity.get_by_class(system_classes, types=True, aliases=True)


def flatten_list_and_remove_duplicates(list_: list[Any]) -> list[Any]:
    return [item for sublist in list_ for item in sublist if item not in list_]


def get_linked_entities_api(id_: Union[int, list[int]]) -> list[Entity]:
    domain_entity = [link_.range for link_ in get_all_links(id_)]
    range_entity = [link_.domain for link_ in get_all_links_inverse(id_)]
    return [*range_entity, *domain_entity]


def get_linked_entities_id_api(id_: int) -> list[Entity]:
    domain_ids = [link_.range.id for link_ in get_all_links(id_)]
    range_ids = [link_.domain.id for link_ in get_all_links_inverse(id_)]
    return [*range_ids, *domain_ids]


def get_entities_linked_to_type_recursive(
        id_: int,
        data: list[Entity]) -> list[Entity]:
    for entity in g.types[id_].get_linked_entities(
            ['P2', 'P89'],
            inverse=True,
            types=True):
        data.append(entity)
    for sub_id in g.types[id_].subs:
        get_entities_linked_to_type_recursive(sub_id, data)
    return data


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
    seen_add = seen.add  # Do not change, faster than always call seen.add(e.id)
    return [
        entity for entity in entities
        if not (entity.id in seen or seen_add(entity.id))]


def link_parser_check(
        new_entities: list[Entity],
        parser: dict[str, Any],
        inverse: bool = False) -> list[Link]:
    if any(i in ['relations', 'types', 'depictions', 'links', 'geometry']
           for i in parser['show']):
        return link_builder(new_entities, inverse)
    return []
