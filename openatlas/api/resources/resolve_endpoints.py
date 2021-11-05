import json
import operator
from typing import Any, Dict, List, Tuple, Union

from flask import Response, jsonify, request, url_for
from flask_restful import marshal

from openatlas import app
from openatlas.api.export.csv_export import ApiExportCSV
from openatlas.api.resources.formats.rdf import rdf_output
from openatlas.api.resources.pagination import Pagination
from openatlas.api.templates.geojson import GeojsonTemplate
from openatlas.api.templates.linked_places import LinkedPlacesTemplate
from openatlas.api.templates.nodes import NodeTemplate
from openatlas.models.entity import Entity


def get_template(parser: Dict[str, str]) -> Dict[str, Any]:
    if parser['format'] == 'geojson':
        return GeojsonTemplate.pagination()
    return LinkedPlacesTemplate.pagination(parser)


def resolve_entities(
        entities: List[Entity],
        parser: Dict[str, Any],
        file_name: Union[int, str]) \
        -> Union[Response, Dict[str, Any], Tuple[Any, int]]:
    if parser['export'] == 'csv':
        return ApiExportCSV.export_entities(entities, file_name)
    # Todo: sorting has to be done at very last I think. So maybe make type_id
    #  and search and then give pagination the sorted entities
    result = Pagination.pagination(sorting(entities, parser), parser)
    if parser['format'] in app.config['RDF_FORMATS']:
        return Response(
            rdf_output(result['results'], parser),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    if parser['count']:
        return jsonify(result['pagination']['entities'])
    if parser['download']:
        return download(result, get_template(parser), file_name)
    return marshal(result, get_template(parser)), 200


def resolve_node_parser(
        node: Dict[str, Any],
        parser: Dict[str, Any],
        file_name: Union[int, str]) \
        -> Union[Response, Dict[str, Any], Tuple[Any, int]]:
    if parser['count']:
        return jsonify(len(node['nodes']))
    if parser['download']:
        return download(node, NodeTemplate.node_template(), file_name)
    return marshal(node, NodeTemplate.node_template()), 200


def get_node_dict(entity: Entity) -> Dict[str, Any]:
    return {
        'id': entity.id,
        'label': entity.name,
        'url': url_for('api.entity', id_=entity.id, _external=True)}


def download(
        data: Union[List[Dict[str, Any]], Dict[str, Any], List[Entity]],
        template: Dict[str, Any],
        name: Union[str, int]) -> Response:
    return Response(
        json.dumps(marshal(data, template)),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename={name}.json'})


def sorting(entities: List[Entity], parser: Dict[str, Any]) -> List[Entity]:
    return entities if 'latest' in request.path else \
        sorted(
            entities,
            key=operator.attrgetter(parser['sort_column']),
            reverse=True if parser['sort_results'] == 'desc' else False)
