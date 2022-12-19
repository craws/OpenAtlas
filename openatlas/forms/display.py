from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from flask import g, render_template
from flask_babel import lazy_gettext as _
from flask_login import current_user
from wtforms import Field, IntegerField
from wtforms.validators import Email

from openatlas import app
from openatlas.forms.field import ValueFloatField, ValueTypeField
from openatlas.forms.util import value_type_expand_icon
from openatlas.util.util import manual, tooltip, uc_first

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.type import Type


def html_form(
        form: Any,
        form_id: Optional[str] = None,
        manual_page: Optional[str] = None) -> str:
    html = ''
    for field in form:
        if isinstance(field, ValueTypeField):
            html += f'''
                <div class="row">
                  <div  class="col-sm-auto mr-1 text-sm-end" style="min-width: 160px"></div>
                  <div class = col>
                    {field()}
                  </div>
                </div>'''
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
                continue  # pragma: no cover
            label = type_.name
            if type_.category == 'standard' and type_.name != 'License':
                label = uc_first(_('type'))
            if field.label.text == 'super':
                label = uc_first(_('super'))
            if type_.category == 'value' and 'is_type_form' not in form:
                field.description = type_.description
                html += add_row(field, label, value_type_expand_icon(type_))
                #html += add_value_type(form, type_)
                continue
            if field.flags.required and field.label.text:
                label += ' *'
            tooltip_ = ''
            if 'is_type_form' not in form:  # pragma: no cover
                tooltip_ = type_.description or ''
                if field.flags.required \
                        and current_user.group == 'contributor':
                    tooltip_ += "&#013;" + str(_('tooltip_required_type'))
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
    for validator in field.validators:
        field_css += ' email' if isinstance(validator, Email) else ''
    return render_template(
        'forms/form_row.html',
        field=field,
        label=label,
        value=value,
        field_css=field_css,
        row_css=row_css)


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
                  <div class="value-type-expander">{value_type_expand_icon(sub)}</div>
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
