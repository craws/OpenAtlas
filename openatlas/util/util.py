# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask_babel import lazy_gettext as _
from openatlas.models.classObject import ClassObject


def uc_first(string):
    new_string = _(string)
    return new_string[0].upper() + new_string[1:]


def link(entity):  # pragma: no cover
    if not entity:
        return ''
    if isinstance(entity, ClassObject):
        return '<a href="/model/class_view/' + str(entity.id) + '">' + entity.code + ' ' + entity.name_translated + '</a>'
    return entity.name + ' (' + entity.class_.name + ')'
