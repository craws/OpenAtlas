from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, g, jsonify, url_for
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidSubunitError
from openatlas.api.v02.resources.parser import default_parser
from openatlas.api.v02.templates.nodes import NodeTemplate
from openatlas.util.util import api_access


class GetNodeEntitiesAll(Resource):  # type: ignore
    @api_access()  # type: ignore
    @swag_from("../swagger/nodes_all.yml", endpoint="node_entities_all")
    def get(self, id_: int) -> Union[Tuple[Resource, int], Response]:
        parser = default_parser.parse_args()
        node = {"nodes": GetNodeEntitiesAll.get_node_all(id_)}
        template = NodeTemplate.node_template()
        if parser['count']:
            return jsonify(len(node['nodes']))
        if parser['download']:
            return Download.download(data=node, template=template, name=id_)
        return marshal(node, template), 200

    @staticmethod
    def get_node_all(id_: int) -> List[Dict[str, Any]]:
        if id_ not in g.nodes:
            raise InvalidSubunitError  # pragma: no cover
        return GetNodeEntitiesAll.get_recursive_node_entities(id_, [])

    @staticmethod
    def get_recursive_node_entities(id_: int, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        entities = g.nodes[id_].get_linked_entities(['P2', 'P89'], inverse=True)
        for e in entities:
            data.append({'id': e.id, 'label': e.name,
                         'url': url_for('entity', id_=e.id, _external=True)})
        node = g.nodes[id_]
        for sub_id in node.subs:
            GetNodeEntitiesAll.get_recursive_node_entities(sub_id, data)
        return data
