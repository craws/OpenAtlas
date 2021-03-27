from typing import Any, Dict, List, Tuple, Union

from flask import Response, g, jsonify
from flask_restful import Resource, marshal

from openatlas.api.export.csv_export import ApiExportCSV
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidCodeError
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.sql import Query
from openatlas.api.v02.templates.geojson import GeoJson
from openatlas.models.entity import Entity
from openatlas.util.util import api_access


class GetBySystemClass(Resource):  # type: ignore
    @api_access()  # type: ignore
    # @swag_from("../swagger/system_class.yml", endpoint="system_class")
    def get(self, system_class: str) -> Union[Tuple[Resource, int], Response]:
        parser = entity_parser.parse_args()
        if parser['export'] == 'csv':
            return ApiExportCSV.export_entities(
                GetBySystemClass.get_entities_by_system_class(system_class=system_class,
                                                              parser=parser))
        system_class_ = Pagination.pagination(
            GetBySystemClass.get_entities_by_system_class(system_class=system_class, parser=parser),
            parser=parser)
        template = GeoJson.pagination(parser['show'])
        if parser['count']:
            return jsonify(system_class_['pagination']['entities'])
        if parser['download']:
            return Download.download(data=system_class_, template=template, name=system_class)
        return marshal(system_class_, template), 200

    @staticmethod
    def get_entities_by_system_class(system_class: str, parser: Dict[str, Any]) -> List[Entity]:
        entities = []
        if system_class not in g.classes:
            raise InvalidCodeError  # pragma: no cover
        for entity in Query.get_by_system_class(system_class, parser):
            entities.append(entity)
        return entities
