from __future__ import annotations

import math
import os
import re
import smtplib
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
from openatlas.models.cidoc_class import CidocClass
from openatlas.models.cidoc_property import CidocProperty
from openatlas.models.content import get_translation
from openatlas.models.imports import Project

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity
    from openatlas.models.user import User


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
                f'class="nav-item nav-link {active}">' + \
                uc_first(_("types")) + '</a>'
        else:
            html += \
                f'<a href="{url_for("index", view=item)}" ' \
                f'class="nav-item nav-link {active}">' + uc_first(_(item)) + \
                '</a>'
    return html


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


@app.template_filter()
def test_file(file_name: str) -> Optional[str]:
    return file_name if (Path(app.root_path) / file_name).is_file() else None


def format_name_and_aliases(entity: Entity, show_links: bool) -> str:
    name = link(entity) if show_links else entity.name
    if not entity.aliases or not current_user.settings['table_show_aliases']:
        return name
    return \
        f'<p>{name}</p>' \
        f'{"".join(f"<p>{alias}</p>" for alias in entity.aliases.values())}'


def get_backup_file_data() -> dict[str, Any]:
    path = app.config['EXPORT_DIR']
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
    if entity.class_.view in [
            'actor', 'artifact', 'event', 'place', 'reference']:
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
        return False
    from_ = f"{g.settings['mail_from_name']} <{g.settings['mail_from_email']}>"
    if app.config['IS_UNIT_TEST']:
        return True  # To test mail functions w/o sending them
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
        return f'<p class="error">{"<br>".join(warnings)}<p>'
    return ''


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
    if id_ not in g.file_stats:
        return None
    ext = g.file_stats[id_]['ext']
    if size:
        if ext in app.config['NONE_DISPLAY_EXT']:
            ext = app.config['PROCESSED_EXT']
        path = app.config['RESIZED_IMAGES'] / size / f"{id_}{ext}"
        return path if os.path.exists(path) else None
    return app.config['UPLOAD_DIR'] / f"{id_}{ext}"


def format_date(value: Union[datetime, numpy.datetime64]) -> str:
    if not value:
        return ''
    if isinstance(value, numpy.datetime64):
        date_ = datetime64_to_timestamp(value)
        return date_.lstrip('0').replace(' 00:00:00', '') if date_ else ''
    return value.date().isoformat().replace(' 00:00:00', '')


def convert_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0 B"
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
    if isinstance(object_, (str, LazyString)):
        js = f'onclick="{js}"' if js else ''
        label = uc_first(str(object_)) if uc_first_ else object_
        class_ = f'class="{class_}"' if class_ else ''
        ext = 'target="_blank" rel="noopener noreferrer"' if external else ''
        return f'<a href="{url}" {class_} {js} {ext}>{label}</a>'
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
    return f"""
        <{tag}
            {f'href="{url}"' if url else ''}
            {f'id="{id_}"' if id_ else ''}
            class="{app.config['CSS']['button'][css]}"
            {f'onclick="{onclick}"' if onclick else ''}>{label}</{tag}>"""


@app.template_filter()
def button_bar(buttons: list[Any]) -> str:
    return \
        f'<div class="toolbar">{" ".join([str(b) for b in buttons])}</div>' \
        if buttons else ''


@app.template_filter()
def display_citation_example(code: str) -> str:
    if code != 'reference':
        return ''
    if text := get_translation('citation_example'):
        return '<h1>' + uc_first(_("citation_example")) + f'</h1>{text}'
    return ''


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
    return '&nbsp;>&nbsp; '.join(items)


@app.template_filter()
def uc_first(string: str) -> str:
    return str(string)[0].upper() + str(string)[1:] if string else ''


@app.template_filter()
def display_info(data: dict[str, Union[str, list[str]]]) -> str:
    return render_template('util/info_data.html', data=data)


@app.template_filter()
def description(entity: Union[Entity, Project, User]) -> str:
    from openatlas.models.entity import Entity
    html = ''
    if isinstance(entity, Entity) \
            and entity.class_.name == 'stratigraphic_unit':
        from openatlas.views.tools import print_sex_result
        if result := print_sex_result(entity):
            html += \
                "<h2>" + uc_first(_('anthropological analyses')) + '</h2>' \
                f"<p>{result}</p>"
    if not entity.description:
        return html
    label = _('description')
    if isinstance(entity, Entity) and entity.class_.name == 'source':
        label = _('content')
    return f"""
        {html}
        <h2>{uc_first(label)}</h2>
        <div class="description more">
            {'<br>'.join(entity.description.splitlines())}
        </div>"""


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
        '<a title="' + uc_first("manual") + '" ' \
        f'href="/static/manual/{site}.html" class="manual" target="_blank" ' \
        'rel="noopener noreferrer"><i class="fas fa-book"></i></a>'


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
        f'<div class="data-table">{html_form(form, form_id, manual_page)}' \
        f'</div></form>'


class MLStripper(HTMLParser):

    def error(self: MLStripper, message: str) -> None:
        pass

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


def datetime64_to_timestamp(
        date: Union[numpy.datetime64, None]) -> Optional[str]:
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
    for entity in g.types[id_].get_linked_entities(
            ['P2', 'P89'],
            inverse=True,
            types=True):
        data.append(entity)
    for sub_id in g.types[id_].subs:
        get_entities_linked_to_type_recursive(sub_id, data)
    return data
