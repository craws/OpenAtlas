from typing import Any, Dict, List, Tuple, Union

from flask import Response, g, jsonify
from flask_restful import Resource, marshal

from openatlas.api.export.csv_export import ApiExportCSV
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidCodeError
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.util import get_template
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetByCode(Resource):  # type: ignore
    @staticmethod
    def get(code: str) -> Union[Tuple[Resource, int], Response]:
        parser = entity_parser.parse_args()
        if parser['export'] == 'csv':
            return ApiExportCSV.export_entities(GetByCode.get_by_view(code, parser), code)
        code_ = Pagination.pagination(GetByCode.get_by_view(code, parser), parser)
        if parser['count']:
            return jsonify(code_['pagination']['entities'])
        if parser['download']:
            return Download.download(code_, get_template(parser), code)
        return marshal(code_, get_template(parser)), 200

    @staticmethod
    def get_by_view(code_: str, parser: Dict[str, Any]) -> List[Entity]:
        if code_ not in g.view_class_mapping:
            raise InvalidCodeError
        sys_class = Db.get_by_system_class(g.view_class_mapping[code_], parser)
        return [Entity(row) for row in sys_class]
