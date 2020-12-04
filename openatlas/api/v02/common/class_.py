from typing import Any, Dict, List, Tuple

from flasgger import swag_from
from flask import g, jsonify
from flask_cors import cross_origin
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidCidocClassCode
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.sql import Query
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.models.entity import Entity
from openatlas.util.util import api_access


class GetByClass(Resource):
    @api_access()  # type: ignore
    @cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
    @swag_from("../swagger/class.yml", endpoint="class")
    def get(self, class_code: str) -> Tuple[Resource, int]:
        parser = entity_parser.parse_args()
        class_ = Pagination.pagination(
            GetByClass.get_entities_by_class(class_code=class_code, parser=parser),
            parser=parser)
        template = GeoJson.pagination(parser['show'])
        if parser['count']:
            return jsonify(class_[1][0]['entities'])
        if parser['download']:
            return Download.download(data=class_, template=template, name=class_code)
        return marshal(class_, template), 200

    @staticmethod
    def get_entities_by_class(class_code: str, parser: Dict[str, Any]) -> List[Entity]:
        entities = []
        if class_code not in g.classes:
            raise InvalidCidocClassCode
        for entity in Query.get_by_class_code_api(class_code, parser):
            entities.append(entity)
        return entities
