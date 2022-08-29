from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING, Union

import numpy
from flask import g, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField

from openatlas import app
from openatlas.forms.setting import ProfileForm
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.util.table import Table
from openatlas.util.util import get_base_table_data, get_file_extension, \
    uc_first

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
        label = uc_first(field.label.text)
        if profile and field.name in current_user.settings:
            value = current_user.settings[field.name]
        elif field.name in g.settings:
            value = g.settings[field.name]
        else:  # pragma: no cover
            value = ''  # In case of a missing setting after an update
        if field.type in ['StringField', 'IntegerField']:
            settings[label] = value
        if field.type == 'BooleanField':  # str() needed for templates
            settings[label] = str(_('on')) if value else str(_('off'))
        if field.type == 'SelectField':
            if isinstance(value, str) and value.isdigit():
                value = int(value)
            settings[label] = dict(field.choices).get(value)
        if field.name in [
                'mail_recipients_feedback',
                'file_upload_allowed_extension']:
            settings[label] = ' '.join(value)
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
            field.data = ' '.join(g.settings[field.name])
            continue
        if field.name not in g.settings:  # pragma: no cover
            field.data = ''  # In case of a missing setting after an update
            continue
        field.data = g.settings[field.name]


def populate_insert_form(
        form: FlaskForm,
        class_: str,
        origin: Union[Entity, Type, None]) -> None:
    if hasattr(form, 'alias'):
        form.alias.append_entry('')
    if not origin:
        return
    view = g.classes[class_].view
    if view == 'actor' and origin.class_.name == 'place':
        form.residence.data = origin.id
    if view == 'artifact' and origin.class_.view == 'actor':
        form.actor.data = origin.id
    if view == 'event':
        if origin.class_.view == 'artifact':
            form.artifact.data = [origin.id]
        elif origin.class_.view in ['artifact', 'place']:
            if class_ == 'move':
                form.place_from.data = origin.id
            else:
                form.place.data = origin.id
    if view == 'source' and origin.class_.name == 'artifact':
        form.artifact.data = [origin.id]
    if view == 'type' and isinstance(origin, Type):
        root_id = origin.root[0] if origin.root else origin.id
        getattr(form, str(root_id)).data = origin.id \
            if origin.id != root_id else None


def was_modified(form: FlaskForm, entity: Entity) -> bool:  # pragma: no cover
    if not entity.modified or not form.opened.data:
        return False
    if entity.modified < datetime.fromtimestamp(float(form.opened.data)):
        return False
    g.logger.log('info', 'multi user', 'Multi user overwrite prevented.')
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
    term = StringField('', render_kw={"placeholder": _('search term')})


@app.context_processor
def inject_template_functions() -> dict[str, Union[str, GlobalSearchForm]]:
    def get_logo() -> str:
        if g.settings['logo_file_id']:
            ext = get_file_extension(int(g.settings['logo_file_id']))
            if ext != 'N/A':
                return url_for(
                    'display_logo',
                    filename=f"{g.settings['logo_file_id']}{ext}")
        return str(Path('/static') / 'images' / 'layout' / 'logo.png')

    return dict(
        get_logo=get_logo(),
        search_form=GlobalSearchForm(prefix='global'))


def check_if_entity_has_time(
        entity: Optional[Union[Entity, Link, Type]]
) -> bool:   # pragma: no cover
    if not entity:
        return False
    for item in [
            entity.begin_from,
            entity.begin_to,
            entity.end_from,
            entity.end_to]:
        if '00:00:00' not in str(item) and item:
            return True
    return False


def get_table_content(
        class_name: str,
        selected_data: Any,
        filter_ids: Optional[list[int]] = None) -> tuple[Table, str]:
    filter_ids = filter_ids or []
    selection = ''
    if class_name in ('cidoc_domain', 'cidoc_property', 'cidoc_range'):
        table = Table(
            ['code', 'name'],
            defs=[
                {'orderDataType': 'cidoc-model', 'targets': [0]},
                {'sType': 'numeric', 'targets': [0]}])
        for id_, entity in (
          g.properties if class_name == 'cidoc_property'
          else g.cidoc_classes).items():
            onclick = f'''
                onclick="selectFromTable(
                    this,
                    '{class_name}',
                    '{id_}',
                    '{entity.code} {entity.name}');"'''
            table.rows.append([
                f'<a href="#" {onclick}>{entity.code}</a>',
                entity.name])
    else:
        aliases = current_user.settings['table_show_aliases']
        if 'place' in class_name or class_name in \
                ['begins_in', 'ends_in', 'residence']:
            class_ = 'place'
            entities = Entity.get_by_view(
                'place',
                types=True,
                aliases=aliases)
        elif class_name == 'event_preceding':
            class_ = 'event'
            entities = Entity.get_by_class(
                ['activity', 'acquisition', 'move', 'production'],
                types=True,
                aliases=aliases)
        else:
            class_ = class_name
            entities = Entity.get_by_view(
                class_,
                types=True,
                aliases=aliases)
        table = Table(g.table_headers[class_])
        for entity in list(
          filter(lambda x: x.id not in filter_ids, entities)):
            if selected_data and entity.id == int(selected_data):
                selection = entity.name
            data = get_base_table_data(entity, show_links=False)
            data[0] = format_name_and_aliases(entity, class_name)
            table.rows.append(data)
    return table, selection


def format_name_and_aliases(entity: Entity, field_id: str) -> str:
    link = f"""<a href='#' onclick="selectFromTable(this,
        '{field_id}', {entity.id})">{entity.name}</a>"""
    if not entity.aliases:
        return link
    html = f'<p>{link}</p>'
    for i, alias in enumerate(entity.aliases.values()):
        html += alias if i else f'<p>{alias}</p>'
    return html
