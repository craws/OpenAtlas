import ast
from typing import Any, Dict, List, Optional, Union

from flask import g

from openatlas.api.v03.resources.error import EntityDoesNotExistError
from openatlas.models.entity import Entity
from openatlas.models.link import Link


def get_entity_by_id(id_: int) -> Entity:
    try:
        entity = Entity.get_by_id(id_, types=True, aliases=True)
    except Exception:
        raise EntityDoesNotExistError
    return entity


def get_entities_by_ids(ids: List[int]) -> List[Entity]:
    return Entity.get_by_ids(ids, types=True, aliases=True)


def get_all_links(entities: Union[int, List[int]]) -> List[Link]:
    links = []
    for link in Link.get_links(entities, list(g.properties)):
        links.append(link)
    return links


def get_all_links_inverse(entities: Union[int, List[int]]) -> List[Link]:
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


def parser_str_to_dict(parser: List[str]) -> List[Dict[str, Any]]:
    return [ast.literal_eval(p) for p in parser]


def link_builder(
        new_entities: List[Entity],
        inverse: bool = False) -> List[Link]:
    entities = [e.id for e in new_entities]
    return get_all_links_inverse(entities) \
        if inverse else get_all_links(entities)

def get_all_subunits_recursive(
        entity: Entity,
        data: List[Dict[Entity, List[Any]]]) -> List[Dict[Any, Any]]:
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
