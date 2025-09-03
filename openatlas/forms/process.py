import ast
from typing import Any

from flask import g
from werkzeug.exceptions import abort

from openatlas.display.util2 import sanitize
from openatlas.models.dates import Dates, form_to_datetime64
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


def process_dates(form: Any) -> dict[str, Any]:
    dates = Dates({})
    if hasattr(form, 'begin_year_from') and form.begin_year_from.data:
        dates.begin_comment = form.begin_comment.data
        dates.begin_from = form_to_datetime64(
            form.begin_year_from.data,
            form.begin_month_from.data,
            form.begin_day_from.data,
            form.begin_hour_from.data if 'begin_hour_from' in form else None,
            form.begin_minute_from.data if 'begin_hour_from' in form else None,
            form.begin_second_from.data if 'begin_hour_from' in form else None)
        dates.begin_to = form_to_datetime64(
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
        dates.end_comment = form.end_comment.data
        dates.end_from = form_to_datetime64(
            form.end_year_from.data,
            form.end_month_from.data,
            form.end_day_from.data,
            form.end_hour_from.data if 'end_hour_from' in form else None,
            form.end_minute_from.data if 'end_hour_from' in form else None,
            form.end_second_from.data if 'end_hour_from' in form else None)
        dates.end_to = form_to_datetime64(
            form.end_year_to.data or
            (form.end_year_from.data if not form.end_day_from.data else None),
            form.end_month_to.data or
            (form.end_month_from.data if not form.end_day_from.data else None),
            form.end_day_to.data,
            form.end_hour_to.data if 'end_hour_from' in form else None,
            form.end_minute_to.data if 'end_hour_from' in form else None,
            form.end_second_to.data if 'end_hour_from' in form else None,
            to_date=True)
    return dates.to_timestamp()
