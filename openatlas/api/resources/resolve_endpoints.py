import itertools
import json
from typing import Any, Union

from flask import Response, jsonify, request
from flask_restful import marshal

from openatlas import app
from openatlas.api.formats.csv import (
    export_csv_for_network_analysis, export_entities_csv)
from openatlas.api.formats.geojson import get_geojson, get_geojson_v2
from openatlas.api.formats.linked_places import get_linked_places_entity
from openatlas.api.formats.rdf import rdf_output
from openatlas.api.formats.xml import subunit_xml
from openatlas.api.resources.error import (
    EntityDoesNotExistError, LastEntityError, NoEntityAvailable, TypeIDError)
from openatlas.api.resources.model_mapper import (
    get_all_links_of_entities, get_all_links_of_entities_inverse)
from openatlas.api.resources.search import search
from openatlas.api.resources.search_validation import (
    iterate_validation)
from openatlas.api.resources.templates import (
    geojson_collection_template, geojson_pagination, linked_place_pagination,
    linked_places_template, subunit_template)
from openatlas.api.resources.util import (
    get_entities_by_type, get_key, link_parser_check,
    link_parser_check_inverse, parser_str_to_dict, remove_duplicate_entities)
from openatlas.models.entity import Entity


def resolve_entities(
        entities: list[Entity],
        parser: dict[str, Any],
        file_name: Union[int, str]) \
        -> Union[Response, dict[str, Any], tuple[Any, int]]:
    if parser['type_id'] and not (
            entities := get_entities_by_type(entities, parser)
    ):  # pylint: disable=superfluous-parens
        # check disabled because of pylint bug, fixed in pylint 2.10.0
        raise TypeIDError
    if parser['search']:
        search_parser = parser_str_to_dict(parser['search'])
        if iterate_validation(search_parser):
            entities = search(entities, search_parser)
    if parser['export'] == 'csv':
        return export_entities_csv(entities, file_name)
    if parser['export'] == 'csvNetwork':
        return export_csv_for_network_analysis(entities, parser)
    if not entities:
        raise NoEntityAvailable
    result = get_json_output(
        sorting(
            remove_duplicate_entities(entities),
            parser),
        parser)
    if parser['format'] in app.config['RDF_FORMATS']:
        return Response(
            rdf_output(result['results'], parser),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    if parser['count'] == 'true':
        return jsonify(result['pagination']['entities'])
    if parser['download'] == 'true':
        return download(result, get_entities_template(parser), file_name)
    return marshal(result, get_entities_template(parser)), 200


def get_entities_template(parser: dict[str, str]) -> dict[str, Any]:
    if parser['format'] in ['geojson', 'geojson-v2']:
        return geojson_pagination()
    return linked_place_pagination(parser)


def sorting(entities: list[Entity], parser: dict[str, Any]) -> list[Entity]:
    if 'latest' in request.path:
        return entities
    return sorted(
        entities,
        key=lambda entity: get_key(entity, parser),
        reverse=bool(parser['sort'] == 'desc'))


def get_entity_formatted(
        entity: Entity,
        parser: dict[str, Any]) -> dict[str, Any]:
    if parser['format'] == 'geojson':
        return get_geojson([entity], parser)
    if parser['format'] == 'geojson-v2':
        return get_geojson_v2([entity], parser)
    return get_linked_places_entity(
        entity,
        get_all_links_of_entities(entity.id),
        get_all_links_of_entities_inverse(entity.id),
        parser)


def resolve_entity(
        entity: Entity,
        parser: dict[str, Any]) \
        -> Union[Response, dict[str, Any], tuple[Any, int]]:
    if parser['export'] == 'csv':
        export_entities_csv(entity, entity.name)
    if parser['export'] == 'csvNetwork':
        export_csv_for_network_analysis([entity], parser)
    result = get_entity_formatted(entity, parser)
    if parser['format'] in app.config['RDF_FORMATS']:
        return Response(
            rdf_output(result, parser),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    template = geojson_collection_template() \
        if parser['format'] in ['geojson', 'geojson-v2'] \
        else linked_places_template(parser['show'])
    if parser['download']:
        download(result, template, entity.id)
    return marshal(result, template), 200


def resolve_subunits(
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
        download(out, subunit_template(name), name)
    return marshal(out, subunit_template(name)), 200


def get_json_output(
        entities: list[Entity],
        parser: dict[str, Any]) -> dict[str, Any]:
    total = [e.id for e in entities]
    count = len(total)
    parser['limit'] = count if parser['limit'] == 0 else parser['limit']
    e_list = list(itertools.islice(total, 0, None, int(parser['limit'])))
    index = [{'page': num + 1, 'startId': i} for num, i in enumerate(e_list)]
    parser['first'] = get_by_page(index, parser) \
        if parser['page'] else parser['first']
    total = get_start_entity(total, parser) \
        if parser['last'] or parser['first'] else total
    j = [i for i, x in enumerate(entities) if x.id == total[0]]
    new_entities = [e for idx, e in enumerate(entities[j[0]:])]
    return {
        "results": get_entities_formatted(new_entities, parser),
        "pagination": {
            'entitiesPerPage': int(parser['limit']),
            'entities': count,
            'index': index,
            'totalPages': len(index)}}


def get_entities_formatted(
        entities_all: list[Entity],
        parser: dict[str, Any]) -> list[dict[str, Any]]:
    entities = entities_all[:int(parser['limit'])]
    if parser['format'] == 'geojson':
        return [get_geojson(entities, parser)]
    if parser['format'] == 'geojson-v2':
        return [get_geojson_v2(entities, parser)]
    entities_dict: dict[str, Any] = {}
    for entity in entities:
        entities_dict[entity.id] = {
            'entity': entity,
            'links': [],
            'links_inverse': []}
    for link_ in link_parser_check(entities, parser):
        entities_dict[link_.domain.id]['links'].append(link_)
    for link_ in link_parser_check_inverse(entities, parser):
        entities_dict[link_.range.id]['links_inverse'].append(link_)
    result = []
    for item in entities_dict.values():
        result.append(
            get_linked_places_entity(
                item['entity'],
                item['links'],
                item['links_inverse'],
                parser))
    return result


def get_start_entity(total: list[int], parser: dict[str, Any]) -> list[Any]:
    if parser['first'] and int(parser['first']) in total:
        return list(itertools.islice(
            total,
            total.index(int(parser['first'])),
            None))
    if parser['last'] and int(parser['last']) in total:
        if not (out := list(itertools.islice(
                total,
                total.index(int(parser['last'])) + 1,
                None))):
            raise LastEntityError
        return out
    raise EntityDoesNotExistError


def get_by_page(
        index: list[dict[str, Any]],
        parser: dict[str, Any]) -> dict[str, Any]:
    page = parser['page'] \
        if parser['page'] < index[-1]['page'] else index[-1]['page']
    return [entry['startId'] for entry in index if entry['page'] == page][0]


def download(
        data: Union[list[Any], dict[Any, Any]],
        template: dict[Any, Any],
        name: Union[str, int]) -> Response:
    return Response(
        json.dumps(marshal(data, template)),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename={name}.json'})
