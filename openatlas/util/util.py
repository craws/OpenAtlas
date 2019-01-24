# Created by Alexander Watzinger and others. Please see README.md for licensing information
import glob
import os
import re
import smtplib
from collections import OrderedDict
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from functools import wraps
from html.parser import HTMLParser

import numpy
from babel import dates
from flask import abort, flash, g, request, session, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user
from numpy import math
from werkzeug.utils import redirect

import openatlas
from openatlas import app
from openatlas.models.classObject import ClassObject
from openatlas.models.date import DateMapper
from openatlas.models.imports import Project
from openatlas.models.property import Property
from openatlas.models.user import User


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"  # pragma: no cover
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    return "%s %s" % (int(size_bytes / math.pow(1024, i)), size_name[i])


def get_file_path(entity):
    entity_id = entity if type(entity) is int else entity.id
    path = glob.glob(os.path.join(app.config['UPLOAD_FOLDER_PATH'], str(entity_id) + '.*'))
    return path[0] if path else None


def print_file_size(entity):
    entity_id = entity if type(entity) is int else entity.id
    path = get_file_path(entity_id)
    return convert_size(os.path.getsize(path)) if path else 'N/A'


def display_tooltip(text):
    if not text:
        return ''
    return ' <span class="tooltip" title="{title}">i</span>'.format(title=text.replace('"', "'"))


def print_file_extension(entity):
    entity_id = entity if type(entity) is int else entity.id
    path = get_file_path(entity_id)
    return os.path.splitext(path)[1] if path else 'N/A'


def send_mail(subject, text, recipients, log_body=True):  # pragma: no cover
    """ Send one mail to every recipient, set log_body to False for sensitive data e.g. passwords"""
    settings = session['settings']
    recipients = recipients if type(recipients) is list else [recipients]
    if not settings['mail'] or len(recipients) < 1:
        return
    mail_user = settings['mail_transport_username']
    from_ = settings['mail_from_name'] + ' <' + settings['mail_from_email'] + '>'
    server = smtplib.SMTP(settings['mail_transport_host'], settings['mail_transport_port'])
    server.ehlo()
    server.starttls()
    try:
        if settings['mail_transport_username']:
            server.login(mail_user, app.config['MAIL_PASSWORD'])
        for recipient in recipients:
            msg = MIMEText(text, _charset='utf-8')
            msg['From'] = from_
            msg['To'] = recipient.strip()
            msg['Subject'] = Header(subject.encode('utf-8'), 'utf-8')
            server.sendmail(settings['mail_from_email'], recipient, msg.as_string())
        log_text = 'Mail from ' + from_ + ' to ' + ', '.join(recipients) + ' Subject: ' + subject
        log_text += ' Content: ' + text if log_body else ''
        openatlas.logger.log('info', 'mail', 'Mail send from ' + from_, log_text)
    except smtplib.SMTPAuthenticationError as e:
        openatlas.logger.log('error', 'mail', 'Error mail login for ' + mail_user, str(e))
        flash(_('error mail login'), 'error')
        return False
    except Exception as e:
        openatlas.logger.log('error', 'mail', 'Error send mail for ' + mail_user, str(e))
        flash(_('error mail send'), 'error')
        return False
    return True


class MLStripper(HTMLParser):

    def error(self, message):  # pragma: no cover
        pass

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def sanitize(string, mode=None):
    if not mode:
        # Remove all characters from a string except ASCII letters and numbers
        return re.sub('[^A-Za-z0-9]+', '', string)
    if mode == 'node':
        # Remove all characters from a string except letters, numbers and spaces
        return re.sub(r'([^\s\w]|_)+', '', string).strip()
    if mode == 'description':
        s = MLStripper()
        s.feed(string)
        return s.get_data()


def get_file_stats(path=app.config['UPLOAD_FOLDER_PATH']):
    """ Build a dict with file ids and stats from files in given directory.
        It's much faster to do this in one call for every file."""
    file_stats = {}
    for file in os.scandir(path):
        split_name = os.path.splitext(file.name)
        if len(split_name) > 1 and split_name[0].isdigit():
            file_stats[int(split_name[0])] = {'ext': split_name[1], 'size': file.stat().st_size,
                                              'date': file.stat().st_ctime}
    return file_stats


