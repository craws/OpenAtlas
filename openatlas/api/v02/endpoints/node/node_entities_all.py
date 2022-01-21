from typing import Any, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.error import InvalidSubunitError
from openatlas.api.v02.resources.parser import default
from openatlas.api.v02.resources.resolve_endpoints import get_node_dict, \
    resolve_node_parser


class GetNodeEntitiesAll(Resource):
    @staticmethod
    @swag_from("../swagger/nodes_all.yml", endpoint="api_02.node_entities_all")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_node_parser(
            {"nodes": GetNodeEntitiesAll.get_node_all(id_)},
            default.parse_args(),
            id_)

    @staticmethod
    def get_node_all(id_: int) -> list[dict[str, Any]]:
        if id_ not in g.types:
            raise InvalidSubunitError  # pragma: no cover
        return GetNodeEntitiesAll.get_recursive_node_entities(id_, [])

    @staticmethod
    def get_recursive_node_entities(id_: int, data: list[dict[str, Any]]) \
            -> list[dict[str, Any]]:
        for entity in g.types[id_].get_linked_entities(['P2', 'P89'],
                                                       inverse=True):
            data.append(get_node_dict(entity))
        for sub_id in g.types[id_].subs:
            GetNodeEntitiesAll.get_recursive_node_entities(sub_id, data)
        return data
