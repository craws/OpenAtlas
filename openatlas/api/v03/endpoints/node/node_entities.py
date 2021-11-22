from typing import Any, Dict, List, Tuple, Union

from flask import Response, g
from flask_restful import Resource

from openatlas.api.v03.resources.error import InvalidSubunitError
from openatlas.api.v03.resources.parser import default
from openatlas.api.v03.resources.resolve_endpoints import get_node_dict, \
    resolve_node_parser


class GetNodeEntities(Resource):

    def get(self,
            id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_node_parser(
            {"nodes": GetNodeEntities.get_node(id_)}, default.parse_args(), id_)

    @staticmethod
    def get_node(id_: int) -> List[Dict[str, Any]]:
        if id_ not in g.nodes:
            raise InvalidSubunitError
        return [get_node_dict(entity) for entity in
                g.nodes[id_].get_linked_entities(['P2', 'P89'], inverse=True)]
