# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import url_for

from openatlas.models.classObject import ClassObject
from openatlas.models.entity import Entity
from openatlas.models.property import Property


def uc_first(string):
    if not string:
        return ''
    return str(string)[0].upper() + str(string)[1:]


def link(entity):
    if not entity:
        return ''
    if isinstance(entity, ClassObject):
        return '<a href="' + url_for('class_view', class_id=entity.id) + '">' + entity.code + '</a>'
    elif isinstance(entity, Property):
        return '<a href="' + url_for('property_view', property_id=entity.id) + '">' + entity.code + '</a>'
    elif isinstance(entity, Entity):
        # To do: what if translation or the like?
        if entity.class_.code == 'E33':
            return '<a href="' + url_for('source_view', source_id=entity.id) + '">' + entity.name + '</a>'
    return entity.name + ' (' + entity.class_.name + ')'


def truncate_string(string, length=40, encoding='utf-8'):
    if string is None:
        return ''  # pragma: no cover
    string = string.encode(encoding)
    title = string.replace('"', '')
    string = '<span title="' + title + '">' + string[:length] + '..</span>' if len(string) > length + 2 else string
    return string.decode(encoding, 'ignore')
