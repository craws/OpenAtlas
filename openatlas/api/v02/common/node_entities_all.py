from typing import Any, Dict, List, Tuple

from flask import g, jsonify, url_for
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.error import Error
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.parser import default_parser
from openatlas.api.v02.templates.nodes import NodeTemplate


class GetNodeEntitiesAll(Resource):
    def get(self, id_: int) -> Tuple[Any, int]:
        parser = default_parser.parse_args()
        node = GetNodeEntitiesAll.get_node_all(id_)
        template = NodeTemplate.node_template()
        if parser['count']:
            return jsonify(len(node))
        if parser['download']:
            return Download.download(data=node, template=template, name=id_)
        return marshal(node, template), 200

    @staticmethod
    def get_node_all(id_: int) -> List[Dict[str, Any]]:
        if id_ not in g.nodes:
            # Todo: Eliminate Error
            raise Error('Node ID ' + str(id_) + ' doesn\'t exist', status_code=404,
                           payload="404g")
        return GetNodeEntitiesAll.get_recursive_node_entities(id_, [])

    @staticmethod
    def get_recursive_node_entities(id_: int, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        entities = g.nodes[id_].get_linked_entities(['P2', 'P89'], inverse=True)
        for e in entities:
            data.append({'id': e.id, 'label': e.name,
                         'url': url_for('api_entity', id_=e.id, _external=True)})
        node = g.nodes[id_]
        for sub_id in node.subs:
            GetNodeEntitiesAll.get_recursive_node_entities(sub_id, data)
        return data
