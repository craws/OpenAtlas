from __future__ import annotations  # Needed for Python 4.0 type annotations

import math
import os
import re
import smtplib
from collections import defaultdict
from datetime import datetime, timedelta
from email.header import Header
from email.mime.text import MIMEText
from functools import wraps
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING, Union

import numpy
from bcrypt import hashpw
from flask import flash, g, render_template, request, url_for
from flask_babel import LazyString, lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from jinja2 import contextfilter
from markupsafe import Markup, escape
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from wtforms import Field, IntegerField
from wtforms.validators import Email

from openatlas import app, logger
from openatlas.models.cidoc_class import CidocClass
from openatlas.models.cidoc_property import CidocProperty
from openatlas.models.content import get_translation
from openatlas.models.imports import Project
from openatlas.util.image_processing import check_processed_image

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity
    from openatlas.models.link import Link
    from openatlas.models.type import Type


@app.template_filter()
def bookmark_toggle(entity_id: int, for_table: bool = False) -> str:
    label = uc_first(
        _('bookmark remove')
        if entity_id in current_user.bookmarks else _('bookmark'))
    onclick = f"ajaxBookmark('{entity_id}');"
    if for_table:
        return \
            f'<a href="#" id="bookmark{entity_id}" onclick="{onclick}">' \
            f'{label}</a>'
    return button(label, id_=f'bookmark{entity_id}', onclick=onclick)


@app.template_filter()
def display_external_references(entity: Entity) -> str:
    return Markup(
        render_template('util/external_references.html', entity=entity))


@app.template_filter()
def display_menu(entity: Optional[Entity], origin: Optional[Entity]) -> str:
    view_name = ''
    if entity:
        view_name = entity.class_.view
    if origin:
        view_name = origin.class_.view
    html = ''
    for item in [
            'source', 'event', 'actor', 'place', 'artifact', 'reference',
            'type']:
        active = ''
        request_parts = request.path.split('/')
        if (view_name == item) or request.path.startswith('/index/' + item):
            active = 'active'
        elif len(request_parts) > 2 and request.path.startswith('/insert/'):
            name = request_parts[2]
            if name in g.class_view_mapping \
                    and g.class_view_mapping[name] == item:
                active = 'active'
        if item == 'type':
            html += \
                f'<a href="{url_for("type_index")}" ' \
                f'class="nav-item nav-link {active}">{uc_first(_("types"))}</a>'
        else:
            html += \
                f'<a href="{url_for("index", view=item)}" ' \
                f'class="nav-item nav-link {active}">{uc_first(_(item))}</a>'
    return Markup(html)


@contextfilter
@app.template_filter()
def is_authorized(context: str, group: Optional[str] = None) -> bool:
    # Using context filter above to prevent Jinja2 context caching
    if not group:  # In case it wasn't called from a template
        group = context
    if not current_user.is_authenticated or not hasattr(current_user, 'group'):
        return False  # pragma: no cover - AnonymousUserMixin has no group
    if current_user.group == 'admin' \
            or current_user.group == group \
            or (current_user.group == 'manager'
                and group in ['editor', 'contributor', 'readonly']) \
            or (current_user.group == 'editor'
                and group in ['contributor', 'readonly']) \
            or (current_user.group == 'contributor' and group in ['readonly']):
        return True
    return False


@app.template_filter()
def sanitize(string: str, mode: Optional[str] = None) -> str:
    if not string:
        return ''
    if mode == 'type':  # Filter letters, numbers, minus, brackets and spaces
        return re.sub(r'([^\s\w()-]|_)+', '', string).strip()
    if mode == 'text':  # Remove HTML tags, keep linebreaks
        stripper = MLStripper()
        stripper.feed(string)
        return stripper.get_data().strip()
    return re.sub('[^A-Za-z0-9]+', '', string)  # Filter ASCII letters/numbers


@app.template_filter()
def test_file(file_name: str) -> Optional[str]:
    return file_name if (Path(app.root_path) / file_name).is_file() else None


