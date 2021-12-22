import time
from typing import Dict, List, Union

from flask import g
from flask_wtf import FlaskForm

from openatlas.util.util import format_date_part
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type


def pre_populate_form(
        form: FlaskForm,
        item: Union[Entity, Link],
        location: Union[Entity, None]) -> FlaskForm:
    form.opened.data = time.time()
    if hasattr(form, 'begin_year_from'):
        populate_dates(form, item)
    if isinstance(item, Entity):
        populate_reference_systems(form, item)
    if isinstance(item, ReferenceSystem) and item.system:
        form.name.render_kw['readonly'] = 'readonly'
    if isinstance(item, Entity) and item.class_.view == 'event':
        form.event_id.data = item.id

    # Types
    types: Dict[Type, str] = item.types
    if location:  # Needed for administrative unit and historical place types
        types.update(location.types)
    type_data: Dict[int, List[int]] = {}
    for type_, value in types.items():
        root = g.types[type_.root[0]] if type_.root else type
        if root.id not in type_data:
            type_data[root.id] = []
        type_data[root.id].append(type_.id)
        if root.category == 'value':
            getattr(form, str(type_.id)).data = value
    for root_id, types_ in type_data.items():
        if hasattr(form, str(root_id)):
            getattr(form, str(root_id)).data = types_
    return form


def populate_reference_systems(form: FlaskForm, item: Entity) -> None:
    system_links = {
        # Can't use isinstance for class check here
        link_.domain.id: link_ for link_ in item.get_links('P67', True)
        if link_.domain.class_.name == 'reference_system'}
    for field in form:
        if field.id.startswith('reference_system_id_'):
            system_id = int(field.id.replace('reference_system_id_', ''))
            if system_id in system_links:
                field.data = system_links[system_id].description
                precision_field = getattr(
                    form,
                    f'reference_system_precision_{system_id}')
                precision_field.data = str(system_links[system_id].type.id)


def populate_dates(form: FlaskForm, item: Union['Entity', Link]) -> None:
    if item.begin_from:
        form.begin_year_from.data = format_date_part(item.begin_from, 'year')
        form.begin_month_from.data = format_date_part(item.begin_from, 'month')
        form.begin_day_from.data = format_date_part(item.begin_from, 'day')
        form.begin_comment.data = item.begin_comment
        if item.begin_to:
            form.begin_year_to.data = format_date_part(item.begin_to, 'year')
            form.begin_month_to.data = format_date_part(item.begin_to, 'month')
            form.begin_day_to.data = format_date_part(item.begin_to, 'day')
    if item.end_from:
        form.end_year_from.data = format_date_part(item.end_from, 'year')
        form.end_month_from.data = format_date_part(item.end_from, 'month')
        form.end_day_from.data = format_date_part(item.end_from, 'day')
        form.end_comment.data = item.end_comment
        if item.end_to:
            form.end_year_to.data = format_date_part(item.end_to, 'year')
            form.end_month_to.data = format_date_part(item.end_to, 'month')
            form.end_day_to.data = format_date_part(item.end_to, 'day')
