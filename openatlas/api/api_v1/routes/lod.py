from typing import Any

from flask import Response, stream_with_context
from flask_openapi3 import APIBlueprint

from openatlas import app
from openatlas.api.api_v1.context.lod_context import (
    get_lod_context, get_oa_ontology_graph)
from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.formatters.lod import (
    format_lod_entities, format_lod_entity)
from openatlas.api.api_v1.formatters.lod_export import stream_lod_nt
from openatlas.api.api_v1.formatters.lod_util import (
    get_entities_response, get_entity_response)
from openatlas.api.api_v1.models.lod import (
    EntityCollectionPath, EntityCollectionQuery, EntityPath, EntityPathExt,
    ExtensionPath, LodDumpQuery)
from openatlas.api.api_v1.openapi_tags import lod_tag
from openatlas.api.api_v1.responses.lod import (
    context_responses, dump_responses, lod_collection_responses, lod_responses,
    ontology_responses)
from openatlas.api.api_v1.util.auth import require_auth
from openatlas.api.api_v1.util.content_negotiation import make_graph_response

api_v1_lod = APIBlueprint(
    'api_v1_lod',
    __name__,
    url_prefix='/api/1',
    abp_security=[{'bearerAuth': []}])
register_error_handlers(api_v1_lod)


@api_v1_lod.get(
    '/entity/<uuid:uuid>',
    summary='Get an LOD entity by UUID',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity(path: EntityPath) -> dict[str, Any] | Response:
    """
    Retrieves a single entity formatted as Linked Open Data
    (OpenAtlas CIDOC-CRM graph).

    The response format defaults to `application/ld+json`.
    You can request other formats (like Turtle or RDF/XML) using the `Accept`
    HTTP header.
    """
    return get_entity_response(path.uuid, formatter=format_lod_entity)


@api_v1_lod.get(
    '/entity/<uuid:uuid>.<ext>',
    summary='Get an LOD entity by UUID with extension',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity_ext(path: EntityPathExt) -> dict[str, Any] | Response:
    """
    Retrieves a single LOD entity with a specific format extension.

    This is an alternative to using the HTTP `Accept` header.
    By appending an extension like `.json`, `.ttl`, or `.xml` to the URL,
    the API will automatically return the entity in the requested format.
    """
    ext_val = path.ext.value if hasattr(path.ext, 'value') else str(path.ext)
    return get_entity_response(
        path.uuid, ext=ext_val, formatter=format_lod_entity)


@api_v1_lod.get(
    '/entities/<string:entity_class>',
    summary='Get a polymorphic collection of entities',
    tags=[lod_tag],
    responses=lod_collection_responses)
def get_entities(
        path: EntityCollectionPath,
        query: EntityCollectionQuery) -> dict[str, Any] | Response:
    """
    Retrieves a paginated collection of entities formatted as Linked Open Data.

    This endpoint allows querying a specific system class
    (e.g. `person`, `place`).
    Results are returned as an OrderedCollectionPage and can be filtered by
    various query parameters such as search strings, dates, or case studies.
    """
    return get_entities_response(
        path,
        query,
        endpoint='api_v1_lod.get_entities',
        formatter=format_lod_entities)


@api_v1_lod.get(
    '/context.json',
    summary='Get the OpenAtlas LOD JSON-LD @context',
    tags=[lod_tag],
    responses=context_responses)
def get_context() -> Response:
    """
    Returns the OpenAtlas JSON-LD context mapping human-readable property
    and class names to CIDOC CRM, CRMarchaeo, GeoSPARQL, and OpenAtlas URIs.
    """
    return Response(
        app.json.dumps(get_lod_context()),
        mimetype='application/ld+json')


@api_v1_lod.get(
    '/ontology',
    summary='Get the OpenAtlas extension ontology graph',
    tags=[lod_tag],
    responses=ontology_responses)
def get_ontology() -> Response:
    """
    Returns the OpenAtlas extension ontology (defining shortcuts like
    oa:has_relationship_to, oa:begins_in, oa:ends_in) in the requested RDF format.
    Format is determined via HTTP Accept header (defaults to JSON-LD).
    """
    return make_graph_response(get_oa_ontology_graph())


@api_v1_lod.get(
    '/ontology.<ext>',
    summary='Get the OpenAtlas extension ontology with extension',
    tags=[lod_tag],
    responses=ontology_responses)
def get_ontology_ext(path: ExtensionPath) -> Response:
    """
    Returns the OpenAtlas extension ontology with format specified by URL extension
    (.json, .ttl, .xml, .nt).
    """
    ext_val = path.ext.value if hasattr(path.ext, 'value') else str(path.ext)
    return make_graph_response(get_oa_ontology_graph(), ext=ext_val)


@api_v1_lod.get(
    '/export/dump',
    summary='Stream full Linked Open Data dump in N-Triples format',
    tags=[lod_tag],
    responses=dump_responses)
def get_lod_dump(query: LodDumpQuery) -> Response:
    """
    Streams a full Linked Open Data export in N-Triples (.nt) format.
    Requires user authentication (Flask session cookie or JWT Bearer token).

    Supports keyset streaming with low memory footprint. Optional query
    parameters allow limiting the exported entities or filtering by entity class.
    """
    require_auth()
    filename = 'openatlas_lod_dump.nt'
    if query.entity_class:
        filename = f'openatlas_{query.entity_class}_lod.nt'
    return Response(
        stream_with_context(
            stream_lod_nt(
                class_name=query.entity_class,
                limit=query.limit)),
        mimetype='application/n-triples',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'})
