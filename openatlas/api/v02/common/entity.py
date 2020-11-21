from typing import Any, Tuple

from flasgger import swag_from
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.templates.geojson import GeoJson


class GetEntity(Resource):
    @swag_from("entity.yml")
    def get(self, id_: int) -> Tuple[Any, int]:
        parser = entity_parser.parse_args()
        entity = GeoJsonEntity.get_entity(GeoJsonEntity.get_entity_by_id(id_), parser)
        template = GeoJson.geojson_template(parser['show'])
        if parser['download']:
            return Download.download(data=entity, template=template, name=id_)
        return marshal(entity, GeoJson.geojson_template(parser['show'])), 200
