import json

from flask import Response, jsonify, request
from flask_restful import Resource, marshal
from typing import Any, Dict, List

from openatlas.api.v01.error import APIError
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v01.parameter import Validation
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.models.entity import Entity


class GetLatest(Resource):
    def get(self, latest: int):
        validation = Validation.validate_url_query(request.args)

        parser = entity_parser.parse_args()
        # Todo: Think about to get latest into the pagination
        entities = GetLatest.get_entities_get_latest(latest, validation)
        if validation['count']:
            # Todo: very static, make it dynamic
            return jsonify(len(entities))
        if parser['download']:
            return Response(json.dumps(marshal(entities, GeoJson.geojson_template(parser['show']))),
                            mimetype='application/json',
                            headers={
                                'Content-Disposition': 'attachment;filename=latest_' + str(
                                    latest) + '.json'})
        return marshal(entities, GeoJson.geojson_template(parser['show'])), 200

    @staticmethod
    def get_entities_get_latest(limit_: int, validation: Dict[str, Any]) -> List[Dict[str, Any]]:
        entities = []
        try:
            limit_ = int(limit_)
        except Exception:
            raise APIError('Invalid limit.', status_code=404, payload="404e")
        if 1 < limit_ < 101:
            for entity in Entity.get_latest(limit_):
                entities.append(GeoJsonEntity.get_entity(entity, meta=validation))
            return entities
        else:
            raise APIError('Invalid limit.', status_code=404, payload="404e")
