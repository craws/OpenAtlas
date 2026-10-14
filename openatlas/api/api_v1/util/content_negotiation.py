from typing import Any, Final

from flask import Response, request
from rdflib import Dataset, Graph

from openatlas import app

EXTENSION_MIME_MAP: Final[dict[str, str]] = {
    'json': 'application/ld+json',
    'ttl': 'text/turtle',
    'xml': 'application/rdf+xml',
    'nt': 'application/n-triples'}

MIME_FORMAT_MAP: Final[dict[str, str]] = {
    'application/ld+json': 'json-ld',
    'text/turtle': 'turtle',
    'application/rdf+xml': 'xml',
    'application/n-triples': 'nt'}


def get_accepted_mimetype(ext: str | None = None) -> str:
    if ext and ext in EXTENSION_MIME_MAP:
        return EXTENSION_MIME_MAP[ext]
    return request.accept_mimetypes.best_match(
        MIME_FORMAT_MAP.keys(),
        default='application/ld+json')


def make_graph_response(
        graph: Graph,
        ext: str | None = None) -> Response:
    mimetype = get_accepted_mimetype(ext)
    rdf_format = MIME_FORMAT_MAP[mimetype]
    return Response(graph.serialize(format=rdf_format), mimetype=mimetype)


def make_lod_response(
        data: dict[str, Any],
        ext: str | None = None) -> Response:
    mimetype = get_accepted_mimetype(ext)
    json_str = app.json.dumps(data)
    if mimetype == 'application/ld+json':
        return Response(json_str, mimetype=mimetype)

    graph = Dataset()
    graph.parse(data=json_str, format='json-ld')
    return Response(
        graph.serialize(format=MIME_FORMAT_MAP[mimetype]),
        mimetype=mimetype)
