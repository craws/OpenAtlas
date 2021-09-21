from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.enpoints_util import get_node_dict, \
    resolve_node_parser
from openatlas.api.v02.resources.error import InvalidSubunitError
from openatlas.api.v02.resources.parser import default


class GetNodeEntities(Resource):  # type: ignore
    @swag_from("../swagger/nodes.yml", endpoint="api.node_entities")
    def get(self,
            id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_node_parser(
            {"nodes": GetNodeEntities.get_node(id_)}, default.parse_args(), id_)

    @staticmethod
    def get_node(id_: int) -> List[Dict[str, Any]]:
        if id_ not in g.nodes:
            raise InvalidSubunitError  # pragma: no cover
        return [get_node_dict(entity) for entity in
                g.nodes[id_].get_linked_entities(['P2', 'P89'], inverse=True)]
