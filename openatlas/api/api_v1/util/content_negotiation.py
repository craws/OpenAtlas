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

    # For RDF graph serialization (Turtle, RDF/XML, N-Triples):
    # If the context is OpenAtlas native LOD (local or remote context URL),
    # supply the in-memory context dictionary so rdflib does not need to perform
    # an HTTP network request to local.host or openatlas.eu.
    parse_data = dict(data)
    ctx = parse_data.get('@context')
    if ctx and 'linked.art' not in str(ctx):
        from openatlas.api.api_v1.context.lod_context import get_lod_context
        parse_data['@context'] = get_lod_context()['@context']
        json_str = app.json.dumps(parse_data)

    graph = Dataset()
    graph.parse(data=json_str, format='json-ld')
    return Response(
        graph.serialize(format=MIME_FORMAT_MAP[mimetype]),
        mimetype=mimetype)
