from __future__ import annotations

import math
import os
import re
import smtplib
import subprocess
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
from jinja2 import contextfilter
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from openatlas import app
from openatlas.display.image_processing import check_processed_image
from openatlas.models.cidoc_class import CidocClass
from openatlas.models.cidoc_property import CidocProperty
from openatlas.models.content import get_translation

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity
    from openatlas.models.user import User
    from openatlas.models.link import Link
    from openatlas.models.type import Type


def remove_link(
        name: str,
        link_: Link,
        origin: Entity,
        tab: Optional[str] = '') -> Optional[str]:
    if not is_authorized('contributor'):
        return None
    url = url_for('link_delete', id_=link_.id, origin_id=origin.id)
    return link(
        _('remove'),
        f'{url}#tab-{tab}' if tab else url,
        js="return confirm('{x}')".format(
            x=_('Remove %(name)s?', name=name.replace("'", ''))))


def edit_link(url: str) -> Optional[str]:
    return link(_('edit'), url) if is_authorized('contributor') else None


@app.template_filter()
def ext_references(links: list[Link]) -> str:
    if not links:
        return ''
    html = '<h2 class="uc-first">' + _("external reference systems") + '</h2>'
    for link_ in links:
        system = g.reference_systems[link_.domain.id]
        html += link(
            f'{system.resolver_url}{link_.description}',
            f'{system.resolver_url}{link_.description}',
            external=True) if system.resolver_url else link_.description
        html += \
            f' ({g.types[link_.type.id].name} ' + _('at') + \
            f' {link(link_.domain)})<br>'
    return html


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


def profile_image_table_link(entity: Entity, file: Entity, ext: str) -> str:
    if file.id == entity.image_id:
        return link(
            _('unset'),
            url_for('file_remove_profile_image', entity_id=entity.id))
    if ext in g.display_file_ext:
        return link(
            _('set'),
            url_for('set_profile_image', id_=file.id, origin_id=entity.id))
    return ''


def get_chart_data(entity: Type) -> Optional[dict[str, Any]]:
    if not entity.subs:
        return None
    data = {}
    for id_ in entity.subs:
        if count := g.types[id_].count + g.types[id_].count_subs:
            data[g.types[id_].name] = count
    if data:
        data = dict(
            sorted(data.items(), key=lambda item: item[1], reverse=True))
        return {
            'labels': list(data.keys()),
            'datasets': [{'data': list(data.values())}]}
    return None


def get_system_data(entity: Entity) -> dict[str, Any]:
    data = {}
    if 'entity_show_class' in current_user.settings \
            and current_user.settings['entity_show_class']:
        data[_('class')] = link(entity.cidoc_class)
    info = g.logger.get_log_info(entity.id)
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
    return data


def bookmark_toggle(entity_id: int, for_table: bool = False) -> str:
    label = _('bookmark remove') \
        if entity_id in current_user.bookmarks else _('bookmark')
    onclick = f"ajaxBookmark('{entity_id}');"
    if for_table:
        return \
            f'<a href="#" id="bookmark{entity_id}" onclick="{onclick}">' \
            f'{label}</a>'
    return button(label, id_=f'bookmark{entity_id}', onclick=onclick)


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
        if view_name == item \
                or request.path.startswith(f'/{item}') \
                or request.path.startswith(f'/index/{item}'):
            active = 'active'
        elif len(request_parts) > 2 and request.path.startswith('/insert/'):
            name = request_parts[2]
            if name in g.class_view_mapping \
                    and g.class_view_mapping[name] == item:
                active = 'active'
        if item == 'type':
            html += \
                f'<a href="{url_for("type_index")}" ' \
                f'class="nav-item nav-link fw-bold uc-first {active}">' + \
                _('types') + '</a>'
        else:
            html += \
                f'<a href="{url_for("index", view=item)}" ' \
                f'class="nav-item nav-link fw-bold uc-first {active}">' + \
                _(item) + '</a>'
    return html