def build_table_form(class_name, linked_entities):
    """ Returns a form with a list of entities with checkboxes"""
    from flask_wtf.csrf import generate_csrf
    from openatlas.models.entity import EntityMapper
    header = app.config['TABLE_HEADERS'][class_name] + ['']
    table = {'id': class_name, 'header': header, 'data': []}
    linked_ids = [entity.id for entity in linked_entities]
    file_stats = get_file_stats() if class_name == 'file' else None
    if class_name == 'file':
        entities = EntityMapper.get_by_system_type('file')
    elif class_name == 'place':
        entities = EntityMapper.get_by_system_type('place')
    else:
        entities = EntityMapper.get_by_codes(class_name)
    for entity in entities:
        if entity.id in linked_ids:
            continue  # Don't show already linked entries
        input_ = '<input id="{id}" name="values" type="checkbox" value="{id}">'.format(id=entity.id)
        table['data'].append(get_base_table_data(entity, file_stats) + [input_])
    if not table['data']:
        return uc_first(_('no entries'))
    return """<form class="table" method="post">
                <input id="csrf_token" name="csrf_token" type="hidden" value="{token}">
                {pager} <button name="form-submit" id="form-submit" type="submit">{add}</button>
              </form>""".format(add=uc_first(_('add')), pager=pager(table), token=generate_csrf())


def display_remove_link(url, name):
    """ Build a link to remove a link with a JavaScript confirmation dialog"""
    name = name.replace('\'', '')
    confirm = 'onclick="return confirm(\'' + _('Remove %(name)s?', name=name) + '\')"'
    return '<a ' + confirm + ' href="' + url + '">' + uc_first(_('remove')) + '</a>'


def get_entity_data(entity, location=None):
    """
    Return related entity information for a table for view.
    The location parameter is for places which have a location attached.
    """
    data = []
    type_data = OrderedDict()

    # Nodes
    if location:
        entity.nodes.update(location.nodes)  # Add location types
    for node, node_value in entity.nodes.items():
        root = g.nodes[node.root[-1]]
        name = 'type' if root.name in app.config['BASE_TYPES'] else root.name
        if root.name not in type_data:
            type_data[name] = []
        text = ''
        if root.value_type:  # Text for value types
            text = ': {value} <span style="font-style:italic;">{description}</span>'.format(
                value=format_number(node_value), description=node.description)
        type_data[name].append(link(node) + text)

    # Sort by name
    type_data = OrderedDict(sorted(type_data.items(), key=lambda t: t[0]))
    for root_type in type_data:
        type_data[root_type].sort()

    # Move the base type to the top
    if 'type' in type_data:
        type_data.move_to_end('type', last=False)
    for root_name, nodes in type_data.items():
        data.append((root_name, '<br />'.join(nodes)))

    # Info for places
    if entity.class_.code in app.config['CLASS_CODES']['place']:
        aliases = entity.get_linked_entities('P1')
        if aliases:
            data.append((uc_first(_('alias')), '<br />'.join([x.name for x in aliases])))

    # Info for files
    if entity.system_type == 'file':
        data.append((uc_first(_('size')), print_file_size(entity)))
        data.append((uc_first(_('extension')), print_file_extension(entity)))

    # Info for events
    if entity.class_.code in app.config['CLASS_CODES']['event']:
        super_event = entity.get_linked_entity('P117')
        if super_event:
            data.append((uc_first(_('sub event of')), link(super_event)))
        place = entity.get_linked_entity('P7')
        if place:
            data.append((uc_first(_('location')), link(place.get_linked_entity('P53', True))))
        # Info for acquisitions
        if entity.class_.code == 'E8':
            data.append((uc_first(_('recipient')), '<br />'.join(
                [link(recipient) for recipient in entity.get_linked_entities('P22')])))
            data.append((uc_first(_('donor')), '<br />'.join(
                [link(donor) for donor in entity.get_linked_entities('P23')])))
            data.append((uc_first(_('given place')), '<br />'.join(
                [link(place) for place in entity.get_linked_entities('P24')])))

    # Info for actors
    if entity.class_.code in app.config['CLASS_CODES']['actor']:
        aliases = entity.get_linked_entities('P131')
        if aliases:
            data.append((uc_first(_('alias')), '<br />'.join([x.name for x in aliases])))

    # Dates
    html = ''
    if entity.begin_from:
        html += format_date(entity.begin_from)
        if entity.begin_to:
            html += ' ' + uc_first(_('between')) + ' ' + format_date(entity.begin_to)
    html += ' ' + entity.begin_comment if entity.begin_comment else ''
    if html:
        data.append((uc_first('begin'), html))
    html = ''
    if entity.end_from:
        html += format_date(entity.end_from)
        if entity.end_to:
            html += ' ' + uc_first(_('between')) + ' ' + format_date(entity.end_to)
    html += ' ' + entity.end_comment if entity.end_comment else ''
    if html:
        data.append((uc_first('end'), html))

    # Additional info for advanced layout
    if hasattr(current_user, 'settings') and current_user.settings['layout'] == 'advanced':
        data.append((uc_first(_('class')), link(entity.class_)))
        info = openatlas.logger.get_log_for_advanced_view(entity.id)
        data.append((_('created'), format_date(entity.created) + ' ' + link(info['creator'])))
        if info['modified']:
            html = format_date(info['modified']) + ' ' + link(info['modifier'])
            data.append((_('modified'), html))
        if info['import_project']:
            data.append((_('imported from'), link(info['import_project'])))
        if info['import_user']:
            data.append((_('imported by'), link(info['import_user'])))
        if info['import_origin_id']:
            data.append(('origin ID', info['import_origin_id']))

    return data


