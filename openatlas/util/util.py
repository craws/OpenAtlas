# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import re
from functools import wraps

import babel
from flask import abort, url_for, request, session
from flask_login import current_user
from flask_babel import lazy_gettext as _
from markupsafe import Markup

from werkzeug.utils import redirect
from openatlas.models.classObject import ClassObject
from openatlas.models.entity import Entity
from openatlas.models.property import Property
from openatlas.models.user import User


def sanitize(string):
    return re.sub('[^A-Za-z0-9]+', '', string)


def add_dates_to_form(form):
    html = '''
        <div class="table-row">
            <div><label>{date}</label> <span class="tooltip" title="{tip}">i</span></div>
            <div class="table-cell date-switcher"><span id="date-switcher" class="button">{show}</span></div>
        </div>'''.format(date=uc_first(_('date')), tip=_('tooltip date'), show=uc_first(_('show')))
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


def bookmark_toggle(entity_id):
    html = '<button id="bookmark' + str(entity_id) + '" type="button" onclick="ajaxBookmark(' + str(entity_id) + ');">'
    html += uc_first(_('bookmark remove')) if entity_id in current_user.bookmarks else uc_first(_('bookmark'))
    html += '</button>'
    return Markup(html)


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


def format_date(value):
    if not value:
        return ''
    return babel.dates.format_date(value, locale=session['language'])


def link(entity):
    if not entity:
        return ''
    if isinstance(entity, User):
        style = '' if entity.active else 'class="inactive"'
        html = '<a ' + style + ' href="' + url_for('user_view', user_id=entity.id) + '">' + entity.username + '</a>'
        return Markup(html)
    if isinstance(entity, ClassObject):
        return Markup('<a href="' + url_for('class_view', class_id=entity.id) + '">' + entity.code + '</a>')
    elif isinstance(entity, Property):
        return Markup('<a href="' + url_for('property_view', property_id=entity.id) + '">' + entity.code + '</a>')
    elif isinstance(entity, Entity):
        # To do: what if E33 is a translation  or the like?
        if entity.class_.code == 'E33':
            return Markup('<a href="' + url_for('source_view', source_id=entity.id) + '">' + entity.name + '</a>')
        if entity.class_.code in ('E7', 'E8', 'E12', 'E6'):
            return Markup('<a href="' + url_for('event_view', event_id=entity.id) + '">' + entity.name + '</a>')
        if entity.class_.code in ('E21', 'E74', 'E40'):
            return Markup('<a href="' + url_for('actor_view', actor_id=entity.id) + '">' + entity.name + '</a>')
        if entity.class_.code == 'E18':
            return Markup('<a href="' + url_for('place_view', place_id=entity.id) + '">' + entity.name + '</a>')
        if entity.class_.code in ('E31', 'E84'):
            return Markup('<a href="' + url_for('reference_view', reference_id=entity.id) + '">' + entity.name + '</a>')
        if entity.class_.code == 'E55':
            return Markup('<a href="' + url_for('node_view', node_id=entity.id) + '">' + entity.name + '</a>')
    return Markup(entity.name + ' (' + entity.class_.name + ')')


def truncate_string(string, length=40):
    if string is None:
        return ''  # pragma: no cover
    title = string.replace('"', '')
    string = '<span title="' + title + '">' + string[:length] + '..</span>' if len(string) > length + 2 else string
    return string
