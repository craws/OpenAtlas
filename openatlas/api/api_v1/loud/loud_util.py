import functools
import json
import pathlib
from collections import defaultdict
from typing import Any

from flask import Response, g, request
from rdflib import Graph

from openatlas import app
from openatlas.database.api import get_wkts_by_ids
from openatlas.models.entity import Entity, Link


def get_links_for_entities(entities: list[Entity]) -> dict[Any, Any]:
    entities_with_links = {}
    preloaded = {e.id: e for e in entities}
    preloaded.update(g.types)
    preloaded.update(g.reference_systems)

    for entity in entities:
        entities_with_links[entity.id] = {
            'entity': entity,
            'links': [],
            'links_inverse': [],
            'geometries': {}}

    geom_ids = set(e.id for e in entities)
    for link_ in Entity.get_links_of_entities(
            [entity.id for entity in entities],
            preloaded_entities=preloaded):
        entities_with_links[link_.domain.id]['links'].append(link_)
        preloaded[link_.range.id] = link_.range
        if link_.property.code == 'P53':
            geom_ids.add(link_.range.id)

    for link_ in Entity.get_links_of_entities(
            [entity.id for entity in entities],
            inverse=True,
            preloaded_entities=preloaded):
        entities_with_links[link_.range.id]['links_inverse'].append(link_)
        preloaded[link_.domain.id] = link_.domain

    if geom_ids:
        wkts = get_wkts_by_ids(list(geom_ids))
        for id_ in entities_with_links:
            entities_with_links[id_]['geometries'] = wkts

    return entities_with_links

def get_type_references() -> dict[int, list[Link]]:
    if hasattr(g, 'type_references'):
        return g.type_references

    type_links = Entity.get_links_of_entities(
        list(g.types.keys()),
        'P67',
        inverse=True,
        preloaded_entities=g.types)

    out: dict[int, list[Link]] = defaultdict(list)
    for link_ in type_links:
        if link_.domain.class_.name in \
                ['external_reference', 'reference_system']:
            out[link_.range.id].append(link_)

    g.type_references = out
    return out


@functools.lru_cache
def get_loud_context() -> dict[str, Any]:
    file_path = pathlib.Path(app.root_path) / 'api' / 'linked-art.json'

    with file_path.open('r', encoding='utf-8') as f:
        return json.load(f)


@functools.lru_cache
def parse_loud_context() -> dict[str, str]:
    context = get_loud_context().get('@context', {})
    inverted: dict[str, str] = {}
    for term, definition in context.items():
        if not isinstance(definition, dict):
            continue
        inverted[definition['@id']] = term
        for nested_term, nested_def in definition.get('@context', {}).items():
            if isinstance(nested_def, dict):
                inverted[nested_def['@id']] = nested_term
    return inverted


def set_accept_header(extension: str | None = None) -> None:
    if not extension:
        return
    ext_map = {
        'json': 'application/ld+json',
        'ttl': 'text/turtle',
        'xml': 'application/rdf+xml',
        'nt': 'application/n-triples'}
    if extension in ext_map:
        request.environ['HTTP_ACCEPT'] = ext_map[extension]


def make_lod_response(data: dict[str, Any]) -> Response:
    accepted = request.accept_mimetypes.best_match(app.config['LOD_HEADER'])
    json_str = app.json.dumps(data)
    if accepted not in [
        'text/turtle', 'application/rdf+xml', 'application/n-triples']:
        return Response(json_str, mimetype='application/ld+json')

    graph = Graph()
    graph.parse(data=json_str, format='json-ld')

    match accepted:
        case 'text/turtle':
            turtle_output = graph.serialize(format='turtle')
            return Response(turtle_output, mimetype='text/turtle')

        case 'application/rdf+xml':
            xml_output = graph.serialize(format='xml')
            return Response(xml_output, mimetype='application/rdf+xml')

        case 'application/n-triples':
            nt_output = graph.serialize(format='nt')
            return Response(nt_output, mimetype='application/n-triples')
