import json
from typing import Any, Dict, List, Tuple

from flask import Response, jsonify, url_for
from flask_restful import Resource, marshal

from openatlas.api.v01.error import APIError
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.templates.nodes import NodeTemplate
from openatlas.models.entity import Entity
from openatlas.models.place import get_structure


class GetSubunit(Resource):
    def get(self, id_: int) -> Tuple[Any, int]:
        parser = entity_parser.parse_args()
        node = GetSubunit.get_subunits(id_)
        if parser['count']:
            # Todo: very static, make it dynamic
            return jsonify(len(GetSubunit.get_subunits(id_)))
        if parser['download']:
            return Response(json.dumps(marshal(node, NodeTemplate.node_template())),
                            mimetype='application/json',
                            headers={
                                'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})
        return marshal(node, NodeTemplate.node_template()), 200

    @staticmethod
    def get_subunits(id_: int) -> List[Dict[str, Any]]:
        # Get first level of subunits
        try:
            id_ = int(id_)
        except Exception:
            raise APIError('Invalid ID: ' + str(id_), status_code=404, payload="404b")
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            raise APIError('ID ' + str(id_) + ' doesn\'t exist', status_code=404,
                           payload="404a")
        structure = get_structure(entity)
        data = []
        if structure and structure['subunits']:
            for n in structure['subunits']:
                data.append({'id': n.id, 'label': n.name,
                             'url': url_for('api_entity', id_=n.id, _external=True)})
        else:  # pragma: no cover
            raise APIError('There is no subunit with the ID: ' + str(id_), status_code=404,
                           payload="404g")
        return data
