from typing import Any, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v03.resources.error import InvalidSubunitError
from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.api.v03.resources.util import get_entities_by_ids
from openatlas.models.entity import Entity
from openatlas.models.link import Link


class GetTypeEntitiesAll(Resource):
    @staticmethod
    @swag_from(
        "../swagger/type_entities_all.yml",
        endpoint="api_03.type_entities_all")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        entities = [entity for entity in GetTypeEntitiesAll.get_node_all(id_)]
        if not entities:
            entities = get_entities_by_ids(
                GetTypeEntitiesAll.get_special_node(id_, []))
        return resolve_entities(entities, entity_.parse_args(), id_)

    @staticmethod
    def get_node_all(id_: int) -> list[Entity]:
        if id_ not in g.types:
            raise InvalidSubunitError
        return GetTypeEntitiesAll.get_recursive_node_entities(id_, [])

    @staticmethod
    def get_recursive_node_entities(
            id_: int,
            data: list[Entity]) -> list[Entity]:
        for entity in g.types[id_].get_linked_entities(
                ['P2', 'P89'],
                inverse=True,
                types=True):
            data.append(entity)
        for sub_id in g.types[id_].subs:
            GetTypeEntitiesAll.get_recursive_node_entities(sub_id, data)
        return data

    @staticmethod
    def get_special_node(id_: int, data: list[int]) -> list[int]:
        for link_ in Link.get_links_by_type(g.types[id_]):
            data.append(link_['domain_id'])
            data.append(link_['range_id'])
        for sub_id in g.types[id_].subs:
            GetTypeEntitiesAll.get_special_node(sub_id, data)
        return data
