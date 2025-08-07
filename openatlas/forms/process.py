import ast
from typing import Any

from flask import g
from werkzeug.exceptions import abort

from openatlas.display.util2 import datetime64_to_timestamp, sanitize
from openatlas.forms.util import form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem


def process_standard_fields(manager: Any) -> None:
    for key, value in manager.form.data.items():
        field_type = getattr(manager.form, key).type
        if field_type in [
                'TreeField',
                'TreeMultiField',
                'TableField',
                'TableMultiField']:
            if value:
                ids = ast.literal_eval(value)
                value = ids if isinstance(ids, list) else [int(ids)]
            else:
                value = []
        if key.startswith((
                'begin_',
                'end_',
                'name_inverse',
                'multiple',
                'page',
                'reference_system_precision_',
                'website_url',
                'resolver_url',
                'placeholder',
                'classes',
                'inverse',
                'creator',
                'license_holder',)) \
                or field_type in [
                    'CSRFTokenField',
                    'HiddenField',
                    'MultipleFileField',
                    'DragNDropField',
                    'SelectField',
                    'SelectMultipleField',
                    'SubmitSourceField',
                    'SubmitField',
                    'TableField',
                    'TableMultiField',
                    'ValueTypeRootField']:
            continue
        if key == 'name':
            name = manager.form.data['name']
            if hasattr(manager.form, 'name_inverse'):
                name = manager.form.name.data.replace(
                    '(', '').replace(')', '').strip()
                if manager.form.name_inverse.data.strip():
                    inverse = manager.form.name_inverse.data. \
                        replace('(', ''). \
                        replace(')', '').strip()
                    name += f' ({inverse})'
            if isinstance(manager.entity, ReferenceSystem) \
                    and manager.entity.system:
                name = manager.entity.name  # Prevent changing a system name
            manager.data['attributes']['name'] = name
        elif key == 'alias':
            manager.data['aliases'] = value
        elif field_type == 'ValueTypeField':
            if value is not None:  # Allow the number zero
                manager.add_link('P2', g.types[int(key)], value)
        elif key == 'public':
            manager.data['file_info'] = {
                'public': bool(manager.form.public.data),
                'creator': sanitize(manager.form.creator.data),
                'license_holder': sanitize(manager.form.license_holder.data)}
        else:  # pragma: no cover
            abort(418, f'Form error: {key}, {field_type}, value={value}')


def process_origin(manager: Any) -> None:
    if not manager.entity:
        return
    if manager.origin.class_.group['name'] == 'reference':
        if manager.entity.class_.group['name'] == 'file':
            manager.add_link(
                'P67',
                manager.origin,
                manager.form.page.data,
                inverse=True)
        else:
            manager.add_link(
                'P67',
                manager.origin,
                inverse=True,
                return_link_id=True)
    elif manager.entity.class_.group['name'] == 'file' \
            or (manager.entity.class_.group['name'] in ['reference', 'source']
                and manager.origin.class_.name != 'file'):
        manager.add_link(
            'P67',
            manager.origin,
            return_link_id=bool(manager.entity.class_.group['name'] == 'reference'))
    elif manager.origin.class_.name == 'source' \
            and manager.entity.class_.name != 'source_translation':
        manager.add_link('P67', manager.origin, inverse=True)
    elif manager.origin.class_.name == 'file':
        if manager.entity.class_.group['name'] == 'reference':
            manager.add_link(
                'P67',
                manager.origin,
                return_link_id=True)
        elif manager.entity.class_.name != 'creation':
            manager.add_link('P67', manager.origin, inverse=True)


def process_date(form: Any, entity: Entity) -> dict[str, Any]:
    data: dict[str, Any] = {
        'begin_from': None,
        'begin_to': None,
        'begin_comment': None,
        'end_from': None,
        'end_to': None,
        'end_comment': None}
    if hasattr(form, 'begin_year_from') and form.begin_year_from.data:
        data['begin_comment'] = form.begin_comment.data
        data['begin_from'] = form_to_datetime64(
            form.begin_year_from.data,
            form.begin_month_from.data,
            form.begin_day_from.data,
            form.begin_hour_from.data if 'begin_hour_from' in form else None,
            form.begin_minute_from.data if 'begin_hour_from' in form else None,
            form.begin_second_from.data if 'begin_hour_from' in form else None)
        data['begin_to'] = form_to_datetime64(
            form.begin_year_to.data or (
                form.begin_year_from.data if not
                form.begin_day_from.data else None),
            form.begin_month_to.data or (
                form.begin_month_from.data if not
                form.begin_day_from.data else None),
            form.begin_day_to.data,
            form.begin_hour_to.data if 'begin_hour_from' in form else None,
            form.begin_minute_to.data if 'begin_hour_from' in form else None,
            form.begin_second_to.data if 'begin_hour_from' in form else None,
            to_date=True)
    if hasattr(form, 'end_year_from') and form.end_year_from.data:
        data['end_comment'] = form.end_comment.data
        data['end_from'] = form_to_datetime64(
            form.end_year_from.data,
            form.end_month_from.data,
            form.end_day_from.data,
            form.end_hour_from.data if 'end_hour_from' in form else None,
            form.end_minute_from.data if 'end_hour_from' in form else None,
            form.end_second_from.data if 'end_hour_from' in form else None)
        data['end_to'] = form_to_datetime64(
            form.end_year_to.data or
            (form.end_year_from.data if not form.end_day_from.data else None),
            form.end_month_to.data or
            (form.end_month_from.data if not form.end_day_from.data else None),
            form.end_day_to.data,
            form.end_hour_to.data if 'end_hour_from' in form else None,
            form.end_minute_to.data if 'end_hour_from' in form else None,
            form.end_second_to.data if 'end_hour_from' in form else None,
            to_date=True)
    return {
        'begin_from': datetime64_to_timestamp(data['begin_from']),
        'begin_to':  datetime64_to_timestamp(data['begin_to']),
        'begin_comment': data['begin_comment'],
        'end_from':  datetime64_to_timestamp(data['end_from']),
        'end_to':  datetime64_to_timestamp(data['end_to']),
        'end_comment': data['end_comment']}
