import json
import operator
from typing import Any, Dict, List, MutableSet, Tuple, Union

from flask import Response, jsonify, request, url_for
from flask_restful import marshal

from openatlas import app
from openatlas.api.v03.export.csv_export import ApiExportCSV
from openatlas.api.v03.resources.error import NoEntityAvailable, TypeIDError
from openatlas.api.v03.resources.formats.rdf import rdf_output
from openatlas.api.v03.resources.formats.xml import subunit_xml
from openatlas.api.v03.resources.pagination import get_entities_by_type, \
    pagination
from openatlas.api.v03.resources.search.search import search
from openatlas.api.v03.resources.search.search_validation import \
    iterate_validation
from openatlas.api.v03.resources.util import parser_str_to_dict
from openatlas.api.v03.templates.geojson import GeojsonTemplate
from openatlas.api.v03.templates.linked_places import LinkedPlacesTemplate
from openatlas.api.v03.templates.nodes import NodeTemplate
from openatlas.api.v03.templates.subunits import SubunitTemplate
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
        entities = get_entities_by_type(entities, parser)
        if not entities:
            raise TypeIDError
    if parser['search']:
        search_parser = parser_str_to_dict(parser['search'])
        if iterate_validation(search_parser):
            entities = search(entities, search_parser)
    if not entities:
        raise NoEntityAvailable
    return resolve_output(
        pagination(sorting(entities, parser), parser),
        parser,
        file_name)


def resolve_output(
        result: Dict[str, Any],
        parser: Dict[str, Any],
        file_name: Union[int, str]) \
        -> Union[Response, Dict[str, Any], Tuple[Any, int]]:
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


def resolve_subunit(
        subunit: List[Dict[str, Any]],
        parser: Dict[str, Any],
        name: Union[int, str]) \
        -> Union[Response, Dict[str, Any], Tuple[Any, int]]:
    out = {'collection' if parser['format'] == 'xml' else name: subunit}
    if parser['count']:
        return jsonify(len(out[name]))
    if parser['format'] == 'xml':
        if parser['download']:
            return Response(
                subunit_xml(out),
                mimetype='application/xml',
                headers={
                    'Content-Disposition': f'attachment;filename={name}.xml'})
        return Response(
            subunit_xml(out),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    if parser['download']:
        return download(out, SubunitTemplate.subunit_template(name),
                        name)
    return marshal(out, SubunitTemplate.subunit_template(name)), 200


def get_node_dict(entity: Entity) -> Dict[str, Any]:
    return {
        'id': entity.id,
        'label': entity.name,
        'url': url_for('api_03.entity', id_=entity.id, _external=True)}


def download(
        data: Union[List[Any], Dict[Any, Any]],
        template: Dict[Any, Any],
        name: Union[str, int]) -> Response:
    return Response(
        json.dumps(marshal(data, template)),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename={name}.json'})


def remove_duplicate_entities(entities: List[Entity]) -> List[Entity]:
    seen: MutableSet = set()
    seen_add = seen.add  # Do not change, faster than always call seen.add(e.id)
    return [entity for entity in entities if
            not (entity.id in seen or seen_add(entity.id))]


def sorting(entities: List[Entity], parser: Dict[str, Any]) -> List[Entity]:
    entities = remove_duplicate_entities(entities)
    return entities if 'latest' in request.path else \
        sorted(
            entities,
            key=operator.attrgetter(parser['column']),
            reverse=bool(parser['sort'] == 'desc'))