def format_entity_date(
        entity: Union[Entity, Link],
        type_: str,  # begin or end
        object_: Optional[Entity] = None) -> str:
    html = link(object_) if object_ else ''
    if getattr(entity, f'{type_}_from'):
        html += ', ' if html else ''
        if getattr(entity, f'{type_}_to'):
            html += _(
                'between %(begin)s and %(end)s',
                begin=format_date(getattr(entity, f'{type_}_from')),
                end=format_date(getattr(entity, f'{type_}_to')))
        else:
            html += format_date(getattr(entity, f'{type_}_from'))
    comment = getattr(entity, f'{type_}_comment')
    return html + (f" ({comment})" if comment else '')


def format_name_and_aliases(entity: Entity, show_links: bool) -> str:
    name = link(entity) if show_links else entity.name
    if not entity.aliases or not current_user.settings['table_show_aliases']:
        return name
    return \
        f'<p>{name}</p>' \
        f'{"".join(f"<p>{alias}</p>" for alias in entity.aliases.values())}'


def get_backup_file_data() -> dict[str, Any]:
    path = app.config['EXPORT_DIR'] / 'sql'
    latest_file = None
    latest_file_date = None
    for file in [
            f for f in path.iterdir()
            if (path / f).is_file() and f.name != '.gitignore']:
        file_date = datetime.utcfromtimestamp((path / file).stat().st_ctime)
        if not latest_file_date or file_date > latest_file_date:
            latest_file = file
            latest_file_date = file_date
    file_data: dict[str, Any] = {'backup_too_old': True}
    if latest_file and latest_file_date:
        yesterday = datetime.today() - timedelta(days=1)
        file_data['file'] = latest_file.name
        file_data['backup_too_old'] = yesterday > latest_file_date
        file_data['size'] = convert_size(latest_file.stat().st_size)
        file_data['date'] = format_date(latest_file_date)
    return file_data


def get_base_table_data(entity: Entity, show_links: bool = True) -> list[Any]:
    data: list[Any] = [format_name_and_aliases(entity, show_links)]
    if entity.class_.view in ['actor', 'artifact', 'event', 'reference']:
        data.append(entity.class_.label)
    if entity.class_.standard_type_id:
        data.append(entity.standard_type.name if entity.standard_type else '')
    if entity.class_.name == 'file':
        data.append(
            g.file_stats[entity.id]['size']
            if entity.id in g.file_stats else 'N/A')
        data.append(
            g.file_stats[entity.id]['ext']
            if entity.id in g.file_stats else 'N/A')
    if entity.class_.view in ['actor', 'artifact', 'event', 'place']:
        data.append(entity.first)
        data.append(entity.last)
    data.append(entity.description)
    return data


