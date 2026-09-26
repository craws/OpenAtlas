from typing import Any
from uuid import UUID

from flask import g
from werkzeug.exceptions import ImATeapot

from openatlas.api.api_v1.error_handlers import abort_not_found
from openatlas.database.api import get_by_class_api, get_count_by_class_api
from openatlas.models.entity import Entity
from openatlas.models.rights_holder import RightsHolder


def get_entity_by_id(
        id_: int,
        types: bool = False,
        aliases: bool = False,
        with_location: bool = True) -> Entity:
    try:
        return Entity.get_by_id(
            id_,
            types=types,
            aliases=aliases,
            with_location=with_location)
    except ImATeapot:
        abort_not_found(id_)

def get_entity_by_uuid(
        uuid: UUID,
        types: bool = False,
        aliases: bool = False,
        with_location: bool = True) -> Entity | None:
    try:
        return Entity.get_by_uuid(
            uuid,
            types=types,
            aliases=aliases,
            with_location=with_location)
    except ImATeapot:
        abort_not_found(uuid)


def get_rightsholder_by_id(id_: int) -> RightsHolder:
    try:
        return RightsHolder.get_rights_holder_by_id(id_)
    except ImATeapot:
        abort_not_found(id_)


def resolve_type_ids(identifier: int | UUID | None) -> list[int] | None:
    if identifier is None:
        return None

    if isinstance(identifier, int):
        entity = g.types.get(identifier)
        return [identifier, *entity.get_sub_ids_recursive()] \
            if entity else None

    uuid_str = str(identifier)
    for type_id, entity in g.types.items():
        if str(entity.uuid) == uuid_str:
            return [type_id, *entity.get_sub_ids_recursive()]

    return None


def get_by_system_class(
        class_name: str,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        start_date: Any = None,
        end_date: Any = None,
        type_id: int | UUID | None = None,
        case_study: int | UUID | None = None) -> list[Entity]:
    type_ids = resolve_type_ids(type_id)
    case_study_ids = resolve_type_ids(case_study)
    aliases = True
    if not g.classes[class_name].attributes.get('alias'):
        aliases = False
    return [
        Entity(row) for row in get_by_class_api(
            class_name,
            types=True,
            aliases=aliases,
            order_by=order_by,
            limit=limit,
            offset=offset,
            search_name=search,
            start_date=start_date,
            end_date=end_date,
            type_ids=type_ids,
            case_study_ids=case_study_ids)]


def get_count_by_system_class(
        class_name: str,
        search: str | None = None,
        start_date: Any = None,
        end_date: Any = None,
        type_id: int | str | UUID | None = None,
        case_study: int | str | UUID | None = None) -> int:
    type_ids = resolve_type_ids(type_id)
    case_study_ids = resolve_type_ids(case_study)
    return get_count_by_class_api(
        class_name,
        search_name=search,
        start_date=start_date,
        end_date=end_date,
        type_ids=type_ids,
        case_study_ids=case_study_ids)
