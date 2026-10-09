from typing import Any

from flask import Response
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.formatters.la import (
    format_la_entities, format_la_entity)
from openatlas.api.api_v1.formatters.lod_util import (
    get_entities_response, get_entity_response)
from openatlas.api.api_v1.models.lod import (
    EntityCollectionPath, EntityCollectionQuery, EntityPath, EntityPathExt)
from openatlas.api.api_v1.openapi_tags import lod_tag
from openatlas.api.api_v1.responses.lod import (
    lod_collection_responses, lod_responses)

api_v1_la = APIBlueprint('api_v1_la', __name__, url_prefix='/api/1/linked-art')
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
        path.uuid, ext=ext_val, formatter=format_la_entity)


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