def get_entity_data(
        entity: Entity,
        event_links: Optional[list[Link]] = None) -> dict[str, Any]:
    data: dict[str, Any] = {_('alias'): list(entity.aliases.values())}

    # Dates
    from_link = ''
    to_link = ''
    if entity.class_.name == 'move':  # Add places to the dates if it's a move
        if place_from := entity.get_linked_entity('P27'):
            from_link = \
                link(place_from.get_linked_entity_safe('P53', True)) + ' '
        if place_to := entity.get_linked_entity('P26'):
            to_link = link(place_to.get_linked_entity_safe('P53', True)) + ' '
    data[_('begin')] = from_link + format_entity_date(entity, 'begin')
    data[_('end')] = to_link + format_entity_date(entity, 'end')

    # Types
    if entity.standard_type:
        title = ' > '.join(
            [g.types[id_].name for id_ in entity.standard_type.root])
        data[_('type')] = \
            f'<span title="{title}">{link(entity.standard_type)}</span>'
    data.update(get_type_data(entity))

    # Class specific information
    from openatlas.models.type import Type
    from openatlas.models.reference_system import ReferenceSystem
    if isinstance(entity, Type):
        data[_('super')] = link(g.types[entity.root[-1]])
        if entity.category == 'value':
            data[_('unit')] = entity.description
        data[_('ID for imports')] = entity.id
    elif isinstance(entity, ReferenceSystem):
        data[_('website URL')] = external_url(entity.website_url)
        data[_('resolver URL')] = external_url(entity.resolver_url)
        data[_('example ID')] = entity.placeholder
    elif entity.class_.view == 'actor':
        begin_object = None
        if begin_place := entity.get_linked_entity('OA8'):
            begin_object = begin_place.get_linked_entity_safe('P53', True)
            entity.linked_places.append(begin_object)
        end_object = None
        if end_place := entity.get_linked_entity('OA9'):
            end_object = end_place.get_linked_entity_safe('P53', True)
            entity.linked_places.append(end_object)
        if residence := entity.get_linked_entity('P74'):
            residence_object = residence.get_linked_entity_safe('P53', True)
            entity.linked_places.append(residence_object)
            data[_('residence')] = link(residence_object)
        data[_('alias')] = list(entity.aliases.values())
        data[_('begin')] = format_entity_date(entity, 'begin', begin_object)
        data[_('end')] = format_entity_date(entity, 'end', end_object)
        if event_links:
            appears_first, appears_last = get_appearance(event_links)
            data[_('appears first')] = appears_first
            data[_('appears last')] = appears_last
    elif entity.class_.view == 'artifact':
        data[_('source')] = \
            [link(source) for source in entity.get_linked_entities('P128')]
        data[_('owned by')] = link(entity.get_linked_entity('P52'))
    elif entity.class_.view == 'event':
        data[_('sub event of')] = link(entity.get_linked_entity('P9'))
        data[_('preceding event')] = link(
            entity.get_linked_entity('P134', True))
        data[_('succeeding event')] = \
            '<br>'.join([link(e) for e in entity.get_linked_entities('P134')])
        if entity.class_.name == 'move':
            person_data = []
            artifact_data = []
            for linked_entity in entity.get_linked_entities('P25'):
                if linked_entity.class_.name == 'person':
                    person_data.append(linked_entity)
                elif linked_entity.class_.view == 'artifact':
                    artifact_data.append(linked_entity)
            data[_('person')] = [link(item) for item in person_data]
            data[_('artifact')] = [link(item) for item in artifact_data]
        else:
            if place := entity.get_linked_entity('P7'):
                data[_('location')] = link(
                    place.get_linked_entity_safe('P53', True))
        if entity.class_.name == 'acquisition':
            data[_('recipient')] = \
                [link(actor) for actor in entity.get_linked_entities('P22')]
            data[_('donor')] = \
                [link(donor) for donor in entity.get_linked_entities('P23')]
            data[_('given place')] = \
                [link(place) for place in entity.get_linked_entities('P24')]
        if entity.class_.name == 'production':
            data[_('produced')] = \
                [link(item) for item in entity.get_linked_entities('P108')]
    elif entity.class_.view == 'file':
        data[_('size')] = g.file_stats[entity.id]['size'] \
            if entity.id in g.file_stats else 'N/A'
        data[_('extension')] = g.file_stats[entity.id]['ext'] \
            if entity.id in g.file_stats else 'N/A'
    elif entity.class_.view == 'source':
        data[_('artifact')] = [
            link(artifact) for artifact in
            entity.get_linked_entities('P128', inverse=True)]
    if hasattr(current_user, 'settings'):
        data |= get_system_data(entity)
    return data


def required_group(group: str):  # type: ignore
    def wrapper(func):  # type: ignore
        @wraps(func)
        def wrapped(*args, **kwargs):  # type: ignore
            if not current_user.is_authenticated:
                return redirect(url_for('login', next=request.path))
            if not is_authorized(group):
                abort(403)
            return func(*args, **kwargs)

        return wrapped

    return wrapper


def send_mail(
        subject: str,
        text: str,
        recipients: Union[str, list[str]],
        log_body: bool = True) -> bool:  # pragma: no cover
    """
        Send one mail to every recipient.
        Set log_body to False for sensitive data, e.g. password mails
    """
    recipients = recipients if isinstance(recipients, list) else [recipients]
    if not g.settings['mail'] or not recipients:
        return False
    from_ = f"{g.settings['mail_from_name']} <{g.settings['mail_from_email']}>"
    try:
        with smtplib.SMTP(
                g.settings['mail_transport_host'],
                g.settings['mail_transport_port']) as smtp:
            smtp.starttls()
            if g.settings['mail_transport_username']:
                smtp.login(
                    g.settings['mail_transport_username'],
                    app.config['MAIL_PASSWORD'])
            for recipient in recipients:
                msg = MIMEText(text, _charset='utf-8')
                msg['From'] = from_
                msg['To'] = recipient.strip()
                msg['Subject'] = Header(subject.encode('utf-8'), 'utf-8')
                smtp.sendmail(
                    g.settings['mail_from_email'],
                    recipient, msg.as_string())
            log_text = \
                f'Mail from {from_} to {", ".join(recipients)} ' \
                f'Subject: {subject}'
            log_text += f' Content: {text}' if log_body else ''
            logger.log('info', 'mail', f'Mail send from {from_}', log_text)
    except smtplib.SMTPAuthenticationError as e:
        logger.log(
            'error',
            'mail',
            f"Error mail login for {g.settings['mail_transport_username']}", e)
        flash(_('error mail login'), 'error')
        return False
    except Exception as e:
        logger.log(
            'error',
            'mail',
            f"Error send mail for {g.settings['mail_transport_username']}", e)
        flash(_('error mail send'), 'error')
        return False
    return True


