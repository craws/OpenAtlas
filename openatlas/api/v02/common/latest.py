from typing import Any, Dict, List, Tuple

from flasgger import swag_from
from flask import jsonify
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.error import Error
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.models.entity import Entity


class GetLatest(Resource):
    @swag_from("latest.yml")
    def get(self, latest: int) -> Tuple[Any, int]:
        parser = entity_parser.parse_args()
        # Todo: Think about to get latest into the pagination
        entities = GetLatest.get_entities_get_latest(latest, parser)
        template = GeoJson.geojson_template(parser['show'])
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
                entities.append(GeoJsonEntity.get_entity(entity, parser=parser))
            return entities
        else:
            # Todo: Eliminate Error
            raise Error('Invalid limit.', status_code=404, payload="404e")
