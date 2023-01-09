from typing import Any

from flask import g

from openatlas.display.util import format_date_part


def populate_types(manager: Any) -> None:
    types: dict[Any, Any] = manager.link_.types \
        if manager.link_ else manager.entity.types
    if manager.entity and manager.entity.class_.name == 'place':
        if location := \
                manager.entity.get_linked_entity_safe('P53', types=True):
            types |= location.types  # Admin. units and historical places
    type_data: dict[int, list[int]] = {}
    for type_, value in types.items():
        root = g.types[type_.root[0]] if type_.root else type
        if root.id not in type_data:
            type_data[root.id] = []
        type_data[root.id].append(type_.id)
        if root.category == 'value':
            getattr(manager.form, str(type_.id)).data = value
    for root_id, types_ in type_data.items():
        if hasattr(manager.form, str(root_id)):
            getattr(manager.form, str(root_id)).data = types_


def populate_reference_systems(manager: Any) -> None:
    if not manager.entity:
        return  # It's a link update which have no reference systems
    system_links = {
        # Can't use isinstance for class check here
        link_.domain.id:
            link_ for link_ in manager.entity.get_links('P67', True)
        if link_.domain.class_.name == 'reference_system'}
    for key in manager.form.data:
        field = getattr(manager.form, key)
        if field.id.startswith('reference_system_id_'):
            system_id = int(field.id.replace('reference_system_id_', ''))
            if system_id in system_links:
                field.data = {}
                field.data['value'] = system_links[system_id].description
                field.data['precision'] = str(system_links[system_id].type.id)


def populate_dates(manager: Any) -> None:
    form = manager.form
    item = manager.link_ or manager.entity
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
