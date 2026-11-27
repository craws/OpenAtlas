from typing import Any, Final

from flask import Response, request
from rdflib import Dataset, Graph

from openatlas import app
from openatlas.api.api_v1.context.lod_context import (
    LA_CONTEXT_URL, LA_SEARCH_CONTEXT_DICT, LA_SEARCH_CONTEXT_URL,
    get_linked_art_context, get_lod_context)

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


def _resolve_local_context(ctx: Any) -> Any:
    if ctx == LA_CONTEXT_URL:
        return get_linked_art_context()
    if isinstance(ctx, list) and LA_CONTEXT_URL in ctx:
        resolved: list[Any] = []
        for item in ctx:
            if item == LA_CONTEXT_URL:
                resolved.append(get_linked_art_context())
            elif item == LA_SEARCH_CONTEXT_URL:
                resolved.append(LA_SEARCH_CONTEXT_DICT)
            elif isinstance(item, dict):
                resolved.append(item)
        return resolved
    if isinstance(ctx, dict):
        return ctx
    return get_lod_context()['@context']


def make_lod_response(
        data: dict[str, Any],
        ext: str | None = None) -> Response:
    mimetype = get_accepted_mimetype(ext)
    if mimetype == 'application/ld+json':
        return Response(app.json.dumps(data), mimetype=mimetype)

    # Supply local in-memory JSON-LD contexts so rdflib never performs
    # outbound HTTP requests (prevents Host-header SSRF and external I/O).
    parse_data = dict(data)
    if '@context' in parse_data:
        parse_data['@context'] = _resolve_local_context(
            parse_data['@context'])
    json_str = app.json.dumps(parse_data)

    graph = Dataset()
    graph.parse(data=json_str, format='json-ld')
    return Response(
        graph.serialize(format=MIME_FORMAT_MAP[mimetype]),
        mimetype=mimetype)
