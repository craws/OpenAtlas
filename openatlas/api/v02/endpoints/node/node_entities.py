from typing import Any, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.error import InvalidSubunitError
from openatlas.api.v02.resources.parser import default
from openatlas.api.v02.resources.resolve_endpoints import (
    get_node_dict, resolve_node_parser)


class GetNodeEntities(Resource):
    @staticmethod
    @swag_from("../swagger/nodes.yml", endpoint="api_02.node_entities")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_node_parser(
            {"nodes": GetNodeEntities.get_node(id_)}, default.parse_args(), id_)

    @staticmethod
    def get_node(id_: int) -> list[dict[str, Any]]:
        if id_ not in g.types:
            raise InvalidSubunitError  # pragma: no cover
        return [get_node_dict(entity) for entity in
                g.types[id_].get_linked_entities(['P2', 'P89'], inverse=True)]
