# Created by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict

from flask import flash, g, render_template, request, session, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import BooleanField, SelectField, StringField, SubmitField
from wtforms.validators import Email, InputRequired

from openatlas import app, logger
from openatlas.models.settings import SettingsMapper
from openatlas.util.util import required_group, send_mail, uc_first








