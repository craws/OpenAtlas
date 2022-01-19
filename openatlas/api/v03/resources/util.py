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
    links = []
    for link in Link.get_links(entities, list(g.properties)):
        links.append(link)
    return links


def get_all_links_inverse(entities: Union[int, list[int]]) -> list[Link]:
    links_inverse = []
    for link in Link.get_links(entities, list(g.properties), inverse=True):
        links_inverse.append(link)
    return links_inverse


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
    entities = [e.id for e in new_entities]
    return get_all_links_inverse(entities) \
        if inverse else get_all_links(entities)


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


def get_by_view(code_: str) -> list[Entity]:
    if code_ not in g.view_class_mapping:
        raise InvalidCodeError
    return Entity.get_by_class(
        g.view_class_mapping[code_],
        types=True,
        aliases=True)


def get_by_class(class_code: str) -> list[Entity]:
    if class_code not in g.cidoc_classes:
        raise InvalidCidocClassCode
    return Entity.get_by_cidoc_class(class_code, types=True, aliases=True)


def get_by_system(system_class: str) -> list[Entity]:
    if system_class not in g.classes:
        raise InvalidSystemClassError
    return Entity.get_by_class(system_class, types=True, aliases=True)


def flatten_list_and_remove_duplicates(list_: list[Any]) -> list[Any]:
    return [item for sublist in list_ for item in sublist if item not in list_]
