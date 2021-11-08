import json
import operator
from typing import Any, Dict, List, Tuple, Union

from flask import Response, jsonify, request, url_for
from flask_restful import marshal

from openatlas import app
from openatlas.api.v03.export.csv_export import ApiExportCSV
from openatlas.api.v03.resources.error import NoEntityAvailable, TypeIDError
from openatlas.api.v03.resources.formats.rdf import rdf_output
from openatlas.api.v03.resources.pagination import Pagination
from openatlas.api.v03.resources.search.search import search
from openatlas.api.v03.resources.util import parser_str_to_dict
from openatlas.api.v03.resources.search.search_validation import iterate_parameters_for_validation
from openatlas.api.v03.templates.geojson import GeojsonTemplate
from openatlas.api.v03.templates.linked_places import LinkedPlacesTemplate
from openatlas.api.v03.templates.nodes import NodeTemplate
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
    if parser['type_id']:
        entities = Pagination.get_entities_by_type(entities, parser)
        if not entities:
            raise TypeIDError
    if parser['search']:
        search_parser = parser_str_to_dict(parser['search'])
        iterate_parameters_for_validation(search_parser)
        entities = search(entities, search_parser)
        if not entities:
            raise NoEntityAvailable
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
            key=operator.attrgetter(parser['column']),
            reverse=True if parser['sort'] == 'desc' else False)
