from typing import Any
from uuid import UUID

from flask import Response
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.entity import (
    get_by_system_class, get_count_by_system_class)
from openatlas.api.api_v1.error_handlers import (
    abort_not_found, register_error_handlers)
from openatlas.api.api_v1.loud.loud import (
    format_loud_entities, format_loud_entity)
from openatlas.api.api_v1.loud.loud_util import (
    make_lod_response, set_accept_header)
from openatlas.api.api_v1.models.lod import (
    EntityCollectionPath, EntityCollectionQuery, EntityPath, EntityPathExt)
from openatlas.api.api_v1.openapi_responses import (
    lod_collection_responses, lod_responses)
from openatlas.api.api_v1.openapi_tags import lod_tag
from openatlas.api.api_v1.pagination import get_pagination
from openatlas.models.entity import Entity

#todo: move to better location
api_v1 = APIBlueprint('api_v1', __name__, url_prefix='/api/1')
register_error_handlers(api_v1)


def _get_entity_response(
        entity_id: UUID,
        ext: str | None = None) -> dict[str, Any] | Response:
    if ext:
        set_accept_header(ext)
    entity = Entity.get_by_uuid(entity_id, types=True, aliases=True)

    if not entity:
        abort_not_found(entity_id)

    return make_lod_response(format_loud_entity(entity))


@api_v1.get(
    '/entity/<uuid:id>',
    endpoint='entity',
    summary='Get an LOD entity by UUID',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity(path: EntityPath) -> dict[str, Any] | Response:
    return _get_entity_response(path.id)


@api_v1.get(
    '/entity/<uuid:id>.<ext>',
    endpoint='entity_ext',
    summary='Get an LOD entity by UUID with extension',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity_ext(path: EntityPathExt) -> dict[str, Any] | Response:
    ext_val = path.ext.value if hasattr(path.ext, 'value') else str(path.ext)
    return _get_entity_response(path.id, ext=ext_val)


@api_v1.get(
    '/entities/<string:entity_class>',
    endpoint='entities',
    summary='Get a polymorphic collection of entities',
    tags=[lod_tag],
    responses=lod_collection_responses)
def get_entities(
        path: EntityCollectionPath,
        query: EntityCollectionQuery) -> dict[str, Any] | Response:
    entity_class_name = (
        path.entity_class.value
        if hasattr(path.entity_class, 'value')
        else str(path.entity_class))

    order_by = f'{query.sort_by}_{query.sort}'
    offset = (query.page - 1) * query.limit

    filter_kwargs = {
        'search': query.search,
        'start_date': query.start_date,
        'end_date': query.end_date,
        'type_id': query.type_id,
        'case_study': query.case_study}

    total_items = get_count_by_system_class(
        entity_class_name,
        **filter_kwargs)
    entities = get_by_system_class(
        entity_class_name,
        order_by=order_by,
        limit=query.limit,
        offset=offset,
        **filter_kwargs)

    pagination = get_pagination(
        'api_v1.entities',
        total_items=total_items,
        page=query.page,
        limit=query.limit,
        entity_class=entity_class_name)

    return make_lod_response(
        format_loud_entities(entities, pagination=pagination))
