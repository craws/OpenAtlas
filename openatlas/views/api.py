# Created by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import DateForm, TableField, TableMultiField, build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.models.user import UserMapper
from openatlas.util.table import Table
from openatlas.util.util import (display_remove_link, get_base_table_data, get_entity_data,
                                 get_profile_image_table_link, is_authorized, link, required_group,
                                 truncate_string, uc_first, was_modified)


@app.route('/api/<version>/entity/<int:id_>')
@required_group('manager')
def api_entity(version: str, id_: int) -> str:

    return render_template('api/entity.html', version=version, id_=id_)


@app.route('/api')
@required_group('manager')
def api_index() -> str:

    return render_template('api/index.html')