import time
from typing import Any

from flask import g

from openatlas.models.dates import Dates, format_date_part
from openatlas.models.entity import Entity


def populate_insert(form: Any) -> None:
    if hasattr(form, 'alias'):
        form.alias.append_entry('')


def populate_update(form: Any, entity: Entity) -> None:
    form.opened.data = time.time()
    # Todo: deal with place types
    # if manager.entity and manager.entity.class_.name == 'place':
    #     if location := \
    #             manager.entity.get_linked_entity_safe('P53', types=True):
    #        types |= location.types  # Admin. units and historical places
    # Todo: implement copy
    # if entity.id and not copy:
    #     form.entity_id.data = entity.id
    populate_reference_systems(form, entity)
    if 'dates' in entity.class_.attributes:
        populate_dates(form, entity.dates)
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

    if entity.class_.group['name'] == 'type':
        if len(entity.root) > 1:
            getattr(form, 'super').data = entity.root[-1]


def populate_reference_systems(form: Any, entity: Entity) -> None:
    for link_ in entity.get_links('P67', ['reference_system'], inverse=True):
        getattr(form, f'reference_system_id_{link_.domain.id}').data = {
            'value': link_.description,
            'precision': str(link_.type.id)}


def populate_dates(form: Any, dates: Dates) -> None:
    for item in ['begin', 'end']:
        from_ = getattr(dates, f'{item}_from')
        to = getattr(dates, f'{item}_to')
        if from_:
            getattr(form, f'{item}_year_from').data = \
                format_date_part(from_, 'year')
            getattr(form, f'{item}_month_from').data = \
                format_date_part(from_, 'month')
            getattr(form, f'{item}_day_from').data = \
                format_date_part(from_, 'day')
            if 'begin_hour_from' in form:
                getattr(form, f'{item}_hour_from').data = \
                    format_date_part(from_, 'hour')
                getattr(form, f'{item}_minute_from').data = \
                    format_date_part(from_, 'minute')
                getattr(form, f'{item}_second_from').data = \
                    format_date_part(from_, 'second')
            form.begin_comment.data = dates.begin_comment
            if to:
                getattr(form, f'{item}_year_to').data = \
                    format_date_part(to, 'year')
                getattr(form, f'{item}_month_to').data = \
                    format_date_part(to, 'month')
                getattr(form, f'{item}_day_to').data = \
                    format_date_part(to, 'day')
                if 'begin_hour_from' in form:
                    getattr(form, f'{item}_hour_to').data = \
                        format_date_part(to, 'hour')
                    getattr(form, f'{item}_minute_to').data = \
                        format_date_part(to, 'minute')
                    getattr(form, f'{item}_second_to').data = \
                        format_date_part(to, 'second')
                form.end_comment.data = dates.end_comment
