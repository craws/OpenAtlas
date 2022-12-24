import ast
from typing import Any

from flask import g
from werkzeug.exceptions import abort

from openatlas.forms.util import form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.util import sanitize


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
                'inverse')) \
                or field_type in [
                    'CSRFTokenField',
                    'HiddenField',
                    'MultipleFileField',
                    'DragNDropField',
                    'SelectField',
                    'SelectMultipleField',
                    'SubmitField',
                    'TableField',
                    'TableMultiField']:
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
            if manager.entity.class_.name == 'type':
                name = sanitize(name, 'text')
            elif isinstance(manager.entity, ReferenceSystem) \
                    and manager.entity.system:
                name = manager.entity.name  # Prevent changing a system name
            manager.data['attributes']['name'] = name
        elif key == 'description':
            manager.data['attributes'][key] = manager.form.data[key]
        elif key == 'alias':
            manager.data['aliases'] = value
        elif field_type in ['TreeField', 'TreeMultiField']:
            if manager.class_.name in \
                    ['actor_function', 'actor_relation', 'involvement']:
                continue
            if g.types[int(getattr(manager.form, key).id)].class_.name \
                    == 'administrative_unit':
                if 'administrative_units' not in manager.data:
                    manager.data['administrative_units'] = []
                manager.data['administrative_units'] += value
            elif not manager.entity or manager.entity.class_.view != 'type':
                manager.data['links']['delete'].add('P2')
                manager.add_link('P2', [g.types[id_] for id_ in value])
        elif field_type == 'ValueFloatField':
            if value is not None:  # Allow the number zero
                manager.add_link('P2', g.types[int(key)], value)
        elif key.startswith('reference_system_id_'):
            system = Entity.get_by_id(
                int(key.replace('reference_system_id_', '')))
            precision_field = getattr(
                manager.form,
                key.replace('id_', 'precision_'))
            manager.data['links']['delete_reference_system'] = True
            if value:
                manager.add_link(
                    'P67',
                    system,
                    value,
                    inverse=True,
                    type_id=precision_field.data)
        else:
            abort(418, f'Form error: {key}, {field_type}, value={value}')


def process_origin(manager: Any) -> None:
    if not manager.entity:
        return
    if manager.origin.class_.view == 'reference':
        if manager.entity.class_.name == 'file':
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
    elif manager.entity.class_.name == 'file' \
            or (manager.entity.class_.view in ['reference', 'source']
                and manager.origin.class_.name != 'file'):
        manager.add_link(
            'P67',
            manager.origin,
            return_link_id=bool(manager.entity.class_.view == 'reference'))
    elif manager.origin.class_.view in ['source', 'file'] \
            and manager.entity.class_.name != 'source_translation':
        manager.add_link('P67', manager.origin, inverse=True)
    return


def process_dates(manager: Any) -> dict[str, Any]:
    data = {
        'begin_from': None, 'begin_to': None, 'begin_comment': None,
        'end_from': None, 'end_to': None, 'end_comment': None}
    form = manager.form
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
            form.begin_year_to.data,
            form.begin_month_to.data,
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
            form.end_hour_from.data if 'begin_hour_from' in form else None,
            form.end_minute_from.data if 'begin_hour_from' in form else None,
            form.end_second_from.data if 'begin_hour_from' in form else None)
        data['end_to'] = form_to_datetime64(
            form.end_year_to.data,
            form.end_month_to.data,
            form.end_day_to.data,
            form.end_hour_to.data if 'begin_hour_from' in form else None,
            form.end_minute_to.data if 'begin_hour_from' in form else None,
            form.end_second_to.data if 'begin_hour_from' in form else None,
            to_date=True)
    return data
