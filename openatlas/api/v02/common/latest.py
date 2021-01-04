from typing import Any, Dict, List, Tuple

from flasgger import swag_from
from flask import jsonify
from flask_cors import cross_origin
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidLimitError
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.models.entity import Entity
from openatlas.util.util import api_access


class GetLatest(Resource): # type: ignore
    @api_access()  # type: ignore
    @cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
    @swag_from("../swagger/latest.yml", endpoint="latest")
    def get(self, latest: int) -> Tuple[Resource, int]:
        parser = entity_parser.parse_args()
        # Todo: Think about to get latest into the pagination
        entities = {"geojson": GetLatest.get_entities_get_latest(latest, parser)}
        template = GeoJson.pagination(parser['show'])
        if parser['count']:
            return jsonify(len(entities))
        if parser['download']:
            return Download.download(data=entities, template=template, name=latest)
        return marshal(entities, template), 200

    @staticmethod
    def get_entities_get_latest(limit_: int, parser: Dict[str, Any]) -> List[Dict[str, Any]]:
        entities = []
        if 1 < limit_ < 101:
            for entity in Entity.get_latest(limit_):
                entities.append(GeoJsonEntity.get_entity(entity, parser))
            return entities
        else:
            raise InvalidLimitError
