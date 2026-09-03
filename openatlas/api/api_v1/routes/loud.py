from typing import Any

from flask import Response
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.formatters.loud import (
    format_loud_entities, format_loud_entity)
from openatlas.api.api_v1.formatters.lod_util import (
    get_entities_response, get_entity_response)
from openatlas.api.api_v1.models.lod import (
    EntityCollectionPath, EntityCollectionQuery, EntityPath, EntityPathExt)
from openatlas.api.api_v1.openapi_tags import lod_tag
from openatlas.api.api_v1.responses.lod import (
    lod_collection_responses, lod_responses)

api_v1_loud = APIBlueprint('api_v1_loud', __name__, url_prefix='/api/1/loud')
register_error_handlers(api_v1_loud)


@api_v1_loud.get(
    '/entity/<uuid:id>',
    endpoint='loud_entity',
    summary='Get a strictly compliant Linked.Art LOUD entity by UUID',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity(path: EntityPath) -> dict[str, Any] | Response:
    """
    Retrieves a single entity formatted as Linked Open Usable Data (Linked.Art).

    This endpoint applies strict profile cleaning to ensure additionalProperties: false
    compliance with the Linked.Art standard.
    """
    return get_entity_response(path.id, formatter=format_loud_entity)


@api_v1_loud.get(
    '/entity/<uuid:id>.<ext>',
    endpoint='loud_entity_ext',
    summary='Get a strictly compliant Linked.Art LOUD entity by UUID with extension',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity_ext(path: EntityPathExt) -> dict[str, Any] | Response:
    """
    Retrieves a single LOUD entity with a specific format extension.
    """
    ext_val = path.ext.value if hasattr(path.ext, 'value') else str(path.ext)
    return get_entity_response(
        path.id, ext=ext_val, formatter=format_loud_entity)


@api_v1_loud.get(
    '/entities/<string:entity_class>',
    endpoint='loud_entities',
    summary='Get a polymorphic collection of Linked.Art LOUD entities',
    tags=[lod_tag],
    responses=lod_collection_responses)
def get_entities(
        path: EntityCollectionPath,
        query: EntityCollectionQuery) -> dict[str, Any] | Response:
    """
    Retrieves a paginated collection of entities formatted as strict Linked.Art LOUD.
    """
    return get_entities_response(
        path,
        query,
        endpoint='api_v1_loud.loud_entities',
        formatter=format_loud_entities)