def add_dates_to_form(form, for_person=False):
    errors = {}
    valid_dates = True
    for field_name in ['begin_year_from', 'begin_month_from', 'begin_day_from',
                       'begin_year_to', 'begin_month_to', 'begin_day_to',
                       'end_year_from', 'end_month_from', 'end_day_from',
                       'end_year_to', 'end_month_to', 'end_day_to']:
        errors[field_name] = ''
        if getattr(form, field_name).errors:
            valid_dates = False
            errors[field_name] = '<label class="error">'
            for error in getattr(form, field_name).errors:
                errors[field_name] += uc_first(error)
            errors[field_name] += ' </label>'
    style = '' if valid_dates else ' style="display:table-row" '
    html = """
        <div class="table-row">
            <div>
                <label>{date}</label> {tooltip}
            </div>
            <div class="table-cell date-switcher">
                <span id="date-switcher" class="button">{show}</span>
            </div>
        </div>""".format(date=uc_first(_('date')), tooltip=display_tooltip(_('tooltip date')),
                         show=uc_first(_('show')))
    html += '<div class="table-row date-switch" ' + style + '>'
    html += '<div>' + uc_first(_('birth') if for_person else _('begin')) + '</div>'
    html += '<div class="table-cell">'
    html += str(form.begin_year_from(class_='year')) + ' ' + errors['begin_year_from'] + ' '
    html += str(form.begin_month_from(class_='month')) + ' ' + errors['begin_month_from'] + ' '
    html += str(form.begin_day_from(class_='day')) + ' ' + errors['begin_day_from'] + ' '
    html += str(form.begin_comment)
    html += '</div></div>'
    html += '<div class="table-row date-switch" ' + style + '>'
    html += '<div></div><div class="table-cell">'
    html += str(form.begin_year_to(class_='year')) + ' ' + errors['begin_year_to'] + ' '
    html += str(form.begin_month_to(class_='month')) + ' ' + errors['begin_month_to'] + ' '
    html += str(form.begin_day_to(class_='day')) + ' ' + errors['begin_day_to'] + ' '
    html += '</div></div>'
    html += '<div class="table-row date-switch" ' + style + '>'
    html += '<div>' + uc_first(_('death') if for_person else _('end')) + '</div>'
    html += '<div class="table-cell">'
    html += str(form.end_year_from(class_='year')) + ' ' + errors['end_year_from'] + ' '
    html += str(form.end_month_from(class_='month')) + ' ' + errors['end_month_from'] + ' '
    html += str(form.end_day_from(class_='day')) + ' ' + errors['end_day_from'] + ' '
    html += str(form.end_comment)
    html += '</div></div>'
    html += '<div class="table-row date-switch"' + style + '>'
    html += '<div></div><div class="table-cell">'
    html += str(form.end_year_to(class_='year')) + ' ' + errors['end_year_to'] + ' '
    html += str(form.end_month_to(class_='month')) + ' ' + errors['end_month_to'] + ' '
    html += str(form.end_day_to(class_='day')) + ' ' + errors['end_day_to'] + ' '
    html += '</div></div>'
    return html


def required_group(group):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login', next=request.path))
            if not is_authorized(group):
                abort(403)
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def bookmark_toggle(entity_id, for_table=False):
    label = uc_first(_('bookmark'))
    if entity_id in current_user.bookmarks:
        label = uc_first(_('bookmark remove'))
    if for_table:
        html = """<a id="bookmark{entity_id}" onclick="ajaxBookmark('{entity_id}');"
            style="cursor:pointer;">{label}</a>""".format(entity_id=entity_id, label=label)
    else:
        html = """<button id="bookmark{entity_id}" onclick="ajaxBookmark('{entity_id}');"
            type="button">{label}</button>""".format(entity_id=entity_id, label=label)
    return html


