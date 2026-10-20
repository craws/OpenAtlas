from typing import Any

from flask import Response, stream_with_context
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.formatters.la_export import stream_la_dump
from openatlas.api.api_v1.formatters.la_formatter import (
    format_la_entities, format_la_entity)
from openatlas.api.api_v1.formatters.lod_util import (
    get_entities_response, get_entity_response)
from openatlas.api.api_v1.models.lod import (
    EntityCollectionPath, EntityCollectionQuery, EntityPath, EntityPathExt,
    LaDumpQuery)
from openatlas.api.api_v1.openapi_tags import lod_tag
from openatlas.api.api_v1.responses.lod import (
    la_dump_responses, lod_collection_responses, lod_responses)
from openatlas.api.api_v1.util.auth import require_auth

api_v1_la = APIBlueprint(
    'api_v1_la',
    __name__,
    url_prefix='/api/1/linked-art',
    abp_security=[{'bearerAuth': []}])
register_error_handlers(api_v1_la)


@api_v1_la.get(
    '/entity/<uuid:uuid>',
    summary='Get a strictly compliant Linked Art entity by UUID',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity(path: EntityPath) -> dict[str, Any] | Response:
    """
    Retrieves a single entity formatted as Linked Art.

    The record is built directly from the Linked Art entity profiles and
    only contains properties allowed by the Linked Art JSON schemas
    (additionalProperties: false).
    """
    return get_entity_response(path.uuid, formatter=format_la_entity)


@api_v1_la.get(
    '/entity/<uuid:uuid>.<ext>',
    summary='Get a strictly compliant Linked Art entity by UUID '
            'with extension',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity_ext(path: EntityPathExt) -> dict[str, Any] | Response:
    """
    Retrieves a single Linked Art entity with a specific format extension.
    """
    ext_val = path.ext.value if hasattr(path.ext, 'value') else str(path.ext)
    return get_entity_response(
        path.uuid,
        ext=ext_val,
        formatter=format_la_entity)


@api_v1_la.get(
    '/entities/<string:entity_class>',
    summary='Get a polymorphic collection of Linked Art entities',
    tags=[lod_tag],
    responses=lod_collection_responses)
def get_entities(
        path: EntityCollectionPath,
        query: EntityCollectionQuery) -> dict[str, Any] | Response:
    """
    Retrieves a paginated collection of entities formatted as strict
    Linked Art.
    """
    return get_entities_response(
        path,
        query,
        endpoint='api_v1_la.get_entities',
        formatter=format_la_entities)


@api_v1_la.get(
    '/export/dump',
    summary='Stream full Linked Art dump in JSON Lines or N-Triples format',
    tags=[lod_tag],
    responses=la_dump_responses)
def get_la_dump(query: LaDumpQuery) -> Response:
    """
    Streams a full Linked Art export.
    Defaults to JSON Lines (`.jsonl` / `application/x-ndjson`), where each line
    is a complete, valid Linked Art JSON-LD document.
    Can also stream N-Triples (`.nt`) by setting `format=nt`.

    Requires user authentication (Flask session cookie or JWT Bearer token).
    """
    require_auth()
    ext = 'jsonl' if query.format == 'jsonl' else 'nt'
    mimetype = (
        'application/x-ndjson' if query.format == 'jsonl'
        else 'application/n-triples')
    filename = f'openatlas_linked_art_dump.{ext}'
    if query.entity_class:
        filename = f'openatlas_linked_art_{query.entity_class}.{ext}'
    return Response(
        stream_with_context(
            stream_la_dump(
                class_name=query.entity_class,
                limit=query.limit,
                output_format=query.format)),
        mimetype=mimetype,
        headers={'Content-Disposition': f'attachment; filename="{filename}"'})
