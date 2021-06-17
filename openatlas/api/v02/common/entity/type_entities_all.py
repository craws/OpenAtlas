from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.error import InvalidSubunitError
from openatlas.api.v02.resources.helpers import resolve_entity
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.util import get_entity_by_id


class GetTypeEntitiesAll(Resource):  # type: ignore
    @swag_from("../swagger/type_entities_all.yml", endpoint="api.type_entities_all")
    def get(self, id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        entities = [get_entity_by_id(entity) for entity in GetTypeEntitiesAll.get_node_all(id_)]
        return resolve_entity(entities, entity_parser.parse_args(), id_)

    @staticmethod
    def get_node_all(id_: int) -> List[int]:
        if id_ not in g.nodes:
            raise InvalidSubunitError
        return GetTypeEntitiesAll.get_recursive_node_entities(id_, [])

    @staticmethod
    def get_recursive_node_entities(id_: int, data: List[int]) -> List[int]:
        for entity in g.nodes[id_].get_linked_entities(['P2', 'P89'], inverse=True):
            data.append(entity.id)
        for sub_id in g.nodes[id_].subs:
            GetTypeEntitiesAll.get_recursive_node_entities(sub_id, data)
        return data
