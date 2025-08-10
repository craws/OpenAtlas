import time
from typing import Any

from flask import g

from openatlas.display.util2 import format_date_part
from openatlas.models.entity import Entity, Link


def populate_insert(form: Any, entity: Entity) -> None:
    if hasattr(form, 'alias'):
        form.alias.append_entry('')


def populate_update(form: Any, entity: Entity) -> None:
    form.opened.data = time.time()  # Todo: what if POST because of not valid?
    # Todo: deal with link types
    # types: dict[Any, Any] = manager.link_.types \
    #    if manager.link_ else manager.entity.types
    # Todo: deal with place types
    # if manager.entity and manager.entity.class_.name == 'place':
    #     if location := \
    #             manager.entity.get_linked_entity_safe('P53', types=True):
    #        types |= location.types  # Admin. units and historical places
    # Todo: implement copy
    # if entity.id and not copy:
    #     form.entity_id.data = entity.id
    populate_reference_systems(form, entity)
    if 'date' in entity.class_.attributes:
        populate_dates(form, entity)
    if hasattr(form, 'alias'):
        for alias in entity.aliases.values():
            form.alias.append_entry(alias)
        form.alias.append_entry('')

    type_data: dict[int, list[int]] = {}
    for type_, value in entity.types.items():
        root = g.types[type_.root[0]] if type_.root else type
        if root.id not in type_data:
            type_data[root.id] = []
        type_data[root.id].append(type_.id)
        if root.category == 'value':
            getattr(form, str(type_.id)).data = value
    for root_id, types_ in type_data.items():
        if hasattr(form, str(root_id)):
            getattr(form, str(root_id)).data = types_


def populate_reference_systems(form: Any, entity: Entity) -> None:
    for link_ in entity.get_links('P67', ['reference_system'], inverse=True):
        getattr(form, f'reference_system_id_{link_.domain.id}').data = {
            'value': link_.description,
            'precision': str(link_.type.id)}


def populate_dates(form: Any, item: Entity | Link) -> None:
    if item.begin_from:
        form.begin_year_from.data = format_date_part(item.begin_from, 'year')
        form.begin_month_from.data = format_date_part(item.begin_from, 'month')
        form.begin_day_from.data = format_date_part(item.begin_from, 'day')
        if 'begin_hour_from' in form:
            form.begin_hour_from.data = \
                format_date_part(item.begin_from, 'hour')
            form.begin_minute_from.data = \
                format_date_part(item.begin_from, 'minute')
            form.begin_second_from.data = \
                format_date_part(item.begin_from, 'second')
        form.begin_comment.data = item.begin_comment
        if item.begin_to:
            form.begin_year_to.data = format_date_part(item.begin_to, 'year')
            form.begin_month_to.data = format_date_part(item.begin_to, 'month')
            form.begin_day_to.data = format_date_part(item.begin_to, 'day')
            if 'begin_hour_from' in form:
                form.begin_hour_to.data = \
                    format_date_part(item.begin_to, 'hour')
                form.begin_minute_to.data = \
                    format_date_part(item.begin_to, 'minute')
                form.begin_second_to.data = \
                    format_date_part(item.begin_to, 'second')
    if item.end_from:
        form.end_year_from.data = format_date_part(item.end_from, 'year')
        form.end_month_from.data = format_date_part(item.end_from, 'month')
        form.end_day_from.data = format_date_part(item.end_from, 'day')
        if 'begin_hour_from' in form:
            form.end_hour_from.data = format_date_part(item.end_from, 'hour')
            form.end_minute_from.data = \
                format_date_part(item.end_from, 'minute')
            form.end_second_from.data = \
                format_date_part(item.end_from, 'second')
        form.end_comment.data = item.end_comment
        if item.end_to:
            form.end_year_to.data = format_date_part(item.end_to, 'year')
            form.end_month_to.data = format_date_part(item.end_to, 'month')
            form.end_day_to.data = format_date_part(item.end_to, 'day')
            if 'begin_hour_from' in form:
                form.end_hour_to.data = format_date_part(item.end_to, 'hour')
                form.end_minute_to.data = \
                    format_date_part(item.end_to, 'minute')
                form.end_second_to.data = \
                    format_date_part(item.end_to, 'second')
