from typing import Any, Final

from flask import Response, request, url_for
from rdflib import Dataset, Graph

from openatlas import app
from openatlas.api.api_v1.context.lod_context import (
    LA_CONTEXT_URL, LA_SEARCH_CONTEXT_DICT, LA_SEARCH_CONTEXT_URL,
    get_linked_art_context, get_lod_context)
from openatlas.api.api_v1.error_handlers import abort_not_acceptable
from openatlas.api.api_v1.formatters.util import entity_uri
from openatlas.models.entity import Entity

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
    if not request.accept_mimetypes:
        return 'application/ld+json'
    if match := request.accept_mimetypes.best_match(
            [*MIME_FORMAT_MAP, 'application/json']):
        return (
            'application/ld+json' if match == 'application/json' else match)
    abort_not_acceptable()


def make_graph_response(
        graph: Graph,
        ext: str | None = None) -> Response:
    mimetype = get_accepted_mimetype(ext)
    rdf_format = MIME_FORMAT_MAP[mimetype]
    response = Response(graph.serialize(format=rdf_format), mimetype=mimetype)
    if ext is None:
        response.vary.add('Accept')
    response.add_etag()
    return response


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


def _add_entity_headers(
        response: Response,
        entity: Entity,
        mimetype: str,
        *,
        ext: str | None,
        ext_endpoint: str | None) -> list[str]:
    links = [f'<{entity_uri(entity)}>; rel="cite-as"']
    if ext_endpoint:
        for alt_ext, alt_mime in EXTENSION_MIME_MAP.items():
            alt_url = url_for(
                ext_endpoint,
                uuid=entity.uuid,
                ext=alt_ext,
                _external=True)
            if ext is None and alt_mime == mimetype:
                response.headers['Content-Location'] = alt_url
            elif alt_mime != mimetype:
                links.append(
                    f'<{alt_url}>; rel="alternate"; type="{alt_mime}"')
    if timestamp := entity.modified or entity.created:
        response.last_modified = timestamp
    return links


def make_lod_response(
        data: dict[str, Any],
        ext: str | None = None,
        *,
        entity: Entity | None = None,
        ext_endpoint: str | None = None) -> Response:
    mimetype = get_accepted_mimetype(ext)
    if mimetype == 'application/ld+json':
        response = Response(app.json.dumps(data), mimetype=mimetype)
    else:
        # Supply local in-memory JSON-LD contexts so rdflib never performs
        # outbound HTTP requests (prevents Host-header SSRF and external I/O).
        parse_data = dict(data)
        if '@context' in parse_data:
            parse_data['@context'] = _resolve_local_context(
                parse_data['@context'])
        graph = Dataset()
        graph.parse(data=app.json.dumps(parse_data), format='json-ld')
        response = Response(
            graph.serialize(format=MIME_FORMAT_MAP[mimetype]),
            mimetype=mimetype)
    if ext is None:
        response.vary.add('Accept')
    links: list[str] = []
    if isinstance(ctx := data.get('@context'), str):
        links.append(
            f'<{ctx}>; rel="http://www.w3.org/ns/json-ld#context"; '
            'type="application/ld+json"')
    if entity is not None:
        links.extend(_add_entity_headers(
            response,
            entity,
            mimetype,
            ext=ext,
            ext_endpoint=ext_endpoint))
    if links:
        response.headers['Link'] = ', '.join(links)
    response.add_etag()
    return response
