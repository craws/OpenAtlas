from typing import Any, Dict, List, Tuple, Union

from flask import Response, jsonify
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidLimitError
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.models.entity import Entity
from openatlas.util.util import api_access


class GetLatest(Resource):  # type: ignore
    @api_access()  # type: ignore
    # @swag_from("../swagger/latest.yml", endpoint="latest")
    def get(self, latest: int) -> Union[Tuple[Resource, int], Response]:
        parser = entity_parser.parse_args()
        entities = {"result": GetLatest.get_entities_get_latest(latest, parser)}
        template = GeoJson.pagination(parser['show'])
        if parser['count']:
            return jsonify(len(entities))
        if parser['download']:
            return Download.download(data=entities, template=template, name=latest)
        return marshal(entities, template), 200

    @staticmethod
    def get_entities_get_latest(limit_: int, parser: Dict[str, Any]) -> List[Dict[str, Any]]:
        entities = []
        if 0 < limit_ < 101:
            for entity in Entity.get_latest(limit_):
                entities.append(GeoJsonEntity.get_entity(entity, parser))
            return entities
        else:
            raise InvalidLimitError  # pragma: no cover
