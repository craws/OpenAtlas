# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import re
import smtplib
from collections import OrderedDict
from datetime import timedelta, date, datetime
from functools import wraps

from babel import dates
from flask import abort, url_for, request, session, flash
from flask_login import current_user
from flask_babel import lazy_gettext as _
from html.parser import HTMLParser
from werkzeug.utils import redirect

import openatlas
from openatlas import app
from openatlas.models.classObject import ClassObject
from openatlas.models.entity import Entity, EntityMapper
from openatlas.models.property import Property
from openatlas.models.user import User


def send_mail(subject, text, recipients, log_body=True):  # pragma: no cover
    recipients = recipients if isinstance(recipients, list) else [recipients]
    if not session['settings']['mail'] or len(recipients) < 1:
        return
    sender = session['settings']['mail_transport_username']
    from_ = session['settings']['mail_from_name']
    from_ += ' <' + session['settings']['mail_from_email'] + '>'
    server = smtplib.SMTP(
        session['settings']['mail_transport_host'],
        session['settings']['mail_transport_port'])
    server.ehlo()
    server.starttls()
    try:
        server.login(sender, app.config['MAIL_PASSWORD'])
        for recipient in recipients:
            body = '\r\n'.join([
                'To: %s' % recipient.strip(),
                'From: %s' % from_,
                'Subject: %s' % subject,
                '', text])
            server.sendmail(sender, recipient, body)
        message = 'Mail send from for ' + from_ + ' to ' + ', '.join(recipients)
        message += ' Subject: ' + subject
        # Don't log sensitive data, e.g. passwords
        message += ' Content: ' + text if log_body else ''
        openatlas.logger.log('info', 'mail', 'Mail send from ' + sender, message)
    except smtplib.SMTPAuthenticationError as e:
        openatlas.logger.log('error', 'mail', 'Error mail login for ' + sender, str(e))
        flash(_('error mail login'), 'error')
        return False
    except Exception as e:
        openatlas.logger.log('error', 'mail', 'Error send mail for ' + sender, str(e))
        flash(_('error mail send'), 'error')
        return False
    return True


class MLStripper(HTMLParser):

    def error(self, message):
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
        """Remove all characters from a string except ASCII letters and numbers"""
        return re.sub('[^A-Za-z0-9]+', '', string)
    if mode == 'node':
        """Remove all characters from a string except letters, numbers and spaces"""
        return re.sub(r'([^\s\w]|_)+', '', string).strip()
    if mode == 'description':
        s = MLStripper()
        s.feed(string)
        return s.get_data()


def build_table_form(class_name, linked_entities):
    """Returns a form with a list of entities with checkboxes"""
    # Todo: add CSRF token
    form = '<form class="table" method="post">'
    header = app.config['TABLE_HEADERS'][class_name] + ['']
    table = {'name': class_name, 'header': header, 'data': []}
    linked_ids = [entity.id for entity in linked_entities]
    for entity in EntityMapper.get_by_codes(class_name):
        if entity.id in linked_ids:
            continue  # don't show already linked entries
        input_ = '<input id="{id}" name="values" type="checkbox" value="{id}">'.format(id=entity.id)
        table['data'].append(get_base_table_data(entity) + [input_])
    if not table['data']:
        return uc_first(_('no entries'))
    form += pager(table)
    form += '<button name="form-submit" id="form-submit" type="submit">'
    form += uc_first(_('add')) + '</button></form>'
    return form


def build_remove_link(url, name):
    """Build a link to remove a link with a JavaScript confirmation dialog"""
    name = name.replace('\'', '')
    confirm = 'onclick="return confirm(\'' + _('Remove %(name)s?', name=name) + '\')"'
    return '<a ' + confirm + ' href="' + url + '">' + uc_first(_('remove')) + '</a>'


