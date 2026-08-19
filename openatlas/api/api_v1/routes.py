from typing import Any

from flask import Response
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v04.resources.api_entity import ApiEntity
from openatlas.api.api_v1.error_handlers import (
    abort_not_found, register_error_handlers)
from openatlas.api.api_v1.loud.loud import format_loud_entities, \
    format_loud_entity
from openatlas.api.api_v1.loud.loud_util import (
    make_lod_response, set_accept_header)
from openatlas.api.api_v1.models import (
    EntityCollectionPath, EntityCollectionQuery, EntityPath)
from openatlas.api.api_v1.openapi_responses import lod_responses
from openatlas.api.api_v1.openapi_tags import lod_tag
from openatlas.models.entity import Entity

api_v1 = APIBlueprint('api_v1', __name__, url_prefix='/api/1')
register_error_handlers(api_v1)


@api_v1.get(
    '/entity/<uuid:id>',
    endpoint='entity',
    summary='Get an LOD entity by UUID',
    tags=[lod_tag],
    responses=lod_responses)
@api_v1.get(
    '/entity/<uuid:id>.<ext>',
    endpoint='entity_ext',
    summary='Get an LOD entity by UUID with extension',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity(path: EntityPath) -> dict[str, Any] | Response:
    set_accept_header(path.ext)
    entity = Entity.get_by_uuid(path.id, types=True, aliases=True)

    if not entity:
        abort_not_found(path.id)

    return make_lod_response(format_loud_entity(entity))


@api_v1.get(
    '/entities/<string:entity_class>',
    endpoint='entities',
    summary='Get a polymorphic collection of entities',
    tags=[lod_tag],
    responses=lod_responses)
@api_v1.get(
    '/entities/<string:entity_class>.<ext>',
    endpoint='entities_ext',
    summary='Get a polymorphic collection of entities',
    tags=[lod_tag],
    responses=lod_responses)
def get_entities(
        path: EntityCollectionPath,
        query: EntityCollectionQuery) -> dict[str, Any] | Response:
    set_accept_header(path.ext)
    entities = ApiEntity.get_by_system_classes([path.entity_class])
    return make_lod_response(format_loud_entities(entities))
