from typing import Any, Dict, List, Tuple, Union

from flask import Response, jsonify
from flask_restful import marshal
from flask_restful.fields import Nested

from openatlas.api.export.csv_export import ApiExportCSV
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.templates.geojson import GeojsonTemplate
from openatlas.api.v02.templates.linked_places import LinkedPlacesTemplate
from openatlas.models.entity import Entity


def get_template(parser: Dict[str, str]) -> Dict[str, Union[List, Nested]]:
    if parser['format'] == 'lp':
        return LinkedPlacesTemplate.pagination(parser['show'])
    if parser['format'] == 'geojson':
        return GeojsonTemplate.pagination()


def resolve_entity_parser(entities: Union[List[Entity], Entity], parser: Dict[str, Any],
                          file_name) -> Union[Response, Dict[str, Any], Tuple[Any, int]]:
    if parser['export'] == 'csv':
        return ApiExportCSV.export_entities(entities, file_name)
    result = Pagination.pagination(entities, parser)
    if parser['count']:
        print(result['pagination']['entities'])
        return jsonify(result['pagination']['entities'])
    if parser['download']:
        return Download.download(result, get_template(parser), file_name)
    return marshal(result, get_template(parser)), 200