@contextfilter
@app.template_filter()
def system_warnings(_context: str, _unneeded_string: str) -> str:
    if not is_authorized('manager'):
        return ''
    warnings = []
    if app.config['DATABASE_VERSION'] != g.settings['database_version']:
        warnings.append(
            f"Database version {app.config['DATABASE_VERSION']} is needed but "
            f"current version is {g.settings['database_version']}")
    for path in app.config['WRITABLE_DIRS']:
        if not os.access(path, os.W_OK):
            warnings.append(
                f"{uc_first(_('directory not writable'))}: "
                f"{str(path).replace(app.root_path, '')}")
    if is_authorized('admin'):
        from openatlas.models.user import User
        user = User.get_by_username('OpenAtlas')
        if user and user.active:
            hash_ = hashpw(
                'change_me_PLEASE!'.encode('utf-8'),
                user.password.encode('utf-8'))
            if hash_ == user.password.encode('utf-8'):
                warnings.append(
                    "User OpenAtlas with default password is still active!")
    if warnings:
        return Markup(f'<p class="error">{"<br>".join(warnings)}<p>')
    return ''  # pragma: no cover


@app.template_filter()
def tooltip(text: str) -> str:
    if not text:
        return ''
    return """
        <span>
            <i class="fas fa-info-circle tooltipicon" title="{title}"></i>
        </span>""".format(title=text.replace('"', "'"))


def was_modified(form: FlaskForm, entity: Entity) -> bool:  # pragma: no cover
    if not entity.modified or not form.opened.data:
        return False
    if entity.modified < datetime.fromtimestamp(float(form.opened.data)):
        return False
    logger.log('info', 'multi user', 'Multi user overwrite prevented.')
    return True


def get_appearance(event_links: list[Link]) -> tuple[str, str]:
    # Get first/last appearance year from events for actors without begin/end
    first_year = None
    last_year = None
    first_string = ''
    last_string = ''
    for link_ in event_links:
        event = link_.domain
        actor = link_.range
        event_link = link(_('event'), url_for('view', id_=event.id))
        if not actor.first:
            if link_.first \
                    and (not first_year or int(link_.first) < int(first_year)):
                first_year = link_.first
                first_string = \
                    f"{format_entity_date(link_, 'begin', link_.object_)} " \
                    f"{_('at an')} {event_link}"
            elif event.first \
                    and (not first_year or int(event.first) < int(first_year)):
                first_year = event.first
                first_string = \
                    f"{format_entity_date(event, 'begin', link_.object_)}" \
                    f" {_('at an')} {event_link}"
        if not actor.last:
            if link_.last \
                    and (not last_year or int(link_.last) > int(last_year)):
                last_year = link_.last
                last_string = \
                    f"{format_entity_date(link_, 'end', link_.object_)} " \
                    f"{_('at an')} {event_link}"
            elif event.last \
                    and (not last_year or int(event.last) > int(last_year)):
                last_year = event.last
                last_string = \
                    f"{format_entity_date(event, 'end', link_.object_)} " \
                    f"{_('at an')} {event_link}"
    return first_string, last_string


def format_datetime(value: Any) -> str:
    return value.replace(microsecond=0).isoformat() if value else ''


def get_file_extension(entity: Union[int, Entity]) -> str:
    path = get_file_path(entity if isinstance(entity, int) else entity.id)
    return path.suffix if path else 'N/A'


