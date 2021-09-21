from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.enpoints_util import get_node_dict, \
    resolve_node_parser
from openatlas.api.v02.resources.error import InvalidSubunitError
from openatlas.api.v02.resources.parser import default


class GetNodeEntitiesAll(Resource):  # type: ignore
    @swag_from("../swagger/nodes_all.yml", endpoint="api.node_entities_all")
    def get(self,
            id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_node_parser(
            {"nodes": GetNodeEntitiesAll.get_node_all(id_)},
            default.parse_args(),
            id_)

    @staticmethod
    def get_node_all(id_: int) -> List[Dict[str, Any]]:
        if id_ not in g.nodes:
            raise InvalidSubunitError  # pragma: no cover
        return GetNodeEntitiesAll.get_recursive_node_entities(id_, [])

    @staticmethod
    def get_recursive_node_entities(id_: int, data: List[Dict[str, Any]]) \
            -> List[Dict[str, Any]]:
        for entity in g.nodes[id_].get_linked_entities(['P2', 'P89'],
                                                       inverse=True):
            data.append(get_node_dict(entity))
        for sub_id in g.nodes[id_].subs:
            GetNodeEntitiesAll.get_recursive_node_entities(sub_id, data)
        return data
