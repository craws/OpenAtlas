from typing import Any, Dict, List, Optional, Tuple

from flasgger import swag_from
from flask import jsonify, url_for
from flask_cors import cross_origin
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import EntityDoesNotExistError, InvalidSubunitError
from openatlas.api.v02.resources.parser import default_parser
from openatlas.api.v02.templates.nodes import NodeTemplate
from openatlas.models.entity import Entity
from openatlas.models.place import get_structure
from openatlas.util.util import api_access


class GetSubunitHierarchy(Resource):
    @api_access()  # type: ignore
    @cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
    @swag_from("../swagger/nodes.yml", endpoint="subunit_hierarchy")
    def get(self, id_: int) -> Tuple[Resource, int]:
        parser = default_parser.parse_args()
        node = GetSubunitHierarchy.get_subunit_hierarchy(id_)
        template = NodeTemplate.node_template()
        if parser['count']:
            return jsonify(len(node))
        if parser['download']:
            return Download.download(data=node, template=template, name=id_)
        return marshal(node, template), 200

    @staticmethod
    def get_subunit_hierarchy(id_: int) -> List[Dict[str, Any]]:
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except EntityDoesNotExistError:
            raise EntityDoesNotExistError
        if entity.class_.code in ['E18']:
            return GetSubunitHierarchy.get_subunits_recursive(entity, [])
        else:
            raise InvalidSubunitError

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