def get_file_path(
        entity: Union[int, Entity],
        size: Optional[str] = None) -> Optional[Path]:
    id_ = entity if isinstance(entity, int) else entity.id
    if id_ not in g.file_stats:
        return None
    ext = g.file_stats[id_]['ext']
    if size:
        if ext in app.config['NONE_DISPLAY_EXT']:
            ext = app.config['PROCESSED_EXT']  # pragma: no cover
        path = app.config['RESIZED_IMAGES'] / size / f"{id_}{ext}"
        return path if os.path.exists(path) else None
    return app.config['UPLOAD_DIR'] / f"{id_}{ext}"


def add_reference_systems_to_form(form: Any) -> str:
    html = ''
    switch_class = ''
    errors = False
    fields = []
    for field in form:
        if field.id.startswith('reference_system_id_'):
            fields.append(field)
            if field.errors:
                errors = True  # pragma: no cover
    if len(fields) > 3 and not errors:  # pragma: no cover
        switch_class = 'reference-system-switch'
        html = render_template('util/reference_system_switch.html')
    for field in fields:
        precision_field = getattr(form, field.id.replace('id_', 'precision_'))
        class_ = field.label.text \
            if field.label.text in ['GeoNames', 'Wikidata'] else ''
        html += add_form_row(
            field,
            field.label,
            f'{field(class_=class_)} {precision_field.label} {precision_field}',
            row_css=f'external-reference {switch_class}')
    return html


def add_dates_to_form(form: Any) -> str:
    errors = {}
    valid_dates = True
    for field_name in [
            'begin_year_from', 'begin_month_from', 'begin_day_from',
            'begin_year_to', 'begin_month_to', 'begin_day_to',
            'end_year_from', 'end_month_from', 'end_day_from',
            'end_year_to', 'end_month_to', 'end_day_to']:
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


def format_date(value: Union[datetime, numpy.datetime64]) -> str:
    if not value:
        return ''
    if isinstance(value, numpy.datetime64):
        date_ = datetime64_to_timestamp(value)
        return date_.lstrip('0') if date_ else ''
    return value.date().isoformat()


def external_url(url: Union[str, None]) -> str:
    return \
        f'<a target="blank_" rel="noopener noreferrer" href="{url}">{url}</a>' \
        if url else ''


def get_system_data(entity: Entity) -> dict[str, Any]:
    data = {}
    if 'entity_show_class' in current_user.settings \
            and current_user.settings['entity_show_class']:
        data[_('class')] = link(entity.cidoc_class)
    info = logger.get_log_info(entity.id)
    if 'entity_show_dates' in current_user.settings \
            and current_user.settings['entity_show_dates']:
        data[_('created')] = \
            f"{format_date(entity.created)} {link(info['creator'])}"
        if info['modified']:
            data[_('modified')] = \
                f"{format_date(info['modified'])} {link(info['modifier'])}"
    if 'entity_show_import' in current_user.settings \
            and current_user.settings['entity_show_import']:
        data[_('imported from')] = link(info['project'])
        data[_('imported by')] = link(info['importer'])
        data['origin ID'] = info['origin_id']
    if 'entity_show_api' in current_user.settings \
            and current_user.settings['entity_show_api']:
        data['API'] = render_template('util/api_links.html', entity=entity)
    return data


def convert_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0 B"  # pragma: no cover
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    return f"{int(size_bytes / math.pow(1024, i))} {size_name[i]}"


def delete_link(name: str, url: str) -> str:
    confirm = _('Delete %(name)s?', name=name.replace("'", ''))
    return link(_('delete'), url=url, js=f"return confirm('{confirm}')")


def display_delete_link(entity: Entity) -> str:
    if entity.id in g.types:
        url = url_for('type_delete', id_=entity.id)
    else:
        url = url_for('index', view=entity.class_.view, delete_id=entity.id)
    confirm = _('Delete %(name)s?', name=entity.name.replace('\'', ''))
    return button(_('delete'), url, onclick=f"return confirm('{confirm}')")


