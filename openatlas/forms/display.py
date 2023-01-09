from typing import Any, Optional

from flask import g, render_template
from flask_babel import lazy_gettext as _
from flask_login import current_user
from wtforms import Field, IntegerField, StringField, FileField
from wtforms.validators import Email

from openatlas import app
from openatlas.display.util import manual, tooltip, uc_first
from openatlas.models.type import Type
from openatlas.forms.field import ValueTypeField


def html_form(
        form: Any,
        form_id: Optional[str] = None,
        manual_page: Optional[str] = None) -> str:
    html = ''
    for field in form:
        if field.id.startswith('insert_'):
            continue  # These will be added in combination with other fields
        if isinstance(field, ValueTypeField):
            html += add_row(field, '', field, row_css=field.selectors)
            continue
        if field.type in ['CSRFTokenField', 'HiddenField']:
            html += str(field)
            continue
        if field.id.split('_', 1)[0] in ('begin', 'end'):
            if field.id == 'begin_year_from':
                html += add_dates(form)
            continue
        if field.type in ['TreeField', 'TreeMultiField']:
            type_ = g.types[int(field.type_id)]
            if not type_.subs:
                continue
            label = type_.name
            if type_.category == 'standard' and type_.name != 'License':
                label = uc_first(_('type'))
            if field.label.text == 'super':
                label = uc_first(_('super'))
            if field.flags.required and field.label.text:
                label += ' *'
            tooltip_ = ''
            if 'is_type_form' not in form:
                tooltip_ = type_.description or ''
                tooltip_ += "&#013;" + str(_('tooltip_required_type')) \
                    if field.flags.required \
                       and current_user.group == 'contributor' else ''
            html += add_row(field, label + tooltip(tooltip_))
            continue

        if field.id == 'save':
            field.label.text = uc_first(field.label.text)
            class_ = app.config['CSS']['button']['primary']
            buttons = []
            if manual_page:
                buttons.append(manual(manual_page))
            buttons.append(field(class_=class_))
            if 'insert_and_continue' in form:
                buttons.append(form.insert_and_continue(class_=class_))
            if 'insert_continue_sub' in form:
                buttons.append(form.insert_continue_sub(class_=class_))
            if 'insert_continue_human_remains' in form:
                buttons.append(
                    form.insert_continue_human_remains(class_=class_))
            html += add_row(
                field,
                '',  # Setting label to '' keeps the button row label empty
                f'<div class="toolbar text-wrap">{" ".join(buttons)}</div>')
            continue
        if field.type in ['TableField', 'TableMultiField']:
            field.label.text = _(field.label.text.lower())
        html += add_row(field, form_id=form_id)
    return html


def add_row(
        field: Field,
        label: Optional[str] = None,
        value: Optional[str] = None,
        form_id: Optional[str] = None,
        row_css: Optional[str] = '') -> str:
    field.label.text = uc_first(field.label.text)
    if field.flags.required and field.label.text and form_id != 'login-form':
        field.label.text += ' *'
    field_css = 'required' if field.flags.required else ''
    field_css += ' integer' if isinstance(field, IntegerField) else ''
    field_css += f' {app.config["CSS"]["string_field"]}' if isinstance(field, (StringField, FileField)) else ''

    for validator in field.validators:
        field_css += ' email' if isinstance(validator, Email) else ''
    return render_template(
        'forms/form_row.html',
        field=field,
        label=label,
        value=value,
        field_css=field_css,
        row_css=row_css)


def add_reference_systems(form: Any) -> str:
    html = ''
    switch_class = ''
    errors = False
    fields = []
    for field in form:
        if field.id.startswith('reference_system_id_'):
            fields.append(field)
            if field.errors:
                errors = True
    if len(fields) > 3 and not errors:
        switch_class = 'reference-system-switch'
        html = render_template('util/reference_system_switch.html')
    for field in fields:
        precision_field = getattr(form, field.id.replace('id_', 'precision_'))
        class_ = field.label.text \
            if field.label.text in ['GeoNames', 'Wikidata'] else ''
        html += add_row(
            field,
            field.label,
            f'{field(class_=class_)} {precision_field.label} '
            f'{precision_field}',
            row_css=f'external-reference {switch_class}')
    return html


def add_value_type(
        form: Any,
        type_: Type,
        root: Optional[Type] = None,
        level: int = 0) -> str:
    html = ''
    root = root or type_
    for sub_id in type_.subs:
        sub = g.types[sub_id]
        field = getattr(form, str(sub_id))
        html += f"""
        <div class="mt-2 table-row value-type-switch{type_.id}">
          <div></div>
          <div class="table-cell">
            <div class="d-flex">
              <div
                  class="d-flex justify-content-between"
                  style="width:16.15em;">
                <div class="ms-{level} position-relative text-wrap">
                  <div class="value-type-expander">{button_icon(sub)}</div>
                  {sub.name}
                </div>
                {field(class_='value-type')}
              </div>
              <span class="ms-1">{sub.description or ''}</span>
            </div>
            {add_value_type(form, sub, root, level + 1)}
          </div>
        </div>"""
    return html


def button_icon(type_: Type) -> str:
    if not type_.subs:
        return ''
    onclick = f'switch_value_type({type_.id})' if len(type_.subs) != 0 else ''
    return \
        f'<span id="value-type-switcher-{type_.id}" class="btn btn-xsm" ' \
        f'onclick="{onclick}"><i class="fa fa-chevron-right"></i></span>'


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
                errors[field_name] += uc_first(error)
            errors[field_name] = \
                f'<label class="error">{errors[field_name]}</label>'
    return render_template(
        'util/dates.html',
        form=form,
        errors=errors,
        style='' if valid_dates else 'display:table-row',
        label=_('hide')
        if form.begin_year_from.data or form.end_year_from.data else _('show'))
