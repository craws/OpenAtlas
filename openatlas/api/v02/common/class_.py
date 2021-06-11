from typing import Any, Dict, List, Tuple, Union

from flask import Response, g, jsonify
from flask_restful import Resource, marshal

from openatlas.api.export.csv_export import ApiExportCSV
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.error import InvalidCidocClassCode
from openatlas.api.v02.resources.geojson import Geojson
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.util import get_all_links
from openatlas.api.v02.templates.geojson import GeojsonTemplate
from openatlas.api.v02.templates.linked_places import LinkedPlacesTemplate
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetByClass(Resource):  # type: ignore
    @staticmethod
    def get(class_code: str) -> Union[Tuple[Resource, int], Response]:
        parser = entity_parser.parse_args()
        if parser['format'] == 'geojson':
            class_ = GetByClass.get_geojson(GetByClass.get_entities_by_class(class_code=class_code, parser=parser))
            template = GeojsonTemplate.geojson_template()
            return marshal(class_, template), 200
        if parser['export'] == 'csv':
            return ApiExportCSV.export_entities(
                GetByClass.get_entities_by_class(class_code=class_code, parser=parser), class_code)
        class_ = Pagination.pagination(
            GetByClass.get_entities_by_class(class_code=class_code, parser=parser),
            parser=parser)
        if parser['count']:
            return jsonify(class_['pagination']['entities'])
        template = LinkedPlacesTemplate.pagination(parser['show'])
        if parser['download']:
            return Download.download(data=class_, template=template, name=class_code)
        return marshal(class_, template), 200

    @staticmethod
    def get_entities_by_class(class_code: str, parser: Dict[str, Any]) -> List[Entity]:
        if class_code not in g.cidoc_classes:
            raise InvalidCidocClassCode
        return [Entity(row) for row in Db.get_by_class_code(class_code, parser)]

    @staticmethod
    def get_geojson(entities: List[Entity]) -> Dict[str, Any]:
        class_json = [Geojson.check_if_geometry(entity) for entity in entities]
        return Geojson.return_output(class_json)
