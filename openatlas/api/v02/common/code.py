import json
from typing import Any, Dict, List, Tuple

from flask import Response, jsonify, request
from flask_restful import Resource, marshal

from openatlas.api.v01.error import APIError
from openatlas.api.v01.parameter import Validation
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.sql import Query
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.models.entity import Entity


class GetByCode(Resource):
    def get(self, item: str) -> Tuple[Any, int]:
        validation = Validation.validate_url_query(request.args)

        parser = entity_parser.parse_args()
        code = Pagination.pagination(
            GetByCode.get_entities_by_menu_item(code_=item, validation=validation),
            validation=validation)
        if validation['count']:
            # Todo: very static, make it dynamic
            return jsonify(code[1][0]['entities'])
        if parser['download']:
            return Response(json.dumps(marshal(code, GeoJson.geojson_template(parser['show']))),
                            mimetype='application/json',
                            headers={
                                'Content-Disposition': 'attachment;filename=' + str(
                                    item) + '.json'})
        return marshal(code, GeoJson.geojson_template(parser['show'])), 200

    @staticmethod
    def get_entities_by_menu_item(code_: str, validation: Dict[str, Any]) -> List[Entity]:
        entities = []
        if code_ not in ['actor', 'event', 'place', 'reference', 'source', 'object']:
            raise APIError('Invalid code: ' + code_, status_code=404, payload="404c")
        for entity in Query.get_by_menu_item_api(code_, validation):
            entities.append(entity)
        return entities
