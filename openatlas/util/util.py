# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask_babel import lazy_gettext as _
from openatlas.models.classObject import ClassObject
from openatlas.models.property import Property


def uc_first(string):
    new_string = _(string)
    return new_string[0].upper() + new_string[1:]


def link(entity):  # pragma: no cover
    if not entity:
        return ''
    if isinstance(entity, ClassObject):
        return '<a href="/model/class_view/' + str(entity.id) + '">' + entity.code + '</a>'
    elif isinstance(entity, Property):
        return '<a href="/model/property_view/' + str(entity.id) + '">' + entity.code + '</a>'
    return entity.name + ' (' + entity.class_.name + ')'