@app.template_filter()
def profile_image(entity: Entity) -> str:
    if not entity.image_id:
        return ''
    if not (path := get_file_path(entity.image_id)):
        return ''  # pragma: no cover

    src = url_for('display_file', filename=path.name)
    url = src
    width = g.settings["profile_image_width"]
    if app.config['IIIF']['activate'] and check_iiif_file_exist(entity.id):
        url = url_for('view_iiif', id_=entity.id)
        iiif_ext = '.tiff' if app.config['IIIF']['conversion'] \
            else g.files[entity.id].suffix
        src = \
            f"{app.config['IIIF']['url']}{entity.id}{iiif_ext}" \
            f"/full/!{width},{width}/0/default.jpg"
    elif g.settings['image_processing'] and check_processed_image(path.name):
        if path_ := get_file_path(
                entity.image_id,
                app.config['IMAGE_SIZE']['thumbnail']):
            src = url_for(
                'display_file',
                size=app.config['IMAGE_SIZE']['thumbnail'],
                filename=path_.name)
    external = False
    if entity.class_.view == 'file':
        external = True
        if path.suffix.lower() not in g.display_file_ext:
            return '<p class="uc-first">' + _('no preview available') + '</p>'
    else:
        url = url_for('view', id_=entity.image_id)
    html = link(
        f'<img style="max-width:{width}px" alt="{entity.name}" src="{src}">',
        url,
        external=external)
    return html


@app.template_filter()
def get_js_messages(lang: str) -> str:
    js_message_file = Path('static') / 'vendor' / 'jquery_validation_plugin' \
                      / f'messages_{lang}.js'
    if not (Path(app.root_path) / js_message_file).is_file():
        return ''
    return f'<script src="/{js_message_file}"></script>'


@contextfilter  # Prevent Jinja2 context caching
@app.template_filter()
def is_authorized(context: str, group: Optional[str] = None) -> bool:
    if not group:  # In case it wasn't called from a template
        group = context
    if not current_user.is_authenticated or not hasattr(current_user, 'group'):
        return False
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
    if mode == 'text':  # Remove HTML tags, keep linebreaks
        stripper = MLStripper()
        stripper.feed(string)
        return stripper.get_data().strip()
    return re.sub('[^A-Za-z0-9]+', '', string)  # Filter ASCII letters/numbers


def format_name_and_aliases(entity: Entity, show_links: bool) -> str:
    name = link(entity) if show_links else entity.name
    if not entity.aliases or not current_user.settings['table_show_aliases']:
        return name
    return \
        f'{name}' \
        f'{"".join(f"<p>{alias}</p>" for alias in entity.aliases.values())}'


def get_backup_file_data() -> dict[str, Any]:
    path = app.config['EXPORT_PATH']
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
        file_data['backup_too_old'] = \
            bool(yesterday > latest_file_date and not app.testing)
        file_data['size'] = convert_size(latest_file.stat().st_size)
        file_data['date'] = format_date(latest_file_date)
    return file_data


