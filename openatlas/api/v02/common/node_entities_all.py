import json
from typing import Any, Dict, List, Tuple

from flask import Response, g, jsonify, url_for
from flask_restful import Resource, marshal

from openatlas.api.v01.error import APIError
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.templates.nodes import NodeTemplate


class GetNodeEntitiesAll(Resource):
    def get(self, id_: int) -> Tuple[Any, int]:
        parser = entity_parser.parse_args()
        node = GetNodeEntitiesAll.get_node_all(id_)
        if parser['count']:
            # Todo: very static, make it dynamic
            return jsonify(len(GetNodeEntitiesAll.get_node(id_)))
        if parser['download']:
            return Response(json.dumps(marshal(node, NodeTemplate.node_template())),
                            mimetype='application/json',
                            headers={
                                'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})
        return marshal(node, NodeTemplate.node_template()), 200

    @staticmethod
    def get_node_all(id_: int) -> List[Dict[str, Any]]:
        try:
            id_ = int(id_)
        except Exception:
            raise APIError('Invalid ID: ' + str(id_), status_code=404, payload="404b")
        if id_ not in g.nodes:
            raise APIError('Node ID ' + str(id_) + ' doesn\'t exist', status_code=404,
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