@app.template_filter()
def link(
        object_: Any,
        url: Optional[str] = None,
        class_: Optional[str] = '',
        uc_first_: Optional[bool] = True,
        js: Optional[str] = None) -> str:
    from openatlas.models.entity import Entity
    from openatlas.models.user import User
    if isinstance(object_, (str, LazyString)):
        return '<a href="{url}" class="{class_}" {js}>{label}</a>'.format(
            url=url,
            class_=class_,
            js=f'onclick="{js}"' if js else '',
            label=(uc_first(str(object_))) if uc_first_ else object_)
    if isinstance(object_, Entity):
        return link(
            object_.name,
            url_for('view', id_=object_.id),
            uc_first_=False)
    if isinstance(object_, CidocClass):
        return link(
            object_.code,
            url_for('cidoc_class_view', code=object_.code))
    if isinstance(object_, CidocProperty):
        return link(object_.code, url_for('property_view', code=object_.code))
    if isinstance(object_, Project):
        return link(
            object_.name,
            url_for('import_project_view', id_=object_.id))
    if isinstance(object_, User):
        return link(
            object_.username,
            url_for('user_view', id_=object_.id),
            class_='' if object_.active else 'inactive',
            uc_first_=False)
    return ''


@app.template_filter()
def button(
        label: str,
        url: Optional[str] = None,
        css: Optional[str] = 'primary',
        id_: Optional[str] = None,
        onclick: Optional[str] = None) -> str:
    tag = 'a' if url else 'span'
    label = uc_first(label)
    if url and '/insert' in url and label != uc_first(_('link')):
        label = f'+ {label}'
    return Markup(f"""
        <{tag}
            {f'href="{url}"' if url else ''}
            {f'id="{id_}"' if id_ else ''} 
            class="{app.config['CSS']['button'][css]}"
            {f'onclick="{onclick}"' if onclick else ''}>{label}</{tag}>""")


@app.template_filter()
def button_bar(buttons: list[Any]) -> str:
    return Markup(
        f'<div class="toolbar">{" ".join([str(b) for b in buttons])}</div>') \
        if buttons else ''


@app.template_filter()
def button_icon(
        icon: str,
        url: Optional[str] = None,
        css: Optional[str] = 'primary',
        id_: Optional[str] = None,
        onclick: Optional[str] = None) -> str:
    tag = 'a' if url else 'span'
    css_class = 'btn btn-xsm' if css == '' else app.config['CSS']['button'][css]
    return Markup(f"""
        <{tag}
            {f'href="{url}"' if url else ''}
            {f'id="{id_}"' if id_ else ''}
            class="{css_class}"
            {f'onclick="{onclick}"' if onclick else ''}>
                <i class="fa {icon}"></i>
            </{tag}>""")


@app.template_filter()
def display_citation_example(code: str) -> str:
    if code != 'reference':
        return ''
    if text := get_translation('citation_example'):
        return Markup(f'<h1>{uc_first(_("citation_example"))}</h1>{text}')
    return ''  # pragma: no cover


@app.template_filter()
def siblings_pager(entity: Entity, structure: Optional[dict[str, Any]]) -> str:
    if not structure or len(structure['siblings']) < 2:
        return ''
    structure['siblings'].sort(key=lambda x: x.id)
    prev_id = None
    next_id = None
    position = None
    for counter, sibling in enumerate(structure['siblings']):
        position = counter + 1
        prev_id = sibling.id if sibling.id < entity.id else prev_id
        if sibling.id > entity.id:
            next_id = sibling.id
            position = counter
            break
    parts = []
    if prev_id:  # pragma: no cover
        parts.append(button('<', url_for('view', id_=prev_id)))
    if next_id:
        parts.append(button('>', url_for('view', id_=next_id)))
    parts.append(f"{position} {_('of')} {len(structure['siblings'])}")
    return Markup(' '.join(parts))


@app.template_filter()
def breadcrumb(crumbs: list[Any]) -> str:
    from openatlas.models.entity import Entity
    from openatlas.models.user import User
    items = []
    for item in crumbs:
        if not item:
            continue  # e.g. if a dynamic generated URL has no origin parameter
        if isinstance(item, (Entity, Project, User)):
            items.append(link(item))
        elif isinstance(item, list):
            items.append(f'<a href="{item[1]}">{uc_first(str(item[0]))}</a>')
        else:
            items.append(uc_first(item))
    return Markup('&nbsp;>&nbsp; '.join(items))


@app.template_filter()
def uc_first(string: str) -> str:
    return str(string)[0].upper() + str(string)[1:] if string else ''


