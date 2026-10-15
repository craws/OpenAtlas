from collections.abc import Callable
from typing import Any
from uuid import UUID

from flask import Response

from openatlas.api.api_v1.entity import (
    get_by_system_class, get_count_by_system_class, get_entity_by_uuid)
from openatlas.api.api_v1.error_handlers import abort_not_found
from openatlas.api.api_v1.util.content_negotiation import make_lod_response
from openatlas.api.api_v1.util.pagination import get_pagination
from openatlas.models.entity import Entity


def get_entity_response(
        entity_id: UUID,
        formatter: Callable[[Entity], dict[str, Any]],
        ext: str | None = None) -> dict[str, Any] | Response:
    entity = get_entity_by_uuid(entity_id, types=True, aliases=True)
    if not entity:
        abort_not_found(entity_id)
    return make_lod_response(formatter(entity), ext=ext)


def get_entities_response(
        path: Any,
        query: Any,
        endpoint: str,
        formatter: Callable[..., dict[str, Any]]) -> dict[str, Any] | Response:
    entity_class_name = (
        path.entity_class.value
        if hasattr(path.entity_class, 'value') else str(path.entity_class))

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
        endpoint,
        total_items=total_items,
        page=query.page,
        limit=query.limit,
        entity_class=entity_class_name)
    return make_lod_response(
        formatter(entities, pagination=pagination))
