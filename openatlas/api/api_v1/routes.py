import math
from typing import Any
from urllib.parse import urlencode

from flask import Response, request, url_for
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.entity import (
    get_by_system_class, get_count_by_system_class)
from openatlas.api.api_v1.error_handlers import (
    abort_not_found, register_error_handlers)
from openatlas.api.api_v1.loud.loud import (
    format_loud_entities, format_loud_entity)
from openatlas.api.api_v1.loud.loud_util import (
    make_lod_response, set_accept_header)
from openatlas.api.api_v1.models import (
    EntityCollectionPath, EntityCollectionQuery, EntityPath)
from openatlas.api.api_v1.openapi_responses import (
    lod_collection_responses, lod_responses)
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
    responses=lod_collection_responses)
def get_entities(
        path: EntityCollectionPath,
        query: EntityCollectionQuery) -> dict[str, Any] | Response:
    entity_class_name = (
        path.entity_class.value
        if hasattr(path.entity_class, 'value')
        else str(path.entity_class))

    page = query.page
    limit = query.limit
    sort_dir = query.sort
    sort_field = 'name'
    if query.sort_by in ('startDate', 'start_date'):
        sort_field = 'start_date'
    elif query.sort_by in ('endDate', 'end_date'):
        sort_field = 'end_date'
    order_by = f'{sort_field}_{sort_dir}'
    offset = (page - 1) * limit

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
        limit=limit,
        offset=offset,
        **filter_kwargs)

    base_url = url_for(
        'api_v1.entities',
        entity_class=entity_class_name,
        _external=True)

    query_params = dict(request.args)

    def page_url(p: int) -> str:
        params = dict(query_params)
        params['page'] = p
        return f'{base_url}?{urlencode(params)}'

    total_pages = max(1, math.ceil(total_items / limit))
    pagination: dict[str, Any] = {
        'total_items': total_items,
        'id': page_url(page),
        'first': page_url(1),
        'last': page_url(total_pages)}
    if page > 1:
        pagination['previous'] = page_url(page - 1)
    if page < total_pages:
        pagination['next'] = page_url(page + 1)

    return make_lod_response(
        format_loud_entities(entities, pagination=pagination))