@app.template_filter()
def display_info(data: dict[str, Union[str, list[str]]]) -> str:
    return Markup(render_template('util/info_data.html', data=data))


def get_type_data(entity: Entity) -> dict[str, Any]:
    if entity.location:
        entity.types.update(entity.location.types)  # Add location types
    data: dict[str, Any] = defaultdict(list)
    for type_, value in sorted(entity.types.items(), key=lambda x: x[0].name):
        if entity.standard_type and type_.id == entity.standard_type.id:
            continue  # Standard type is already added
        html = f"""
            <span title="{" > ".join([g.types[i].name for i in type_.root])}">
                {link(type_)}</span>"""
        if type_.category == 'value':
            html += f' {float(value):g} {type_.description}'
        data[g.types[type_.root[0]].name].append(html)
    return {key: data[key] for key in sorted(data.keys())}


@app.template_filter()
def description(entity: Union[Entity, Project]) -> str:
    from openatlas.models.entity import Entity
    html = ''
    if isinstance(entity, Entity) \
            and entity.class_.name == 'stratigraphic_unit':
        from openatlas.views.anthropology import print_result
        if result := print_result(entity):
            html += \
                f"<h2>{uc_first(_('anthropological analyses'))}</h2>" \
                f"<p>{result}</p>"
    if not entity.description:
        return  Markup(html)
    label = _('description')
    if isinstance(entity, Entity) and entity.class_.name == 'source':
        label = _('content')
    return Markup(f"""
        {html}
        <h2>{uc_first(label)}</h2>
        <div class="description more">
            {'<br>'.join(entity.description.splitlines())}
        </div>""")


@app.template_filter()
def download_button(entity: Entity) -> str:
    if entity.image_id:
        if path := get_file_path(entity.image_id):
            return Markup(
                button(
                    _('download'),
                    url_for('download_file', filename=path.name)))
    return ''  # pragma: no cover


@app.template_filter()
def display_profile_image(entity: Entity) -> str:
    if not entity.image_id:
        return ''
    path = get_file_path(entity.image_id)
    if not path:
        return ''  # pragma: no cover
    resized = None
    size = app.config['IMAGE_SIZE']['thumbnail']
    if g.settings['image_processing'] and check_processed_image(path.name):
        if path_ := get_file_path(entity.image_id, size):
            resized = url_for('display_file', filename=path_.name, size=size)
    return Markup(
        render_template(
            'util/profile_image.html',
            entity=entity,
            path=path,
            resized=resized))


@contextfilter
@app.template_filter()
def display_content_translation(_context: str, text: str) -> str:
    return get_translation(text)


@app.template_filter()
def manual(site: str) -> str:
    """ If the manual page exists, return the link to it"""
    parts = site.split('/')
    if len(parts) < 2:
        return ''
    path = \
        Path(app.root_path) / 'static' / 'manual' / parts[0] / \
        (parts[1] + '.html')
    if not path.exists():
        # print(f'Missing manual link: {path}')
        return ''
    return Markup(
        f'<a class="manual" href="/static/manual/{site}.html" target="_blank" '
        f'title="{uc_first("manual")}"><i class="fas fa-book"></i></a>')


