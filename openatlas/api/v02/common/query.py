from typing import Any, Tuple

from flasgger import swag_from
from flask import jsonify
from flask_restful import Resource, marshal

from openatlas.api.v02.common.class_ import GetByClass
from openatlas.api.v02.common.code import GetByCode
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.resources.parser import query_parser
from openatlas.api.v02.templates.geojson import GeoJson


class GetQuery(Resource):
    @swag_from("../swagger/query.yml", endpoint="query")
    def get(self, ) -> Tuple[Resource, int]:
        entities = []
        parser = query_parser.parse_args()
        template = GeoJson.geojson_template(parser['show'])
        if parser['entities']:
            for entity in parser['entities']:
                entities.append(GeoJsonEntity.get_entity_by_id(entity))
        if parser['items']:
            for item in parser['items']:
                entities.extend(GetByCode.get_entities_by_menu_item(code_=item, parser=parser))
        if parser['classes']:
            for class_ in parser['classes']:
                entities.extend(GetByClass.get_entities_by_class(class_code=class_, parser=parser))
        if parser['count']:
            return jsonify(len(entities))
        if parser['download']:
            return Download.download(data=entities, template=template, name='query')

        output = Pagination.pagination(entities=entities, parser=parser)

        return marshal(output, template), 200
