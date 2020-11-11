import json

from flask import Response, request
from flask_restful import Resource, marshal

from openatlas.api.v01.parameter import Validation
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.templates.geojson import GeoJson


class GetEntity(Resource):
    def get(self, id_):
        validation = Validation.validate_url_query(request.args)

        parser = entity_parser.parse_args()
        entity = GeoJsonEntity.get_entity(GeoJsonEntity.get_entity_by_id(id_), validation)
        if parser['download']:
            return Response(json.dumps(marshal(entity, GeoJson.geojson_template(parser['show']))),
                            mimetype='application/json',
                            headers={
                                'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})
        return marshal(entity, GeoJson.geojson_template(parser['show'])), 200
