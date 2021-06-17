from typing import Any, Dict, List, Tuple, Union

from flask import Response, jsonify, url_for
from flask_restful import marshal
from flask_restful.fields import Nested

from openatlas.api.export.csv_export import ApiExportCSV
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.templates.geojson import GeojsonTemplate
from openatlas.api.v02.templates.linked_places import LinkedPlacesTemplate
from openatlas.api.v02.templates.nodes import NodeTemplate
from openatlas.models.entity import Entity


def get_template(parser: Dict[str, str]) -> Dict[str, Any]:
    if parser['format'] == 'geojson':
        return GeojsonTemplate.pagination()
    return LinkedPlacesTemplate.pagination(parser)


def resolve_entity(
        entities: List[Entity],
        parser: Dict[str, Any],
        file_name: Union[int, str]) -> Union[Response, Dict[str, Any], Tuple[Any, int]]:
    if parser['export'] == 'csv':
        return ApiExportCSV.export_entities(entities, file_name)
    result = Pagination.pagination(entities, parser)
    if parser['count']:
        return jsonify(result['pagination']['entities'])
    if parser['download']:
        return Download.download(result, get_template(parser), file_name)
    return marshal(result, get_template(parser)), 200


def resolve_node_parser(
        node: Dict[str, Any],
        parser: Dict[str, Any],
        file_name: Union[int, str]) -> Union[Response, Dict[str, Any], Tuple[Any, int]]:
    if parser['count']:
        return jsonify(len(node['nodes']))
    if parser['download']:
        return Download.download(node, NodeTemplate.node_template(), file_name)
    return marshal(node, NodeTemplate.node_template()), 200


def get_node_dict(entity: Entity) -> Dict[str, Any]:
    return {'id': entity.id,
            'label': entity.name,
            'url': url_for('api.entity', id_=entity.id, _external=True)}
