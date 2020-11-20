from typing import Any, Dict, List, Tuple

from flask import jsonify, url_for
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.error import Error
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.parser import default_parser
from openatlas.api.v02.templates.nodes import NodeTemplate
from openatlas.models.entity import Entity
from openatlas.models.place import get_structure


class GetSubunit(Resource):
    def get(self, id_: int) -> Tuple[Any, int]:
        parser = default_parser.parse_args()
        node = GetSubunit.get_subunits(id_)
        template = NodeTemplate.node_template()
        if parser['count']:
            return jsonify(len(node))
        if parser['download']:
            return Download.download(data=node, template=template, name=id_)
        return marshal(node, template), 200

    @staticmethod
    def get_subunits(id_: int) -> List[Dict[str, Any]]:
        # Get first level of subunits
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            # Todo: Eliminate Error
            raise Error('ID ' + str(id_) + ' doesn\'t exist', status_code=404,
                           payload="404a")
        structure = get_structure(entity)
        data = []
        if structure and structure['subunits']:
            for n in structure['subunits']:
                data.append({'id': n.id, 'label': n.name,
                             'url': url_for('api_entity', id_=n.id, _external=True)})
        else:  # pragma: no cover
            raise Error('There is no subunit with the ID: ' + str(id_), status_code=404,
                           payload="404g")
        return data
