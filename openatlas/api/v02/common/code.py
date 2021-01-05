from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, jsonify
from flask_cors import cross_origin
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidCodeError
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.sql import Query
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.models.entity import Entity
from openatlas.util.util import api_access


class GetByCode(Resource):  # type: ignore
    @api_access()  # type: ignore
    @cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
    @swag_from("../swagger/code.yml", endpoint="code")
    def get(self, item: str) -> Union[Tuple[Resource, int], Response]:
        parser = entity_parser.parse_args()
        code = Pagination.pagination(
            GetByCode.get_entities_by_menu_item(code_=item, parser=parser),
            parser=parser)
        template = GeoJson.pagination(parser['show'])
        if parser['count']:
            return jsonify(code['pagination'][0]['entities'])
        if parser['download']:
            return Download.download(data=code, template=template, name=item)
        return marshal(code, template), 200

    @staticmethod
    def get_entities_by_menu_item(code_: str, parser: Dict[str, Any]) -> List[Entity]:
        entities = []
        if code_ not in ['actor', 'event', 'place', 'reference', 'source', 'object']:
            raise InvalidCodeError
        for entity in Query.get_by_menu_item_api(code_, parser):
            entities.append(entity)
        return entities