def is_authorized(group):
    if not current_user.is_authenticated or not hasattr(current_user, 'group'):
        return False
    if current_user.group == 'admin' or (
            current_user.group == 'manager' and group in ['manager', 'editor', 'readonly']) or (
            current_user.group == 'editor' and group in ['editor', 'readonly']) or (
            current_user.group == 'readonly' and group == 'readonly'):
        return True
    return False


def uc_first(string):
    if not string:
        return ''
    return str(string)[0].upper() + str(string)[1:]


def format_datetime(value, format_='medium'):
    return dates.format_datetime(value, format=format_, locale=session['language']) if value else ''


def format_date(value, format_='medium'):
    # Todo: handle NaT values
    if not value:
        return ''
    if type(value) is numpy.datetime64:
        return DateMapper.datetime64_to_timestamp(value)
    return dates.format_date(value, format=format_, locale=session['language'])


def get_profile_image_table_link(file, entity, extension, profile_image_id):
    if file.id == profile_image_id:
        url = url_for('file_remove_profile_image', entity_id=entity.id)
        return '<a href="' + url + '">' + uc_first(_('unset')) + '</a>'
    elif extension in app.config['DISPLAY_FILE_EXTENSIONS']:
        url = url_for('file_set_as_profile_image', id_=file.id, origin_id=entity.id)
        return '<a href="' + url + '">' + uc_first(_('set')) + '</a>'
    return ''  # pragma: no cover - only happens for non image files


def link(entity):
    # Builds an html link to entity view for display
    from openatlas.models.entity import Entity
    if not entity:
        return ''
    html = ''
    if type(entity) is Project:
        url = url_for('import_project_view', id_=entity.id)
        html = '<a href="' + url + '">' + entity.name + '</a>'
    elif type(entity) is User:
        style = '' if entity.active else 'class="inactive"'
        url = url_for('user_view', id_=entity.id)
        html = '<a ' + style + ' href="' + url + '">' + entity.username + '</a>'
    elif type(entity) is ClassObject:
        url = url_for('class_view', code=entity.code)
        html = '<a href="' + url + '">' + entity.code + '</a>'
    elif type(entity) is Property:
        url = url_for('property_view', code=entity.code)
        html = '<a href="' + url + '">' + entity.code + '</a>'
    elif type(entity) is Entity:
        url = ''
        if entity.class_.code == 'E33':
            if entity.system_type == 'source content':
                url = url_for('source_view', id_=entity.id)
            elif entity.system_type == 'source translation':
                url = url_for('translation_view', id_=entity.id)
        elif entity.system_type == 'file':
            url = url_for('file_view', id_=entity.id)
        elif entity.class_.code in ('E7', 'E8', 'E12', 'E6'):
            url = url_for('event_view', id_=entity.id)
        elif entity.class_.code in ('E21', 'E74', 'E40'):
            url = url_for('actor_view', id_=entity.id)
        elif entity.class_.code in ('E18', 'E22'):
            url = url_for('place_view', id_=entity.id)
        elif entity.class_.code in ('E31', 'E84'):
            url = url_for('reference_view', id_=entity.id)
        elif entity.class_.code in ['E55', 'E53']:
            url = url_for('node_view', id_=entity.id)
            if not entity.root:
                url = url_for('node_index') + '#tab-' + str(entity.id)
        if entity.class_.code == 'E61':
            return entity.name
        if not url:
            return entity.name + ' (' + entity.class_.name + ')'
        return '<a href="' + url + '">' + truncate_string(entity.name) + '</a>'
    return html


def truncate_string(string, length=40, span=True):
    """
    Returns a truncates string with '..' at the end if it was longer than length
    Also adds a span title (for mouse over) with the original string if parameter "span" is True
    """
    if string is None:
        return ''  # pragma: no cover
    if len(string) < length + 1:
        return string
    if not span:
        return string[:length] + '..'
    return '<span title="' + string.replace('"', '') + '">' + string[:length] + '..' + '</span>'


