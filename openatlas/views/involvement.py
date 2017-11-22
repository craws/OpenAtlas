# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import flash, render_template, url_for, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app, PropertyMapper
from openatlas.forms import DateForm, build_form, TableMultiField, TreeField
from openatlas.models.entity import EntityMapper, Entity
from openatlas.models.link import LinkMapper
from openatlas.util.util import (required_group, truncate_string, append_node_data,
                                 build_delete_link, build_remove_link, get_base_table_data,
                                 uc_first, link)


class ActorForm(DateForm):
    actor = TableMultiField(_('actor'), validators=[InputRequired()])
    involvement = TreeField()
    activity = SelectField(_('activity'))
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/involvement/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def involvement_insert(origin_id):
    origin = EntityMapper.get_by_id(origin_id)
    form = ActorForm()
    if origin.class_.code in ['E6', 'E7', 'E8', 'E12']:
        form.activity.choices = [('P11', PropertyMapper.get_by_code('P11').name)]
        if origin.class_.code in ['E7', 'E8', 'E12']:
            form.activity.choices.append(('P14', PropertyMapper.get_by_code('P14').name))
        if origin.class_.code == 'E8':
            form.activity.choices.append(('P22', PropertyMapper.get_by_code('P22').name))
            form.activity.choices.append(('P23', PropertyMapper.get_by_code('P23').name))
    if form.validate_on_submit():
        if origin.class_.code in ['E6', 'E7', 'E8', 'E12']:
            openatlas.get_cursor().execute('BEGIN')
            origin.link(form.activity.data, ast.literal_eval(form.actor.data))
            openatlas.get_cursor().execute('COMMIT')
            flash(_('entity created'), 'info')
            return redirect(url_for('event_view', id_=origin.id) + '#tab-actor')

    return render_template('involvement/insert.html', origin=origin, form=form)


@app.route('/involvement/update/<int:id_><int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def involvement_update(id_, origin_id):
    return render_template('involvement/update.html')