def add_form_row(
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


@app.template_filter()
def display_form(
        form: Any,
        form_id: Optional[str] = None,
        manual_page: Optional[str] = None) -> str:
    from openatlas.forms.field import ValueFloatField

    reference_systems_added = False
    html = ''
    for field in form:
        if isinstance(field, ValueFloatField) or field.id.startswith(
                ('insert_', 'reference_system_precision')):
            continue  # These will be added in combination with other fields
        if field.type in ['CSRFTokenField', 'HiddenField']:
            html += str(field)
            continue
        if field.id.split('_', 1)[0] in ('begin', 'end'):
            if field.id == 'begin_year_from':
                html += add_dates_to_form(form)
            continue

        if field.type in ['TreeField', 'TreeMultiField']:
            hierarchy_id = int(field.id)
            type_ = g.types[hierarchy_id]
            label = type_.name
            if type_.category == 'standard':
                label = uc_first(_('type'))
            if field.label.text == 'super':
                label = uc_first(_('super'))
            if type_.category == 'value' and 'is_type_form' not in form:
                field.description = type_.description
                html += add_form_row(
                    field,
                    label,
                    button_icon(
                        'fa-chevron-right',
                        onclick=f'switch_value_type({type_.id})',
                        css='',
                        id_=f'value-type-switcher-{type_.id}'))
                html += display_value_type_fields(form, type_)
                continue
            tooltip_ = '' \
                if 'is_type_form' in form else f' {tooltip(type_.description)}'
            html += add_form_row(field, label + tooltip_)
            continue

        if field.id == 'save':
            field.label.text = uc_first(field.label.text)
            class_ = app.config['CSS']['button']['primary']
            buttons = []
            if manual_page:
                buttons.append(escape(manual(manual_page)))
            buttons.append(field(class_=class_))
            if 'insert_and_continue' in form:
                buttons.append(form.insert_and_continue(class_=class_))
            if 'insert_continue_sub' in form:
                buttons.append(form.insert_continue_sub(class_=class_))
            if 'insert_continue_human_remains' in form:
                buttons.append(
                    form.insert_continue_human_remains(class_=class_))
            html += add_form_row(
                field,
                '',  # Setting label to '' keeps the button row label empty
                f'<div class="toolbar text-wrap">{" ".join(buttons)}</div>')
            continue

        if field.id.startswith('reference_system_id_'):
            if not reference_systems_added:
                html += add_reference_systems_to_form(form)
                reference_systems_added = True
            continue
        html += add_form_row(field, form_id=form_id)
    return Markup(render_template(
        'forms/form.html',
        form_id=form_id,
        form=form,
        html=html))


def display_value_type_fields(
        form: Any,
        type_: Type,
        root: Optional[Type] = None,
        level: int = 0) -> str:
    html = ''
    root = root if root else type_
    for sub_id in type_.subs:
        sub = g.types[sub_id]
        field = getattr(form, str(sub_id))
        expand_button = button_icon(
            'fa-chevron-right',
            onclick=f'switch_value_type({sub.id})',
            css='',
            id_=f'value-type-switcher-{sub.id}') if len(sub.subs) != 0 else ''
        html += f"""
        <div class="mt-2 table-row value-type-switch{type_.id}">
            <div></div>
            <div class="table-cell">
                <div class="d-flex">
                    <div
                            class="d-flex justify-content-between"
                            style="width:16.15em;">
                        <div class="ml-{level} position-relative text-wrap">
                            <div class="value-type-expander">
                                {expand_button}
                            </div>
                            {sub.name}
                        </div>
                        {field(class_='value-type')}
                    </div>
                    <span class="ml-1">
                        {sub.description if sub.description else ''}
                    </span>
                </div>
                {display_value_type_fields(form, sub, root, level+1)}
            </div>
        </div>"""
    return html


class MLStripper(HTMLParser):

    def error(self: MLStripper, message: str) -> None:  # pragma: no cover
        pass

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed: list[str] = []

    def handle_data(self, d: Any) -> None:
        self.fed.append(d)

    def get_data(self) -> str:
        return ''.join(self.fed)


def format_date_part(date: numpy.datetime64, part: str) -> str:
    string = str(date).split(' ')[0]
    bc = False
    if string.startswith('-') or string.startswith('0000'):
        bc = True
        string = string[1:]
    parts = string.split('-')
    if part == 'year':  # If it's a negative year, add one year
        return f'-{int(parts[0]) + 1}' if bc else f'{int(parts[0])}'
    if part == 'month':
        return parts[1]
    return parts[2]


def timestamp_to_datetime64(string: str) -> Optional[numpy.datetime64]:
    if not string:
        return None
    if 'BC' in string:
        parts = string.split(' ')[0].split('-')
        string = f'-{int(parts[0]) - 1}-{parts[1]}-{parts[2]}'
    return numpy.datetime64(string.split(' ')[0])


def datetime64_to_timestamp(
        date: Union[numpy.datetime64, None]) -> Optional[str]:
    if not date:
        return None
    string = str(date)
    postfix = ''
    if string.startswith('-') or string.startswith('0000'):
        string = string[1:]
        postfix = ' BC'
    parts = string.split('-')
    year = int(parts[0]) + 1 if postfix else int(parts[0])
    return f'{year:04}-{int(parts[1]):02}-{int(parts[2]):02}{postfix}'
