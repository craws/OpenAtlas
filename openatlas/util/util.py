# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import url_for
from markupsafe import Markup
from datetime import datetime

from openatlas.models.classObject import ClassObject
from openatlas.models.entity import Entity
from openatlas.models.property import Property


def uc_first(string):
    if not string:
        return ''
    return str(string)[0].upper() + str(string)[1:]


def format_date(value, formatstring='%Y-%m-%d'):
    if not value:
        return 'Never'
    try:
        return datetime.strftime(value, formatstring)
    except:
        return "Invalid date: {} for format:{}".format(value, formatstring)


def link(entity):
    if not entity:
        return ''
    if isinstance(entity, ClassObject):
        return Markup('<a href="' + url_for('class_view', class_id=entity.id) + '">' + entity.code + '</a>')
    elif isinstance(entity, Property):
        return Markup('<a href="' + url_for('property_view', property_id=entity.id) + '">' + entity.code + '</a>')
    elif isinstance(entity, Entity):
        # To do: what if translation or the like?
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
    return Markup(entity.name + ' (' + entity.class_.name + ')')


def truncate_string(string, length=40, encoding='utf-8'):
    if string is None:
        return ''  # pragma: no cover
    string = string.encode(encoding)
    title = string.replace('"', '')
    string = '<span title="' + title + '">' + string[:length] + '..</span>' if len(string) > length + 2 else string
    return string.decode(encoding, 'ignore')