def get_base_table_data(entity: Entity, show_links: bool = True) -> list[Any]:
    data: list[Any] = [format_name_and_aliases(entity, show_links)]
    if entity.class_.view in [
            'actor', 'artifact', 'event', 'place', 'reference']:
        data.append(entity.class_.label)
    if entity.class_.standard_type_id:
        data.append(entity.standard_type.name if entity.standard_type else '')
    if entity.class_.name == 'file':
        data.append(entity.get_file_size())
        data.append(entity.get_file_ext())
    if entity.class_.view in ['actor', 'artifact', 'event', 'place']:
        data.append(entity.first)
        data.append(entity.last)
    data.append(entity.description)
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
        log_body: bool = True) -> bool:
    """
        Send one mail to every recipient.
        Set log_body to False for sensitive data, e.g. password mails.
    """
    recipients = recipients if isinstance(recipients, list) else [recipients]
    if not g.settings['mail'] or not recipients:
        return False  # pragma: no cover
    from_ = f"{g.settings['mail_from_name']} <{g.settings['mail_from_email']}>"
    if app.testing:
        return True  # To test mail functions without sending them
    try:  # pragma: no cover
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
            g.logger.log('info', 'mail', f'Mail send from {from_}', log_text)
    except smtplib.SMTPAuthenticationError as e:  # pragma: no cover
        g.logger.log(
            'error',
            'mail',
            f"Error mail login for {g.settings['mail_transport_username']}", e)
        flash(_('error mail login'), 'error')
        return False
    except Exception as e:  # pragma: no cover
        g.logger.log(
            'error',
            'mail',
            f"Error send mail for {g.settings['mail_transport_username']}", e)
        flash(_('error mail send'), 'error')
        return False  # pragma: no cover
    return True  # pragma: no cover


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
    if app.config['IIIF']['activate']:
        if path := app.config['IIIF']['path']:
            check_write_access(path, warnings)
    for path in g.writable_paths:
        check_write_access(path, warnings)
    if is_authorized('admin'):
        from openatlas.models.user import User
        user = User.get_by_username('OpenAtlas')
        if user and user.active:
            hash_ = hashpw(
                'change_me_PLEASE!'.encode('utf-8'),
                user.password.encode('utf-8'))
            if hash_ == user.password.encode('utf-8'):
                warnings.append(
                    '<p class="uc-first mb-0">' +
                    _('user OpenAtlas with default password is still active') +
                    '</p>')
    return \
        '<div class="alert alert-danger">' \
        f'{"<br>".join(warnings)}</div>' if warnings else ''


def check_write_access(path: Path, warnings: list[str]) -> list[str]:
    if not os.access(path, os.W_OK):
        warnings.append(
            '<p class="uc-first">' + _('directory not writable') +
            f" {str(path).replace(app.root_path, '')}</p>")
    return warnings


@app.template_filter()
def tooltip(text: str) -> str:
    if not text:
        return ''
    return """
        <span>
            <i class="fas fa-info-circle tooltipicon" title="{title}"></i>
        </span>""".format(title=text.replace('"', "'"))


def get_file_path(
        entity: Union[int, Entity],
        size: Optional[str] = None) -> Optional[Path]:
    id_ = entity if isinstance(entity, int) else entity.id
    if id_ not in g.files:
        return None
    ext = g.files[id_].suffix
    if size:
        if ext in app.config['PROCESSABLE_EXT']:
            ext = app.config['PROCESSED_EXT']  # pragma: no cover
        path = app.config['RESIZED_IMAGES'] / size / f"{id_}{ext}"
        return path if os.path.exists(path) else None
    return app.config['UPLOAD_PATH'] / f"{id_}{ext}"


def format_date(value: Union[datetime, numpy.datetime64]) -> str:
    if not value:
        return ''
    if isinstance(value, numpy.datetime64):
        date_ = datetime64_to_timestamp(value)
        return date_.lstrip('0').replace(' 00:00:00', '') if date_ else ''
    return value.date().isoformat().replace(' 00:00:00', '')


def convert_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0 B"  # pragma: no cover
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    return f"{int(size_bytes / math.pow(1024, i))} {size_name[i]}"


@app.template_filter()
def link(
        object_: Any,
        url: Optional[str] = None,
        class_: Optional[str] = '',
        uc_first_: Optional[bool] = True,
        js: Optional[str] = None,
        external: bool = False) -> str:
    from openatlas.models.entity import Entity
    from openatlas.models.user import User
    from openatlas.models.imports import Project
    html = ''
    if isinstance(object_, (str, LazyString)):
        js = f'onclick="{js}"' if js else ''
        uc_first_class = 'uc-first' if uc_first_ and not \
            str(object_).startswith('http') else ''
        ext = 'target="_blank" rel="noopener noreferrer"' if external else ''
        html = \
            f'<a href="{url}" class="{class_} {uc_first_class}" {js} ' \
            f'{ext}>{object_}</a>'
    elif isinstance(object_, Entity):
        html = link(
            object_.name,
            url_for('view', id_=object_.id),
            uc_first_=False,
            external=external)
    elif isinstance(object_, CidocClass):
        html = link(
            object_.code,
            url_for('cidoc_class_view', code=object_.code),
            external=external)
    elif isinstance(object_, CidocProperty):
        html = link(
            object_.code,
            url_for('property_view', code=object_.code),
            external=external)
    elif isinstance(object_, Project):
        html = link(
            object_.name,
            url_for('import_project_view', id_=object_.id),
            external=external)
    elif isinstance(object_, User):
        html = link(
            object_.username,
            url_for('user_view', id_=object_.id),
            class_='' if object_.active else 'inactive',
            uc_first_=False,
            external=external)
    return html


