from typing import Any, Dict, List, Optional, Tuple

from flasgger import swag_from
from flask import jsonify, url_for
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.error import Error
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.parser import default_parser
from openatlas.api.v02.templates.nodes import NodeTemplate
from openatlas.models.entity import Entity
from openatlas.models.place import get_structure


class GetSubunitHierarchy(Resource):
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
            # Todo: Eliminate Error
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            raise Error('ID ' + str(id_) + ' doesn\'t exist', status_code=404,
                           payload="404a")
        if entity.class_.code in ['E18']:
            return GetSubunitHierarchy.get_subunits_recursive(entity, [])
        else:
            # Todo: Eliminate Error
            raise Error('There is no subunit with the ID: ' + str(id_), status_code=404,
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
