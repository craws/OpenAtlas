from typing import Any, Dict, List, Tuple, Union
from openatlas.api.v02.resources.util import get_template

from flasgger import swag_from
from flask import Response, g, jsonify
from flask_restful import Resource, marshal

from openatlas.api.export.csv_export import ApiExportCSV
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidCidocClassCode
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetByClass(Resource):  # type: ignore
    @swag_from("../swagger/class.yml", endpoint="class")
    def get(self, class_code: str) -> Union[Tuple[Resource, int], Response]:
        parser = entity_parser.parse_args()
        if parser['export'] == 'csv':
            return ApiExportCSV.export_entities(
                GetByClass.get_by_class(class_code, parser), class_code)
        class_ = Pagination.pagination(GetByClass.get_by_class(class_code, parser), parser)
        if parser['count']:
            return jsonify(class_['pagination']['entities'])
        if parser['download']:
            return Download.download(class_, get_template(parser), class_code)
        return marshal(class_, get_template(parser)), 200

    @staticmethod
    def get_by_class(class_code: str, parser: Dict[str, Any]) -> List[Entity]:
        if class_code not in g.cidoc_classes:
            raise InvalidCidocClassCode
        return [Entity(row) for row in Db.get_by_class_code(class_code, parser)]
