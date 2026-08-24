from typing import Any
from uuid import UUID

from flask import g

from openatlas.api.api_v1.error_handlers import abort_invalid_class
from openatlas.models.entity import Entity


def resolve_type_ids(
        identifier: int | str | UUID | None) -> list[int] | None:
    if identifier is None:
        return None
    if isinstance(identifier, int):
        type_id = identifier
    elif isinstance(identifier, str) and identifier.isdigit():
        type_id = int(identifier)
    else:
        uuid_str = str(identifier)
        for t_id, type_entity in g.types.items():
            if str(type_entity.uuid) == uuid_str:
                return [t_id] + type_entity.get_sub_ids_recursive()
        entity = Entity.get_by_uuid(uuid_str)
        if not entity:
            return []
        type_id = entity.id

    if type_id in g.types:
        return [type_id] + g.types[type_id].get_sub_ids_recursive()
    return [type_id]


def _validate_class(name: str) -> str:
    if name not in g.classes:
        abort_invalid_class(name)
    return name


def get_by_system_class(
        name: str,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        start_date: Any = None,
        end_date: Any = None,
        type_id: int | str | UUID | None = None,
        case_study: int | str | UUID | None = None) -> list[Entity]:
    class_name = _validate_class(name)
    type_ids = resolve_type_ids(type_id)
    case_study_ids = resolve_type_ids(case_study)
    return Entity.get_by_class_api(
        class_name,
        types=True,
        aliases=True,
        order_by=order_by,
        limit=limit,
        offset=offset,
        search=search,
        start_date=start_date,
        end_date=end_date,
        type_ids=type_ids,
        case_study_ids=case_study_ids)


def get_count_by_system_class(
        name: str,
        search: str | None = None,
        start_date: Any = None,
        end_date: Any = None,
        type_id: int | str | UUID | None = None,
        case_study: int | str | UUID | None = None) -> int:
    class_name = _validate_class(name)
    type_ids = resolve_type_ids(type_id)
    case_study_ids = resolve_type_ids(case_study)
    return Entity.get_count_by_class_api(
        class_name,
        search_name=search,
        start_date=start_date,
        end_date=end_date,
        type_ids=type_ids,
        case_study_ids=case_study_ids)
