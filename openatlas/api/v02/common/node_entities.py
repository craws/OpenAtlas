from typing import Any, Dict, List, Tuple

from flasgger import swag_from
from flask import g, jsonify, url_for
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.error import Error
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.parser import default_parser
from openatlas.api.v02.templates.nodes import NodeTemplate


class GetNodeEntities(Resource):
    @swag_from("nodes.yml")
    def get(self, id_: int) -> Tuple[Any, int]:
        parser = default_parser.parse_args()
        node = GetNodeEntities.get_node(id_)
        template = NodeTemplate.node_template()
        if parser['count']:
            return jsonify(len(node))
        if parser['download']:
            return Download.download(data=node, template=template, name=id_)
        return marshal(node, template), 200

    @staticmethod
    def get_node(id_: int) -> List[Dict[str, Any]]:
        if id_ not in g.nodes:
            # Todo: Eliminate Error
            raise Error('Node ID ' + str(id_) + ' doesn\'t exist', status_code=404,
                           payload="404g")
        entities = g.nodes[id_].get_linked_entities(['P2', 'P89'], inverse=True)
        data = []
        for e in entities:
            data.append({'id': e.id, 'label': e.name,
                         'url': url_for('api_entity', id_=e.id, _external=True)})
        return data
