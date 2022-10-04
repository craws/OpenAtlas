import json
from typing import Any, Union

from flask import Response, jsonify, url_for
from flask_restful import marshal

from openatlas import app
from openatlas.api.v02.resources.formats.rdf import rdf_output
from openatlas.api.v02.resources.pagination import Pagination
from openatlas.api.v02.templates.geojson import GeojsonTemplate
from openatlas.api.v02.templates.linked_places import LinkedPlacesTemplate
from openatlas.api.v02.templates.nodes import NodeTemplate
from openatlas.api.v03.resources.formats.csv import export_entities_csv
from openatlas.models.entity import Entity


def get_template(parser: dict[str, str]) -> dict[str, Any]:
    if parser['format'] == 'geojson':
        return GeojsonTemplate.pagination()
    return LinkedPlacesTemplate.pagination(parser)


def resolve_entities(
        entities: list[Entity],
        parser: dict[str, Any],
        file_name: Union[int, str]) \
        -> Union[Response, dict[str, Any], tuple[Any, int]]:
    if parser['export'] == 'csv':
        return export_entities_csv(entities, file_name)
    result = Pagination.pagination(entities, parser)
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
        node: dict[str, Any],
        parser: dict[str, Any],
        file_name: Union[int, str]) \
        -> Union[Response, dict[str, Any], tuple[Any, int]]:
    if parser['count']:
        return jsonify(len(node['nodes']))
    if parser['download']:
        return download(node, NodeTemplate.node_template(), file_name)
    return marshal(node, NodeTemplate.node_template()), 200


def get_node_dict(entity: Entity) -> dict[str, Any]:
    return {
        'id': entity.id,
        'label': entity.name,
        'url': url_for('api_02.entity', id_=entity.id, _external=True)}


def download(
        data: Union[list[dict[str, Any]], dict[str, Any], list[Entity]],
        template: dict[str, Any],
        name: Union[str, int]) -> Response:
    return Response(
        json.dumps(marshal(data, template)),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename={name}.json'})