@app.template_filter()
def button(
        label: str,
        url: Optional[str] = None,
        css: Optional[str] = 'primary',
        id_: Optional[str] = None,
        onclick: Optional[str] = None,
        tooltip_text: Optional[str] = None) -> str:
    tag = 'a' if url else 'span'
    if url and '/insert' in url and label != _('link'):
        label = f'+ <span class="uc-first d-inline-block">{label}</span>'
    tooltip_ = ''
    if tooltip_text:
        tooltip_ = \
            'data-bs-toggle="tooltip" data-bs-placement="top" ' \
            f'title="{uc_first(tooltip_text)}"'
    return f"""
        <{tag}
            {f'href="{url}"' if url else ''}
            {f'id="{id_}"' if id_ else ''}
            class="{app.config['CSS']['button'][css]} uc-first"
            {f'onclick="{onclick}"' if onclick else ''}
            tabindex="0"
            role="button"
            {tooltip_}>{label}</{tag}>"""


@app.template_filter()
def button_bar(buttons: list[Any]) -> str:
    def add_col(input_: str) -> str:
        return \
            f'<div class="col-auto d-flex align-items-center">{input_}</div>'

    return \
        '<div class="row my-2 g-1">' \
        f'{" ".join([str(b) for b in list(map(add_col, buttons))])}' \
        '</div>' if buttons else ''


@app.template_filter()
def display_citation_example(code: str) -> str:
    html = ''
    if code == 'reference' and (text := get_translation('citation_example')):
        html = '<h1 class="uc-first">' + _('citation_example') + f'</h1>{text}'
    return html


@app.template_filter()
def breadcrumb(crumbs: list[Any]) -> str:
    items = []
    for item in crumbs:
        if isinstance(item, list):
            items.append(
                f'<a href="{item[1]}" class="uc-first">{str(item[0])}</a>')
        elif isinstance(item, (str, LazyString)):
            items.append(f'<span class="uc-first">{item}</span>')
        elif item:
            items.append(link(item))
    return '&nbsp;>&nbsp; '.join(items)


@app.template_filter()
def uc_first(string: str) -> str:
    return str(string)[0].upper() + str(string)[1:] if string else ''


@app.template_filter()
def display_info(data: dict[str, Union[str, list[str]]]) -> str:
    return render_template('util/info_data.html', data=data)


@app.template_filter()
def description(text: str, label: Optional[str] = '') -> str:
    return '' if not text else \
        f'<h2 class="uc-first fw-bold">{label or _("description")}</h2>' \
        f'<div class="description more">{"<br>".join(text.splitlines())}</div>'


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
    return \
        '<a title="' + uc_first(_('manual')) + '" ' \
        f'href="/static/manual/{site}.html" class="manual" ' \
        f'target="_blank" rel="noopener noreferrer">' \
        f'<i class="fas fs-4 fa-book"></i></a>'


@app.template_filter()
def display_form(
        form: Any,
        form_id: Optional[str] = None,
        manual_page: Optional[str] = None) -> str:
    from openatlas.forms.display import html_form
    form_id = f'id="{form_id}"' if form_id else ''
    multipart = 'enctype="multipart/form-data"' if 'file' in form else ''
    return \
        f'<form method="post" {form_id} {multipart}>' \
        '<table class="table table-no-style">' \
        f'{html_form(form, form_id, manual_page)}' \
        f'</table></form>'


