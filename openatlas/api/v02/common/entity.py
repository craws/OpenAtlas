from typing import Tuple, Union

from flasgger import swag_from
from flask import Response
from flask_cors import cross_origin
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.util.util import api_access


class GetEntity(Resource):  # type: ignore
    @api_access()  # type: ignore
    @cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
    @swag_from("../swagger/entity.yml", endpoint="entity")
    def get(self, id_: int) -> Union[Tuple[Resource, int], Response]:
        print("here")
        parser = entity_parser.parse_args()
        entity = GeoJsonEntity.get_entity(GeoJsonEntity.get_entity_by_id(id_), parser)
        template = GeoJson.geojson_template(parser['show'])
        if parser['download']:
            return Download.download(data=entity, template=template, name=id_)
        return marshal(entity, GeoJson.geojson_template(parser['show'])), 200
