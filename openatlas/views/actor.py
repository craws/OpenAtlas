# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_form
from openatlas.models.entity import EntityMapper
from openatlas.util.util import link, truncate_string, required_group, append_node_data


class ActorForm(DateForm):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/actor/view/<int:id_>')
@required_group('readonly')
def actor_view(id_):
    actor = EntityMapper.get_by_id(id_)
    actor.set_dates()
    data = {'info': []}
    append_node_data(data['info'], actor)
    return render_template('actor/view.html', actor=actor, data=data)


@app.route('/actor')
@required_group('readonly')
def actor_index():
    tables = {'actor': {
        'name': 'actor',
        'header': [_('name'), _('class'), _('first'), _('last'), _('info')],
        'data': []}}
    for actor in EntityMapper.get_by_codes('actor'):
        tables['actor']['data'].append([
            link(actor),
            openatlas.classes[actor.class_.id].name,
            actor.first,
            actor.last,
            truncate_string(actor.description)])
    return render_template('actor/index.html', tables=tables)


@app.route('/actor/insert/<code>', methods=['POST', 'GET'])
@required_group('editor')
def actor_insert(code):
    forms = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, forms[code])
    if form.validate_on_submit():
        actor = save(form, EntityMapper.insert(code, form.name.data))
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('actor_insert', code=code))
        return redirect(url_for('actor_view', id_=actor.id))
    return render_template('actor/insert.html', form=form, code=code)


@app.route('/actor/delete/<int:id_>')
@required_group('editor')
def actor_delete(id_):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(id_)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('actor_index'))


@app.route('/actor/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def actor_update(id_):
    actor = EntityMapper.get_by_id(id_)
    actor.set_dates()
    forms = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, forms[actor.class_.code], actor, request)
    if form.validate_on_submit():
        save(form, actor)
        flash(_('info update'), 'info')
        return redirect(url_for('actor_view', id_=id_))
    return render_template('actor/update.html', form=form, actor=actor)


def save(form, entity):
    openatlas.get_cursor().execute('BEGIN')
    entity.name = form.name.data
    entity.description = form.description.data
    entity.update()
    entity.save_dates(form)
    entity.save_nodes(form)
    openatlas.get_cursor().execute('COMMIT')
    return entity
