from typing import Any

from flask import g

from openatlas.util.util import format_date_part


def populate_types(manager) -> None:
    types: dict[Any, Any] = manager.entity.types
    # if manager.location:
    #    types |= manager.location.types  # Admin. units and historical places
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


def populate_reference_systems(manager) -> None:
    system_links = {
        # Can't use isinstance for class check here
        link_.domain.id: link_ for link_ in manager.entity.get_links('P67', True)
        if link_.domain.class_.name == 'reference_system'}
    for key in manager.form.data:
        field = getattr(manager.form, key)
        if field.id.startswith('reference_system_id_'):
            system_id = int(field.id.replace('reference_system_id_', ''))
            if system_id in system_links:
                field.data = system_links[system_id].description
                precision_field = getattr(
                    manager.form,
                    f'reference_system_precision_{system_id}')
                precision_field.data = str(system_links[system_id].type.id)


def populate_dates(manager) -> None:
    if manager.entity.begin_from:
        manager.form.begin_year_from.data = \
            format_date_part(manager.entity.begin_from, 'year')
        manager.form.begin_month_from.data = \
            format_date_part(manager.entity.begin_from, 'month')
        manager.form.begin_day_from.data = \
            format_date_part(manager.entity.begin_from, 'day')
        if 'begin_hour_from' in manager.form:
            manager.form.begin_hour_from.data = \
                format_date_part(manager.entity.begin_from, 'hour')
            manager.form.begin_minute_from.data = \
                format_date_part(manager.entity.begin_from, 'minute')
            manager.form.begin_second_from.data = \
                format_date_part(manager.entity.begin_from, 'second')
        manager.form.begin_comment.data = manager.entity.begin_comment
        if manager.entity.begin_to:
            manager.form.begin_year_to.data = \
                format_date_part(manager.entity.begin_to, 'year')
            manager.form.begin_month_to.data = \
                format_date_part(manager.entity.begin_to, 'month')
            manager.form.begin_day_to.data = \
                format_date_part(manager.entity.begin_to, 'day')
            if 'begin_hour_from' in manager.form:
                manager.form.begin_hour_to.data = \
                    format_date_part(manager.entity.begin_to, 'hour')
                manager.form.begin_minute_to.data = \
                    format_date_part(manager.entity.begin_to, 'minute')
                manager.form.begin_second_to.data = \
                    format_date_part(manager.entity.begin_to, 'second')
    if manager.entity.end_from:
        manager.form.end_year_from.data = \
            format_date_part(manager.entity.end_from, 'year')
        manager.form.end_month_from.data = \
            format_date_part(manager.entity.end_from, 'month')
        manager.form.end_day_from.data = \
            format_date_part(manager.entity.end_from, 'day')
        if 'begin_hour_from' in manager.form:
            manager.form.end_hour_from.data = \
                format_date_part(manager.entity.end_from, 'hour')
            manager.form.end_minute_from.data = \
                format_date_part(manager.entity.end_from, 'minute')
            manager.form.end_second_from.data = \
                format_date_part(manager.entity.end_from, 'second')
        manager.form.end_comment.data = manager.entity.end_comment
        if manager.entity.end_to:
            manager.form.end_year_to.data = \
                format_date_part(manager.entity.end_to, 'year')
            manager.form.end_month_to.data = \
                format_date_part(manager.entity.end_to, 'month')
            manager.form.end_day_to.data = \
                format_date_part(manager.entity.end_to, 'day')
            if 'begin_hour_from' in manager.form:
                manager.form.end_hour_to.data = \
                    format_date_part(manager.entity.end_to, 'hour')
                manager.form.end_minute_to.data = \
                    format_date_part(manager.entity.end_to, 'minute')
                manager.form.end_second_to.data = \
                    format_date_part(manager.entity.end_to, 'second')
