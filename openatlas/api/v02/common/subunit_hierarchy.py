import json
from typing import Any, Dict, List, Optional, Tuple

from flask import Response, jsonify, url_for
from flask_restful import Resource, marshal

from openatlas.api.v01.error import APIError
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.templates.nodes import NodeTemplate
from openatlas.models.entity import Entity
from openatlas.models.place import get_structure


class GetSubunitHierarchy(Resource):
    def get(self, id_: int) -> Tuple[Any, int]:

        parser = entity_parser.parse_args()
        node = GetSubunitHierarchy.get_subunit_hierarchy(id_)
        if parser['count']:
            # Todo: very static, make it dynamic
            return jsonify(len(GetSubunitHierarchy.get_subunit_hierarchy(id_)))
        if parser['download']:
            return Response(json.dumps(marshal(node, NodeTemplate.node_template())),
                            mimetype='application/json',
                            headers={
                                'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})
        return marshal(node, NodeTemplate.node_template()), 200

    @staticmethod
    def get_subunit_hierarchy(id_: int) -> List[Dict[str, Any]]:
        try:
            id_ = int(id_)
        except Exception:
            raise APIError('Invalid ID: ' + str(id_), status_code=404, payload="404b")
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            raise APIError('ID ' + str(id_) + ' doesn\'t exist', status_code=404,
                           payload="404a")
        if entity.class_.code in ['E18']:
            return GetSubunitHierarchy.get_subunits_recursive(entity, [])
        else:
            raise APIError('There is no subunit with the ID: ' + str(id_), status_code=404,
                           payload="404g")

    @staticmethod
    def get_subunits_recursive(entity: Optional[Entity], data: List[Dict[str, Any]]) \
            -> List[Dict[str, Any]]:
        structure = get_structure(entity)
        if structure and structure['subunits']:
            for n in structure['subunits']:
                data.append({'id': n.id, 'label': n.name,
                             'url': url_for('api_entity', id_=n.id, _external=True)})
        node = get_structure(entity)
        if node:
            for sub_id in node['subunits']:
                GetSubunitHierarchy.get_subunits_recursive(sub_id, data)
        return data