def get_entity_data(entity, location=None):
    """
    Return related entity information for a table for view.
    The location parameter is for places which have a location attached.
    """
    data = []
    # Nodes
    type_data = OrderedDict()
    nodes = entity.nodes + (location.nodes if location else [])
    for node in nodes:
        if not node.root:
            continue
        root = openatlas.nodes[node.root[-1]]
        name = 'type' if root.name in app.config['BASE_TYPES'] else root.name
        if root.name not in type_data:
            type_data[name] = []
        type_data[name].append(node.name)
    type_data = OrderedDict(sorted(type_data.items(), key=lambda t: t[0]))  # sort by name
    if 'type' in type_data:  # move the base type to the top
        type_data.move_to_end('type', last=False)
    for root_name, nodes in type_data.items():
        data.append((root_name, '<br />'.join(nodes)))

    # Info for places
    if entity.class_.code in app.config['CLASS_CODES']['place']:
        aliases = entity.get_linked_entities('P1')
        if aliases:
            data.append((uc_first(_('alias')), '<br />'.join([x.name for x in aliases])))

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
            recipients = entity.get_linked_entities('P22')
            if recipients:
                html = ''
                for recipient in recipients:
                    html += link(recipient) + '<br />'
                data.append((uc_first(_('recipient')), html))
            donors = entity.get_linked_entities('P23')
            if donors:
                html = ''
                for donor in donors:
                    html += link(donor) + '<br />'
                data.append((uc_first(_('donor')), html))
            given_places = entity.get_linked_entities('P24')
            if given_places:
                html = ''
                for given_place in given_places:
                    html += link(given_place) + '<br />'
                data.append((uc_first(_('given place')), html))

    # Info for actors
    if entity.class_.code in app.config['CLASS_CODES']['actor']:
        aliases = entity.get_linked_entities('P131')
        if aliases:
            data.append((uc_first(_('alias')), '<br />'.join([x.name for x in aliases])))

    # Dates
    date_types = OrderedDict([
        ('OA1', _('first')),
        ('OA3', _('birth')),
        ('OA2', _('last')),
        ('OA4', _('death')),
        ('OA5', _('begin')),
        ('OA6', _('end'))])
    for code, label in date_types.items():
        if code in entity.dates:
            if 'exact date value' in entity.dates[code]:
                html = format_date(entity.dates[code]['exact date value']['timestamp'])
                html += ' ' + entity.dates[code]['exact date value']['info']
                data.append((uc_first(label), html))
            else:
                html = uc_first(_('between')) + ' '
                html += format_date(entity.dates[code]['from date value']['timestamp'])
                html += ' and ' + format_date(entity.dates[code]['to date value']['timestamp'])
                html += ' ' + entity.dates[code]['from date value']['info']
                data.append((uc_first(label), html))

    # Additional info for advanced layout
    if hasattr(current_user, 'settings') and current_user.settings['layout'] == 'advanced':
        data.append((uc_first(_('class')), link(entity.class_)))
        user_log = openatlas.logger.get_log_for_advanced_view(entity.id)
        created = format_date(entity.created) if entity.modified else ''
        if user_log['creator_id']:
            created = format_date(user_log['created']) + ' ' + user_log['creator_name']
        data.append((_('created'), created))
        modified = format_date(entity.modified) if entity.modified else None
        if user_log['modifier_id']:
            modified = format_date(user_log['modified']) + ' ' + user_log['modifier_name']
        if modified:
            data.append((_('modified'), modified))

    return data


def add_dates_to_form(form, for_person=False):
    html = """
        <div class="table-row">
            <div>
                <label>{date}</label> <span class="tooltip" title="{tip}">i</span>
            </div>
            <div class="table-cell date-switcher">
                <span id="date-switcher" class="button">{show}</span>
            </div>
        </div>""".format(date=uc_first(_('date')), tip=_('tooltip date'), show=uc_first(_('show')))
    html += '<div class="table-row date-switch">'
    html += '<div>' + str(form.date_begin_year.label) + '</div><div class="table-cell">'
    html += str(form.date_begin_year(class_='year')) + ' '
    html += str(form.date_begin_month(class_='month')) + ' '
    html += str(form.date_begin_day(class_='day')) + ' '
    html += str(form.date_begin_info())
    html += '</div></div>'
    html += '<div class="table-row date-switch">'
    html += '<div></div><div class="table-cell">'
    html += str(form.date_begin_year2(class_='year')) + ' '
    html += str(form.date_begin_month2(class_='month')) + ' '
    html += str(form.date_begin_day2(class_='day')) + ' '
    if for_person:
        html += str(form.date_birth) + str(form.date_birth.label)
    html += '</div></div>'
    html += '<div class="table-row date-switch">'
    html += '<div>' + str(form.date_end_year.label) + '</div><div class="table-cell">'
    html += str(form.date_end_year(class_='year')) + ' '
    html += str(form.date_end_month(class_='month')) + ' '
    html += str(form.date_end_day(class_='day')) + ' '
    html += str(form.date_end_info())
    html += '</div></div>'
    html += '<div class="table-row date-switch">'
    html += '<div></div><div class="table-cell">'
    html += str(form.date_end_year2(class_='year')) + ' '
    html += str(form.date_end_month2(class_='month')) + ' '
    html += str(form.date_end_day2(class_='day')) + ' '
    if for_person:
        html += str(form.date_death) + str(form.date_death.label)
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
    if group not in ['admin', 'manager', 'editor', 'readonly']:
        return False
    if group == 'admin' and current_user.group != 'admin':
        return False
    if group == 'manager' and current_user.group not in ['admin', 'manager']:
        return False
    if group == 'editor' and current_user.group not in ['admin', 'manager', 'editor']:
        return False
    if group == 'readonly' and current_user.group not in ['admin', 'manager', 'editor', 'readonly']:
        return False
    return True


def uc_first(string):
    if not string:
        return ''
    return str(string)[0].upper() + str(string)[1:]


def format_datetime(value, format_='medium'):
    return dates.format_datetime(value, format=format_, locale=session['language']) if value else ''


def format_date(value, format_='medium'):
    return dates.format_date(value, format=format_, locale=session['language']) if value else ''


