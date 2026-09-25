from typing import Any

from flask import Response, request
from rdflib import Graph

from openatlas import app

EXTENSION_MIME_MAP: dict[str, str] = {
    'json': 'application/ld+json',
    'ttl': 'text/turtle',
    'xml': 'application/rdf+xml',
    'nt': 'application/n-triples'}

MIME_FORMAT_MAP: dict[str, str] = {
    'text/turtle': 'turtle',
    'application/rdf+xml': 'xml',
    'application/n-triples': 'nt',
    'application/ld+json': 'json-ld'}


def set_accept_header(extension: str | None = None) -> None:
    if not extension:
        return
    if extension in EXTENSION_MIME_MAP:
        request.environ['HTTP_ACCEPT'] = EXTENSION_MIME_MAP[extension]


def make_graph_response(
        graph: Graph,
        ext: str | None = None) -> Response:
    if ext:
        set_accept_header(ext)
    accepted = request.accept_mimetypes.best_match(app.config['LOD_HEADER'])
    rdf_format = MIME_FORMAT_MAP.get(accepted, 'json-ld')
    mimetype = accepted if accepted in MIME_FORMAT_MAP else 'application/ld+json'
    return Response(graph.serialize(format=rdf_format), mimetype=mimetype)


def make_lod_response(
        data: dict[str, Any],
        ext: str | None = None) -> Response:
    if ext:
        set_accept_header(ext)
    accepted = request.accept_mimetypes.best_match(app.config['LOD_HEADER'])
    json_str = app.json.dumps(data)
    if accepted not in [
        'text/turtle', 'application/rdf+xml', 'application/n-triples']:
        return Response(json_str, mimetype='application/ld+json')

    graph = Graph()
    graph.parse(data=json_str, format='json-ld')
    return make_graph_response(graph)
