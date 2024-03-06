from __future__ import annotations

import ast
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING

import numpy
from flask import g, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField

from openatlas import app
from openatlas.display.table import Table
from openatlas.display.util import \
    get_base_table_data, get_file_path
from openatlas.forms.field import format_name_and_aliases
from openatlas.forms.setting import ProfileForm
from openatlas.models.entity import Entity

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.link import Link


def get_form_settings(form: Any, profile: bool = False) -> dict[str, str]:
    if isinstance(form, ProfileForm):
        return {
            _('name'): current_user.real_name,
            _('email'): current_user.email,
            _('show email'): str(
                _('on') if current_user.settings['show_email'] else _('off')),
            _('newsletter'): str(
                _('on') if current_user.settings['newsletter'] else _('off'))}
    settings = {}
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue
        if profile and field.name in current_user.settings:
            value = current_user.settings[field.name]
        elif field.name in g.settings:
            value = g.settings[field.name]
        else:
            value = ''  # pragma: no cover - if missing setting after an update
        if field.type in ['StringField', 'IntegerField']:
            settings[field.label.text] = value
        if field.type == 'BooleanField':
            settings[field.label.text] = str(_('on') if value else _('off'))
        if field.type == 'SelectField':
            if isinstance(value, str) and value.isdigit():
                value = int(value)
            settings[field.label.text] = dict(field.choices).get(value)
        if field.name in [
                'mail_recipients_feedback',
                'file_upload_allowed_extension']:
            settings[field.label.text] = '<br>'.join(value)
    return settings


def string_to_entity_list(string: str) -> list[Entity]:
    ids = ast.literal_eval(string)
    ids = [int(id_) for id_ in ids] if isinstance(ids, list) else [int(ids)]
    return Entity.get_by_ids(ids)


def set_form_settings(form: Any, profile: bool = False) -> None:
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue
        if profile and field.name == 'name':
            field.data = current_user.real_name
            continue
        if profile and field.name == 'email':
            field.data = current_user.email
            continue
        if profile and field.name in current_user.settings:
            field.data = current_user.settings[field.name]
            continue
        if field.name in ['log_level']:
            field.data = int(g.settings[field.name])
            continue
        if field.name in [
                'mail_recipients_feedback',
                'file_upload_allowed_extension']:
            for item in g.settings[field.name]:
                field.append_entry(item)
            continue
        if field.name not in g.settings:  # pragma: no cover
            field.data = ''  # If missing setting after an update
            continue
        field.data = g.settings[field.name]


def was_modified(form: Any, entity: Entity) -> bool:
    if not entity.modified or not form.opened.data:
        return False
    if entity.modified < datetime.fromtimestamp(
            float(form.opened.data)):
        return False
    g.logger.log('info', 'multi user', 'Overwrite denied')
    return True


def form_to_datetime64(
        year: Any,
        month: Any,
        day: Any,
        hour: Optional[Any] = None,
        minute: Optional[Any] = None,
        second: Optional[Any] = None,
        to_date: bool = False) -> Optional[numpy.datetime64]:
    if not year:
        return None
    year = year if year > 0 else year + 1

    def is_leap_year(year_: int) -> bool:
        if year_ % 400 == 0:  # e.g. 2000
            return True
        if year_ % 100 == 0:  # e.g. 1000
            return False
        if year_ % 4 == 0:  # e.g. 1996
            return True
        return False

    def get_last_day_of_month(year_: int, month_: int) -> int:
        months_days: dict[int, int] = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
            10: 31, 11: 30, 12: 31}
        months_days_leap: dict[int, int] = {
            1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
            10: 31, 11: 30, 12: 31}
        date_lookup = months_days_leap \
            if is_leap_year(year_) else months_days
        return date_lookup[month_]

    if month:
        month = f'{month:02}'
    elif to_date:
        month = '12'
    else:
        month = '01'

    if day:
        day = f'{day:02}'
    elif to_date:
        day = f'{get_last_day_of_month(int(year), int(month)):02}'
    else:
        day = '01'

    hour = f'{hour:02}' if hour else '00'
    minute = f'{minute:02}' if minute else '00'
    second = f'{second:02}' if second else '00'
    try:
        date_time = numpy.datetime64(
            f'{year}-{month}-{day}T{hour}:{minute}:{second}')
    except ValueError:
        return None
    return date_time


class GlobalSearchForm(FlaskForm):
    term = StringField('')


@app.context_processor
def inject_template_functions() -> dict[str, str | GlobalSearchForm]:
    def get_logo() -> str:
        if g.settings['logo_file_id']:
            if path := get_file_path(int(g.settings['logo_file_id'])):
                return url_for(
                    'display_logo',
                    filename=f"{g.settings['logo_file_id']}{path.suffix}")
        return str(Path('/static') / 'images' / 'layout' / 'logo.png')
    return {
        'get_logo': get_logo(),
        'search_form': GlobalSearchForm(prefix='global')}


def check_if_entity_has_time(item: Entity | Link) -> bool:
    for date_ in [item.begin_from, item.begin_to, item.end_from, item.end_to]:
        if date_ and '00:00:00' not in str(date_):
            return True
    return False


