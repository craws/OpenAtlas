from typing import Any, Dict, List, Tuple, Union

# from flasgger import swag_from
from flask import Response, jsonify
from flask_restful import Resource, marshal

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
    # @swag_from("../swagger/code.yml", endpoint="code")
    def get(self, code: str) -> Union[Tuple[Resource, int], Response]:
        parser = entity_parser.parse_args()
        code_ = Pagination.pagination(
            GetByCode.get_entities_by_menu_item(code_=code, parser=parser),
            parser=parser)
        template = GeoJson.pagination(parser['show'])
        if parser['count']:
            return jsonify(code_['pagination']['entities'])
        if parser['download']:
            return Download.download(data=code_, template=template, name=code)
        return marshal(code_, template), 200

    @staticmethod
    def get_entities_by_menu_item(code_: str, parser: Dict[str, Any]) -> List[Entity]:
        entities = []
        if code_ not in ['actor', 'event', 'place', 'reference', 'source', 'artifact']:
            raise InvalidCodeError  # pragma: no cover
        for entity in Query.get_by_menu_item_api(code_, parser):
            entities.append(entity)
        return entities