def pager(table, remove_rows=True):
    if not table['data']:
        return '<p>' + uc_first(_('no entries')) + '</p>'
    html = ''
    table_rows = session['settings']['default_table_rows']
    if hasattr(current_user, 'settings'):
        table_rows = current_user.settings['table_rows']
    show_pager = table['show_pager'] if 'show_pager' in table else True
    if show_pager:
        options = ''
        for amount in app.config['DEFAULT_TABLE_ROWS']:
            options += '<option value="{amount}"{selected}>{amount}</option>'.format(
                amount=amount, selected=' selected="selected"' if amount == table_rows else '')
        placeholder = uc_first(_('type to search'))
        if int(session['settings']['minimum_tablesorter_search']) > 1:  # pragma: no cover
            placeholder += ' (' + _('min %(limit)s chars',
                                    limit=session['settings']['minimum_tablesorter_search']) + ')'
        html += """
            <div id="{id}-pager" class="pager">
                <div class="navigation first"></div>
                <div class="navigation prev"></div>
                <div class="pagedisplay">
                    <input class="pagedisplay" type="text" disabled="disabled">
                </div>
                <div class="navigation next"></div>
                <div class="navigation last"></div>
                <div><select class="pagesize">{options}</select></div>
                <input id="{id}-search" class="search" type="text" data-column="all"
                    placeholder="{placeholder}">
            </div><div style="clear:both;"></div>
            """.format(id=table['id'], options=options, placeholder=placeholder)
    html += '<table id="{id}-table" class="tablesorter"><thead><tr>'.format(id=table['id'])
    for header in table['header']:
        style = '' if header else 'class=sorter-false '  # only show and sort headers with a title
        html += '<th ' + style + '>' + (uc_first(_(header)) if header else '') + '</th>'
    # Append missing headers
    html += '<th class=sorter-false></th>' * (len(table['data'][0]) - len(table['header']))
    html += '</tr></thead><tbody>'
    for row in table['data']:
        html += '<tr>'
        for entry in row:
            entry = str(entry) if (entry and entry != 'None') or entry == 0 else ''
            try:
                float(entry.replace(',', ''))
                style = ' style="text-align:right;"'  # pragma: no cover
            except ValueError:
                style = ''
            html += '<td' + style + '>' + entry + '</td>'
        html += '</tr>'
    html += '</tbody></table><script>'
    sort = '' if 'sort' not in table else table['sort'] + ','
    if show_pager:
        html += """
            $("#{id}-table").tablesorter({{
                {headers}
                {sort}
                dateFormat: "ddmmyyyy",
                widgets: ["filter", "zebra"],
                widgetOptions: {{
                    filter_liveSearch: {filter_liveSearch},
                    filter_external: "#{id}-search",
                    filter_columnFilters: false
                }}}})
            .tablesorterPager({{
                delayInit: true,
                {remove_rows}
                positionFixed: false,
                container: $("#{id}-pager"),
                size:{size}}});
        """.format(id=table['id'], sort=sort, size=table_rows,
                   remove_rows='removeRows: true,' if remove_rows else '',
                   filter_liveSearch=session['settings']['minimum_tablesorter_search'],
                   headers=(table['headers'] + ',') if 'headers' in table else '')
    else:
        html += """
            $("#{id}-table").tablesorter({{
                {sort}
                widgets: ["filter", "zebra"],
                widgetOptions: {{
                    filter_liveSearch: {filter_liveSearch},
                    filter_external: "#{id}-search",
                    filter_columnFilters: false
                }}}});
        """.format(id=table['id'], sort=sort,
                   filter_liveSearch=session['settings']['minimum_jstree_search'])
    html += '</script>'
    return html


def get_base_table_data(entity, file_stats=None):
    """ Returns standard table data for an entity"""
    data = [link(entity)]
    if entity.view_name in ['event', 'actor']:
        data.append(g.classes[entity.class_.code].name)
    if entity.view_name in ['reference'] and entity.system_type != 'file':
        data.append(uc_first(_(entity.system_type)))
    if entity.view_name in ['event', 'place', 'source', 'reference', 'file']:
        data.append(entity.print_base_type())
    if entity.system_type == 'file':
        if file_stats:
            data.append(convert_size(
                file_stats[entity.id]['size']) if entity.id in file_stats else 'N/A')
            data.append(
                file_stats[entity.id]['ext'] if entity.id in file_stats else 'N/A')
        else:
            data.append(print_file_size(entity))
            data.append(print_file_extension(entity))
    if entity.view_name in ['event', 'actor', 'place']:
        data.append(format_date(entity.first))
        data.append(format_date(entity.last))
    if entity.view_name in ['source'] or entity.system_type == 'file':
        data.append(truncate_string(entity.description))
    return data


def was_modified(form, entity):  # pragma: no cover
    """ Checks if an entity was modified after an update form was opened."""
    if not entity.modified or not form.opened.data:
        return False
    if entity.modified < datetime.fromtimestamp(float(form.opened.data)):
        return False
    openatlas.logger.log('info', 'multi user', 'Multi user overwrite prevented.')
    return True
