from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, jsonify, url_for
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


class GetSubunit(Resource):  # type: ignore
    @api_access()  # type: ignore
    @cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
    @swag_from("../swagger/nodes.yml", endpoint="subunit")
    def get(self, id_: int) -> Union[Tuple[Resource, int], Response]:
        parser = default_parser.parse_args()
        node = {"nodes": GetSubunit.get_subunits(id_)}
        template = NodeTemplate.node_template()
        if parser['count']:
            return jsonify(len(node['nodes']))
        if parser['download']:
            return Download.download(data=node, template=template, name=id_)
        return marshal(node, template), 200

    @staticmethod
    def get_subunits(id_: int) -> List[Dict[str, Any]]:
        # Get first level of subunits
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            raise EntityDoesNotExistError
        structure = get_structure(entity)
        data = []
        if structure and structure['subunits']:
            for n in structure['subunits']:
                data.append({'id': n.id, 'label': n.name,
                             'url': url_for('entity', id_=n.id, _external=True)})
        else:  # pragma: no cover
            raise InvalidSubunitError
        return data
