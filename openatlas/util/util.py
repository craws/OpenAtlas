# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask.ext.babel import lazy_gettext as _


def uc_first(string):
    new_string = _(string)
    return new_string[0].upper() + new_string[1:]
