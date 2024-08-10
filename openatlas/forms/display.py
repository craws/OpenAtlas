from __future__ import annotations

from typing import Any, Optional

from flask import g, render_template
from flask_babel import lazy_gettext as _
from wtforms import Field, FileField, IntegerField, SelectField, StringField
from wtforms.validators import Email

from openatlas import app
from openatlas.display.util2 import manual
from openatlas.forms.field import ValueTypeField


def html_form(
        form: Any,
        form_id: Optional[str] = None,
        manual_page: Optional[str] = None) -> str:
    html = ''
    reference_systems_added = False
    reference_systems_fields = list(
        filter(lambda x: x.id.startswith('reference_system_id_'), form))
    reference_systems_fields_errors = \
        any(f.errors for f in reference_systems_fields)
    for field in form:
        if field.id.startswith('insert_'):
            continue  # These will be added in combination with other fields
        if isinstance(field, ValueTypeField):
            html += add_row(field, '', field(), row_css=field.selectors)
            continue
        if field.type in ['CSRFTokenField', 'HiddenField']:
            html += f' {field}'
            continue
        if field.type in ['CustomField']:
            html += add_row(field, value=field.content)
            continue
        if field.id.startswith("reference_system") \
                and len(reference_systems_fields) > 3 \
                and not reference_systems_fields_errors:
            if not reference_systems_added:
                reference_systems_added = True
                html += add_row(
                    None,
                    _('reference system'),
                    '<span id="reference-system-switcher" class="uc-first '
                    f'{app.config["CSS"]["button"]["secondary"]}">'
                    + _('show') + '</span>')
            html += add_row(field, row_css="d-none")
            continue
        if field.id.split('_', 1)[0] in ('begin', 'end'):
            if field.id == 'begin_year_from':
                html += add_dates(form)
            continue
        if field.type in ['TreeField', 'TreeMultiField', 'ValueTypeRootField']:
            type_ = g.types[int(field.type_id)]
            if not type_.subs:
                continue
            label = type_.name
            if type_.category == 'standard' and type_.name != 'License':
                label = _('type')
            if field.label.text == 'super':
                label = _('super')
            if field.flags.required and field.label.text:
                label += ' *'
            if not hasattr(field, 'is_type_form') or not field.is_type_form:
                field.description = type_.description
            html += add_row(field, label)
            continue
        if field.id == 'save':
            class_ = \
                f"{app.config['CSS']['button']['primary']} text-wrap uc-first"
            buttons = [manual(manual_page)] if manual_page else []
            buttons.append(field(class_=class_))
            if 'insert_and_continue' in form:
                buttons.append(form.insert_and_continue(class_=class_))
            if 'insert_continue_sub' in form:
                buttons.append(form.insert_continue_sub(class_=class_))
            if 'insert_continue_human_remains' in form:
                buttons.append(
                    form.insert_continue_human_remains(class_=class_))
            buttons = list(
                map(lambda x: f'<div class="col-auto">{x}</div>', buttons))
            html += add_row(
                field,
                '',  # Setting label to '' to keep button row label empty
                '<div class="row g-1 align-items-center ">'
                f'{"".join(buttons)}</div>')
            continue
        if field.type in ['TableField', 'TableMultiField']:
            field.label.text = _(field.label.text.lower())
        html += add_row(field, form_id=form_id)
    return html


def add_row(
        field: Optional[Field],
        label: Optional[str] = None,
        value: Optional[str] = None,
        form_id: Optional[str] = None,
        row_css: Optional[str] = None) -> str:
    row_css = row_css or ''
    field_css = ''
    if field and field.render_kw and 'class' in field.render_kw:
        field_css = field.render_kw['class']
    if field:
        if field.flags.required \
                and field.label.text \
                and form_id != 'login-form':
            field.label.text += ' *'
        field_css += ' required' if field.flags.required else ''
        field_css += ' integer' if isinstance(field, IntegerField) else ''
        field_css += f' {app.config["CSS"]["string_field"]}' \
            if isinstance(
                field,
                (StringField, SelectField, FileField, IntegerField)) else ''
        row_css += f' {field.row_css if hasattr(field, "row_css") else ""}'
        for validator in field.validators:
            field_css += ' email' if isinstance(validator, Email) else ''
    return render_template(
        'forms/form_row.html',
        field=field,
        label=label,
        value=value,
        field_css=field_css.strip(),
        row_css=row_css)


def add_dates(form: Any) -> str:
    errors = {}
    valid_dates = True
    date_name = [
        'begin_year_from', 'begin_month_from', 'begin_day_from',
        'begin_year_to', 'begin_month_to', 'begin_day_to',
        'end_year_from', 'end_month_from', 'end_day_from',
        'end_year_to', 'end_month_to', 'end_day_to']
    if 'begin_hour_from' in form:
        date_name += [
            'begin_hour_from', 'begin_minute_from', 'begin_second_from',
            'begin_hour_to', 'begin_minute_to', 'begin_second_to',
            'end_hour_from', 'end_minute_from', 'end_second_from',
            'end_hour_to', 'end_minute_to', 'end_second_to']
    for field_name in date_name:
        errors[field_name] = ''
        if getattr(form, field_name).errors:
            valid_dates = False
            errors[field_name] = ''
            for error in getattr(form, field_name).errors:
                errors[field_name] += error
            errors[field_name] = \
                f'<label class="error uc-first">{errors[field_name]}</label>'
    return render_template(
        'util/dates.html',
        form=form,
        errors=errors,
        style='' if valid_dates else 'display:table-row',
        label=_('hide')
        if form.begin_year_from.data or form.end_year_from.data else _('show'))


@app.template_filter()
def display_form(
        form: Any,
        form_id: Optional[str] = None,
        manual_page: Optional[str] = None) -> str:
    form_id = f'id="{form_id}"' if form_id else ''
    multipart = 'enctype="multipart/form-data"' if 'file' in form else ''
    return \
        f'<form method="post" {form_id} {multipart}>' \
        '<table class="table table-no-style">' \
        f'{html_form(form, form_id, manual_page)}' \
        f'</table></form>'
