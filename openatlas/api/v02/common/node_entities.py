from typing import Any, Dict, List, Tuple, Union

# from flasgger import swag_from
from flask import Response, g, jsonify, url_for
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidSubunitError
from openatlas.api.v02.resources.parser import default_parser
from openatlas.api.v02.templates.nodes import NodeTemplate
from openatlas.util.util import api_access


class GetNodeEntities(Resource):  # type: ignore
    @api_access()  # type: ignore
    # @swag_from("../swagger/nodes.yml", endpoint="node_entities")
    def get(self, id_: int) -> Union[Tuple[Resource, int], Response]:
        parser = default_parser.parse_args()
        node = {"nodes": GetNodeEntities.get_node(id_)}
        template = NodeTemplate.node_template()
        if parser['count']:
            return jsonify(len(node['nodes']))
        if parser['download']:
            return Download.download(data=node, template=template, name=id_)
        return marshal(node, template), 200

    @staticmethod
    def get_node(id_: int) -> List[Dict[str, Any]]:
        if id_ not in g.nodes:
            raise InvalidSubunitError  # pragma: no cover
        entities = g.nodes[id_].get_linked_entities(['P2', 'P89'], inverse=True)
        data = []
        for e in entities:
            data.append({
                'id': e.id, 'label': e.name,
                'url': url_for('entity', id_=e.id, _external=True)})
        return data
