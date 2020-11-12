from typing import Any, Tuple

from flask import jsonify, request
from flask_restful import Resource, marshal

from openatlas.api.v01.parameter import Validation
from openatlas.api.v02.common.class_ import GetByClass
from openatlas.api.v02.common.code import GetByCode
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.parser import query_parser
from openatlas.api.v02.templates.geojson import GeoJson


class GetQuery(Resource):
    def get(self, ) -> Tuple[Any, int]:
        validation = Validation.validate_url_query(request.args)

        parser = query_parser.parse_args()
        # Können die SQL Request auch mehrere Classes oder Items verarbeiten?
        codes = GetByCode.get_entities_by_menu_item(code_="", validation=validation)
        class_ = GetByClass.get_entities_by_class(class_code="class_code", validation=validation)
        template = GeoJson.geojson_template(parser['show'])
        return ''
