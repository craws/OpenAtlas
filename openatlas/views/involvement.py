# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, render_template, url_for, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_form, TableMultiField, TreeField
from openatlas.models.entity import EntityMapper, Entity
from openatlas.models.link import LinkMapper
from openatlas.util.util import (required_group, truncate_string, append_node_data,
                                 build_delete_link, build_remove_link, get_base_table_data,
                                 uc_first, link)


class ActorForm(DateForm):
    actor = TableMultiField(_('actor'))
    involvement = TreeField()
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/involvement/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def involvement_insert(origin_id):
    origin = EntityMapper.get_by_id(origin_id)
    form = ActorForm()
    return render_template('involvement/insert.html', origin=origin, form=form)


@app.route('/involvement/update/<int:id_><int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def involvement_update(id_, origin_id):
    return render_template('involvement/update.html')