def link(entity):
    if not entity:
        return ''
    html = ''
    if isinstance(entity, User):
        style = '' if entity.active else 'class="inactive"'
        url = url_for('user_view', id_=entity.id)
        html = '<a ' + style + ' href="' + url + '">' + entity.username + '</a>'
    elif isinstance(entity, ClassObject):
        url = url_for('class_view', code=entity.code)
        html = '<a href="' + url + '">' + entity.code + '</a>'
    elif isinstance(entity, Property):
        url = url_for('property_view', code=entity.code)
        html = '<a href="' + url + '">' + entity.code + '</a>'
    elif isinstance(entity, Entity):
        url = ''
        if entity.class_.code == 'E33':
            if entity.system_type == 'source content':
                url = url_for('source_view', id_=entity.id)
            elif entity.system_type == 'source translation':
                url = url_for('translation_view', id_=entity.id)
        elif entity.class_.code in ('E7', 'E8', 'E12', 'E6'):
            url = url_for('event_view', id_=entity.id)
        elif entity.class_.code in ('E21', 'E74', 'E40'):
            url = url_for('actor_view', id_=entity.id)
        elif entity.class_.code == 'E18':
            url = url_for('place_view', id_=entity.id)
        elif entity.class_.code in ('E31', 'E84'):
            url = url_for('reference_view', id_=entity.id)
        elif entity.class_.code in ['E55', 'E53']:
            url = url_for('node_view', id_=entity.id)
            if not entity.root:
                url = url_for('node_index') + '#tab-' + str(entity.id)
        if entity.class_.code == 'E61':
            return format_date(entity.timestamp)
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


def create_date_from_form(form_date, postfix=''):
    date_ = date(
        form_date['year' + postfix],
        form_date['month' + postfix] if form_date['month' + postfix] else 1,
        1)
    if form_date['day' + postfix]:  # add days to date to prevent errors for e.g. February 31
        date_ += timedelta(days=form_date['day' + postfix]-1)
    return date_


def pager(table):
    if not table['data']:
        return '<p>' + uc_first(_('no entries')) + '</p>'
    html = ''
    table_rows = session['settings']['default_table_rows']
    if hasattr(current_user, 'settings'):
        table_rows = current_user.settings['table_rows']
    show_pager = False if len(table['data']) < table_rows else True
    if show_pager:
        options = ''
        for amount in app.config['DEFAULT_TABLE_ROWS']:
            options += '<option value="{amount}"{selected}>{amount}</option>'.format(
                amount=amount, selected=' selected="selected"' if amount == table_rows else '')
        html += """
            <div id="{name}-pager" class="pager">
                <div class="navigation first"></div>
                <div class="navigation prev"></div>
                <div class="pagedisplay">
                    <input class="pagedisplay" type="text" disabled="disabled">
                </div>
                <div class="navigation next"></div>
                <div class="navigation last"></div>
                <div><select class="pagesize">{options}</select></div>
                <input id="{name}-search" class="search" type="text" data-column="all"
                    placeholder="{filter}">
            </div><div style="clear:both;"></div>
            """.format(name=table['name'], filter=uc_first(_('filter')), options=options)
    html += '<table id="{name}-table" class="tablesorter"><thead><tr>'.format(name=table['name'])
    for header in table['header']:
        style = '' if header else 'class=sorter-false '  # only show and sort headers with a title
        html += '<th ' + style + '>' + (_(header).capitalize() if header else '') + '</th>'
    # append missing headers
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
            $("#{name}-table").tablesorter({{
                {headers}
                {sort}
                dateFormat: "ddmmyyyy",
                widgets: [\'zebra\', \'filter\'],
                widgetOptions: {{
                    filter_external: \'#{name}-search\',
                    filter_columnFilters: false
                }}}})
            .tablesorterPager({{positionFixed: false, container: $("#{name}-pager"), size:{size}}});
        """.format(
            name=table['name'],
            sort=sort,
            size=table_rows,
            headers='' if 'headers' not in table else table['headers'] + ',')
    else:
        html += '$("#' + table['name'] + '-table").tablesorter({' + sort + 'widgets:[\'zebra\']});'
    html += '</script>'
    return html


def get_base_table_data(entity):
    """Returns standard table data for an entity"""
    name = app.config['CODE_CLASS'][entity.class_.code]
    data = [link(entity)]
    if name in ['event', 'actor']:
        data.append(openatlas.classes[entity.class_.code].name)
    if name in ['reference']:
        data.append(uc_first(_(entity.system_type)))
    if name in ['event', 'place', 'source', 'reference']:
        data.append(entity.print_base_type())
    if name in ['event', 'actor', 'place']:
        data.append(format(entity.first))
        data.append(format(entity.last))
    return data


def was_modified(form, entity):   # pragma: no cover
    """Checks if an entity was modified after an update form was opened."""
    if not entity.modified or not form.opened.data:
        return False
    if entity.modified < datetime.fromtimestamp(float(form.opened.data)):
        return False
    openatlas.logger.log('info', 'multi user', 'Multi user overwrite prevented.')
    return True