def table(
        table_id: str,
        class_name: str,
        entities: list[Entity],
        filter_ids: Optional[list[int]] = None) -> Table:
    table_ = Table(g.table_headers[class_name])
    for entity in \
            [e for e in entities if not filter_ids or e.id not in filter_ids]:
        data = get_base_table_data(entity, show_links=False)
        data[0] = format_name_and_aliases(entity, table_id)
        table_.rows.append(data)
    return table_


def table_multi(
        entities: list[Entity],
        selected: Optional[dict[int, Entity]] = None,
        filter_ids: Optional[list[int]] = None) -> Table:
    table_ = Table(
        ['name', 'type', 'x'],
        order=[[2, "desc"], [0, "asc"]],
        defs=[{'orderDataType': 'dom-checkbox', 'targets': 2}])
    for e in [e for e in entities if not filter_ids or e.id not in filter_ids]:
        check = 'checked' if selected and e.id in list(selected.keys()) else ''
        table_.rows.append([
            e.name,
            # print_tags(e),
            f'<input id="{e.id}" value="{e.name}" '
            f'type="checkbox" {check} class="multi-table-select">'])
    return table_

    #@staticmethod
    #def get_table(
    #        class_name: str,
    #        entities: list[Entity],
    #        selected_data: Optional[Any] = None,
    #        filter_ids: Optional[list[int]] = None) -> Table:
    #    filter_ids = filter_ids or []
        # if class_name in ('cidoc_domain', 'cidoc_property', 'cidoc_range'):
        #     table = Table(
        #         ['code', 'name'],
        #         defs=[
        #             {'orderDataType': 'cidoc-model', 'targets': [0]},
        #             {'sType': 'numeric', 'targets': [0]}])
        #     for id_, entity in (
        #             g.properties if class_name == 'cidoc_property'
        #             else g.cidoc_classes).items():
        #         onclick = f'''
        #             onclick="selectFromTable(
        #                 this,
        #                 '{class_name}',
        #                 '{id_}',
        #                 '{entity.code} {entity.name}');"'''
        #         table.rows.append([
        #             f'<a href="#" {onclick}>{entity.code}</a>',
        #             entity.name])
        #         if entity.code == selected_data:
        #             selection = f'{entity.code} {entity.name}'
        # elif class_name == 'annotated_entity':
        #     # Hackish (mis)use of filter_ids to get table field for annotations
        #     table = Table(['name', 'class', 'description'])
        #     for item in Entity.get_by_id(filter_ids[0]).get_linked_entities(
        #             'P67'):
        #         if selected_data and item.id == int(selected_data):
        #             selection = item.name  # pragma: no cover
        #         table.rows.append([
        #             format_name_and_aliases(item, 'annotated_entity'),
        #             uc_first(item.class_.name),
        #             item.description])
        # else:
        #     aliases = current_user.settings['table_show_aliases']
        #     if 'place' in class_name or class_name in \
        #             ['begins_in', 'ends_in', 'residence']:
        #         class_ = 'place'
        #         entities = Entity.get_by_view('place', types=True,
        #                                       aliases=aliases)
        #     elif class_name == 'feature_super':
        #         class_ = 'place'
        #         entities = \
        #             Entity.get_by_class('place', types=True, aliases=aliases)
        #     elif class_name == 'stratigraphic_super':
        #         class_ = 'place'
        #         entities = \
        #             Entity.get_by_class('feature', types=True, aliases=aliases)
        #     elif class_name == 'artifact_super':
        #         class_ = 'place'
        #         entities = Entity.get_by_class(
        #             g.view_class_mapping['place'] + ['artifact'],
        #             types=True,
        #             aliases=aliases)
        #     elif class_name == 'human_remains_super':
        #         class_ = 'place'
        #         entities = Entity.get_by_class(
        #             g.view_class_mapping['place'] + ['human_remains'],
        #             types=True,
        #             aliases=aliases)
        #     else:
        #         class_ = class_name
        #         entities = Entity.get_by_view(
        #             class_,
        #             types=True,
        #             aliases=aliases)
        #table = Table(g.table_headers[class_name])
        #for entity in [e for e in entities if e.id not in filter_ids]:
        #    data = get_base_table_data(entity, show_links=False)
        #    data[0] = format_name_and_aliases(entity, class_name)
        #    table.rows.append(data)
        #return table


# class TableMultiSelect(HiddenInput):
#
#     def __call__(self, field: TableMultiField, **kwargs: Any) -> str:
#
#         data = field.data or []
#         data = ast.literal_eval(data) if isinstance(data, str) else data
#         aliases = current_user.settings['table_show_aliases']
#         if class_ in ['group', 'person']:
#             entities = Entity.get_by_class(class_, types=True, aliases=aliases)
#         else:
#             entities = Entity.get_by_view(class_, types=True, aliases=aliases)
#         table = Table(
#             [''] + g.table_headers[class_],
#             order=[[0, 'desc'], [1, 'asc']],
#             defs=[{'orderDataType': 'dom-checkbox', 'targets': 0}])
#         for entity in [e for e in entities if e.id not in field.filter_ids]:
#             row = get_base_table_data(entity, show_links=False)
#             row.insert(
#                 0,
#                 f'<input type="checkbox" value="{entity.name}"'
#                 f' id="{entity.id}" '
#                 f'{" checked" if entity.id in data else ""}>')
#             table.rows.append(row)
#         return Markup(render_template(
#             'forms/table_multi_select.html',
#             field=field,
#             selection=[e for e in entities if e.id in data],
#             table=table)) + super().__call__(field, **kwargs)
