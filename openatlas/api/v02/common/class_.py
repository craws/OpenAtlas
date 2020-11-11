import json
from typing import Any, Dict, List

from flask import Response, g, jsonify, request
from flask_restful import Resource, marshal

from openatlas.api.v01.error import APIError
from openatlas.api.v01.parameter import Validation
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.sql import Query
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.models.entity import Entity


class GetByClass(Resource):
    def get(self, class_code):
        validation = Validation.validate_url_query(request.args)

        parser = entity_parser.parse_args()
        class_ = Pagination.pagination(
            GetByClass.get_entities_by_class(class_code=class_code, validation=validation),
            validation=validation)
        if validation['count']:
            # Todo: very static, make it dynamic
            return jsonify(class_[1][0]['entities'])
        if parser['download']:
            return Response(json.dumps(marshal(class_, GeoJson.geojson_template(parser['show']))),
                            mimetype='application/json',
                            headers={
                                'Content-Disposition': 'attachment;filename=' + str(
                                    class_code) + '.json'})
        return marshal(class_, GeoJson.geojson_template(parser['show'])), 200

    @staticmethod
    def get_entities_by_class(class_code: str, validation: Dict[str, Any]) -> List[Entity]:
        entities = []
        if class_code not in g.classes:
            raise APIError('Invalid CIDOC CRM class code: ' + class_code, status_code=404,
                           payload="404d")
        for entity in Query.get_by_class_code_api(class_code, validation):
            entities.append(entity)
        return entities
