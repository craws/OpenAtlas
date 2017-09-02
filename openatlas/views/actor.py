# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.util.util import uc_first, link, truncate_string, required_group


class ActorForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('description')))
    continue_ = HiddenField()


@app.route('/actor/view/<int:actor_id>')
@required_group('readonly')
def actor_view(actor_id):
    actor = EntityMapper.get_by_id(actor_id)
    data = {'info': [
        (_('name'), actor.name),
    ]}
    return render_template('actor/view.html', actor=actor, data=data)


@app.route('/actor')
@required_group('readonly')
def actor_index():
    tables = {'actor': {
        'name': 'actor',
        # 'sort': 'sortList: [[3, 1]]',
        'header': ['name', 'class', 'info'],
        'data': []}}
    for actor in EntityMapper.get_by_codes(['E21', 'E74', 'E40']):
        tables['actor']['data'].append([
            link(actor),
            openatlas.classes[actor.class_.id].name,
            truncate_string(actor.description)
        ])
    return render_template('actor/index.html', tables=tables)


@app.route('/actor/insert/<code>', methods=['POST', 'GET'])
@required_group('editor')
def actor_insert(code):
    form = ActorForm()
    if form.validate_on_submit():
        actor = EntityMapper.insert(code, form.name.data, form.description.data)
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('actor_insert', code=code))
        return redirect(url_for('actor_view', actor_id=actor.id))
    return render_template('actor/insert.html', form=form, code=code)


@app.route('/actor/delete/<int:actor_id>')
@required_group('editor')
def actor_delete(actor_id):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(actor_id)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('actor_index'))


@app.route('/actor/update/<int:actor_id>', methods=['POST', 'GET'])
@required_group('editor')
def actor_update(actor_id):
    actor = EntityMapper.get_by_id(actor_id)
    form = ActorForm()
    if form.validate_on_submit():
        actor.name = form.name.data
        actor.description = form.description.data
        actor.update()
        flash(_('info update'), 'info')
        return redirect(url_for('actor_view', actor_id=actor.id))
    form.name.data = actor.name
    form.description.data = actor.description
    return render_template('actor/update.html', form=form, actor=actor)
