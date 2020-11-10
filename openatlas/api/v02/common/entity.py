from flask import request
from flask_restful import Resource, marshal

import openatlas.api.v02.templates.geojson as template
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v01.parameter import Validation
from openatlas.api.v02.resources.parser import entity_parser


class GetEntity(Resource):
    def get(self, id_):
        args = entity_parser.parse_args()
        validation = Validation.validate_url_query(request.args)
        entity = GeoJsonEntity.get_entity(GeoJsonEntity.get_entity_by_id(id_), validation)
        print(entity)
        return marshal(entity, template.entity_json), 200
