from typing import Any

from flask import Response
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.formatters.lod import (
    format_lod_entities, format_lod_entity)
from openatlas.api.api_v1.formatters.lod_util import (
    get_entities_response, get_entity_response)
from openatlas.api.api_v1.models.lod import (
    EntityCollectionPath, EntityCollectionQuery, EntityPath, EntityPathExt)
from openatlas.api.api_v1.openapi_tags import lod_tag
from openatlas.api.api_v1.responses.lod import (
    lod_collection_responses, lod_responses)

api_v1_lod = APIBlueprint('api_v1_lod', __name__, url_prefix='/api/1')
register_error_handlers(api_v1_lod)


@api_v1_lod.get(
    '/entity/<uuid:id>',
    endpoint='entity',
    summary='Get an LOD entity by UUID',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity(path: EntityPath) -> dict[str, Any] | Response:
    """
    Retrieves a single entity formatted as Linked Open Data (OpenAtlas CIDOC-CRM graph).
    
    The response format defaults to `application/ld+json`. 
    You can request other formats (like Turtle or RDF/XML) using the `Accept`
    HTTP header.
    """
    return get_entity_response(path.id, formatter=format_lod_entity)


@api_v1_lod.get(
    '/entity/<uuid:id>.<ext>',
    endpoint='entity_ext',
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
        path.id, ext=ext_val, formatter=format_lod_entity)


@api_v1_lod.get(
    '/entities/<string:entity_class>',
    endpoint='entities',
    summary='Get a polymorphic collection of entities',
    tags=[lod_tag],
    responses=lod_collection_responses)
def get_entities(
        path: EntityCollectionPath,
        query: EntityCollectionQuery) -> dict[str, Any] | Response:
    """
    Retrieves a paginated collection of entities formatted as Linked Open Data.
    
    This endpoint allows querying a specific system class (e.g. `person`, `place`).
    Results are returned as a Hydra Collection and can be filtered by various 
    query parameters such as search strings, dates, or case studies.
    """
    return get_entities_response(
        path,
        query,
        endpoint='api_v1_lod.entities',
        formatter=format_lod_entities)
