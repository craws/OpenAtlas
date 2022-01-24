import json
import operator
from typing import Any, Union

from flask import Response, jsonify, request
from flask_restful import marshal

from openatlas import app
from openatlas.api.csv_export import csv_export, export_entities
from openatlas.api.v03.resources.error import NoEntityAvailable, TypeIDError
from openatlas.api.v03.resources.formats.geojson import get_geojson
from openatlas.api.v03.resources.formats.linked_places import get_entity
from openatlas.api.v03.resources.formats.rdf import rdf_output
from openatlas.api.v03.resources.formats.xml import subunit_xml
from openatlas.api.v03.resources.pagination import get_entities_by_type, \
    pagination
from openatlas.api.v03.resources.search import search
from openatlas.api.v03.resources.search_validation import \
    iterate_validation
from openatlas.api.v03.resources.templates import geojson_collection_template, \
    geojson_pagination, linked_place_pagination, \
    linked_places_template, subunit_template
from openatlas.api.v03.resources.util import get_all_links, \
    get_all_links_inverse, parser_str_to_dict
from openatlas.models.entity import Entity


def get_entity_template(parser: dict[str, Any]) -> dict[str, Any]:
    if parser['format'] == 'geojson':
        return geojson_collection_template()
    return linked_places_template(parser['show'])


def get_entities_template(parser: dict[str, str]) -> dict[str, Any]:
    if parser['format'] == 'geojson':
        return geojson_pagination()
    return linked_place_pagination(parser)


def resolve_entity(
        entity: Entity,
        parser: dict[str, Any]) \
        -> Union[Response, dict[str, Any], tuple[Any, int]]:
    if parser['export'] == 'csv':
        return csv_export(entity)
    result = get_format_entity(entity, parser)
    if parser['format'] in app.config['RDF_FORMATS']:
        return Response(
            rdf_output(result, parser),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    if parser['download']:
        return download(result, get_entity_template(parser), entity.id)
    return marshal(result, get_entity_template(parser)), 200


def resolve_entities(
        entities: list[Entity],
        parser: dict[str, Any],
        file_name: Union[int, str]) \
        -> Union[Response, dict[str, Any], tuple[Any, int]]:
    if parser['export'] == 'csv':
        return export_entities(entities, file_name)
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
        result: dict[str, Any],
        parser: dict[str, Any],
        file_name: Union[int, str]) \
        -> Union[Response, dict[str, Any], tuple[Any, int]]:
    if parser['format'] in app.config['RDF_FORMATS']:
        return Response(
            rdf_output(result['results'], parser),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    if parser['count']:
        return jsonify(result['pagination']['entities'])
    if parser['download']:
        return download(result, get_entities_template(parser), file_name)
    return marshal(result, get_entities_template(parser)), 200


def resolve_subunit(
        subunit: list[dict[str, Any]],
        parser: dict[str, Any],
        name: str) -> Union[Response, dict[str, Any], tuple[Any, int]]:
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
        return download(out, subunit_template(name), name)
    return marshal(out, subunit_template(name)), 200


def download(
        data: Union[list[Any], dict[Any, Any]],
        template: dict[Any, Any],
        name: Union[str, int]) -> Response:
    return Response(
        json.dumps(marshal(data, template)),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename={name}.json'})


def remove_duplicate_entities(entities: list[Entity]) -> list[Entity]:
    seen = set()  # type: ignore
    seen_add = seen.add  # Do not change, faster than always call seen.add(e.id)
    return [
        entity for entity in entities
        if not (entity.id in seen or seen_add(entity.id))]


def sorting(entities: list[Entity], parser: dict[str, Any]) -> list[Entity]:
    entities = remove_duplicate_entities(entities)
    return entities if 'latest' in request.path else \
        sorted(
            entities,
            key=operator.attrgetter(parser['column']),
            reverse=bool(parser['sort'] == 'desc'))


def get_format_entity(
        entity: Entity,
        parser: dict[str, Any]) \
        -> Union[list[dict[str, Any]], dict[str, Any]]:
    if parser['format'] == 'geojson':
        return get_geojson([entity])
    return get_entity(
        entity,
        get_all_links(entity.id),
        get_all_links_inverse(entity.id),
        parser)