class MLStripper(HTMLParser):

    def error(self: MLStripper, message: str) -> None:
        pass  # pragma: no cover

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed: list[str] = []

    def handle_data(self, data: Any) -> None:
        self.fed.append(data)

    def get_data(self) -> str:
        return ''.join(self.fed)


def format_date_part(date: numpy.datetime64, part: str) -> str:
    string = str(date).split(' ')[0]
    bc = False
    if string.startswith('-') or string.startswith('0000'):
        bc = True
        string = string[1:]
    string = string.replace('T', '-').replace(':', '-')
    parts = string.split('-')
    if part == 'year':  # If it's a negative year, add one year
        return f'-{int(parts[0]) + 1}' if bc else f'{int(parts[0])}'
    if part == 'month':
        return parts[1]
    if part == 'hour':
        return parts[3]
    if part == 'minute':
        return parts[4]
    if part == 'second':
        return parts[5]
    return parts[2]


def timestamp_to_datetime64(string: str) -> Optional[numpy.datetime64]:
    if not string:
        return None
    string_list = string.split(' ')
    if 'BC' in string_list:
        parts = string_list[0].split('-')
        date = f'-{int(parts[0]) - 1}-{parts[1]}-{parts[2]}T{string_list[1]}'
        return numpy.datetime64(date)
    return numpy.datetime64(f'{string_list[0]}T{string_list[1]}')


def datetime64_to_timestamp(date: Optional[numpy.datetime64]) -> Optional[str]:
    if not date:
        return None
    string = str(date)
    postfix = ''
    if string.startswith('-') or string.startswith('0000'):
        string = string[1:]
        postfix = ' BC'
    string = string.replace('T', '-').replace(':', '-').replace(' ', '-')
    parts = string.split('-')
    year = int(parts[0]) + 1 if postfix else int(parts[0])
    hour = 0
    minute = 0
    second = 0
    if len(parts) > 3:
        hour = int(parts[3])
        minute = int(parts[4])
        second = int(parts[5])
    return \
        f'{year:04}-{int(parts[1]):02}-{int(parts[2]):02} ' \
        f'{hour:02}:{minute:02}:{second:02}{postfix}'


def get_entities_linked_to_type_recursive(
        id_: int,
        data: list[Entity]) -> list[Entity]:
    for entity in g.types[id_].get_linked_entities(['P2', 'P89'], True, True):
        data.append(entity)
    for sub_id in g.types[id_].subs:
        get_entities_linked_to_type_recursive(sub_id, data)
    return data


def check_iiif_activation() -> bool:
    iiif = app.config['IIIF']
    return bool(iiif['activate'] and os.access(Path(iiif['path']), os.W_OK))


def check_iiif_file_exist(id_: int) -> bool:
    if app.config['IIIF']['conversion']:
        return get_iiif_file_path(id_).is_file()
    return bool(get_file_path(id_))


def get_iiif_file_path(id_: int) -> Path:
    ext = '.tiff' if app.config['IIIF']['conversion'] \
        else g.files[id_].suffix
    return Path(app.config['IIIF']['path']) / f'{id_}{ext}'


def convert_image_to_iiif(id_: int) -> None:
    compression = app.config['IIIF']['compression'] \
        if app.config['IIIF']['compression'] in ['deflate', 'jpeg'] \
        else 'deflate'
    vips = "vips" if os.name == 'posix' else "vips.exe"
    command = \
        (f"{vips} tiffsave {get_file_path(id_)} {get_iiif_file_path(id_)} "
         f"--tile --pyramid --compression {compression} "
         f"--premultiply --tile-width 128 --tile-height 128")
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
        flash(_('IIIF converted'), 'info')
    except Exception as e:  # pragma: no cover
        flash(f"{_('failed to convert image')}: {e}", 'error')
