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
from openatlas.models.link import LinkMapper
from openatlas.util.util import (link, truncate_string, required_group, append_node_data,
                                 build_delete_link, build_remove_link)


class ActorForm(DateForm):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/actor/view/<int:id_>')
@app.route('/actor/view/<int:id_>/<int:unlink_id>')
@required_group('readonly')
def actor_view(id_, unlink_id=None):
    actor = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
    actor.set_dates()
    tables = {'info': []}
    append_node_data(tables['info'], actor)
    delete_link = build_delete_link(url_for('actor_delete', id_=actor.id), actor.name)
    tables['source'] = {'name': 'source', 'header': ['name', 'type', 'info', ''], 'data': []}
    for link_ in actor.get_links('P67', True):
        name = app.config['CODE_CLASS'][link_.domain.class_.code]
        entity = link_.domain
        unlink_url = url_for('actor_view', id_=actor.id, unlink_id=link_.id) + '#tab-' + name
        tables['source']['data'].append([
            link(entity),
            entity.print_base_type(),
            truncate_string(entity.description),
            build_remove_link(unlink_url, entity.name)])
    return render_template('actor/view.html', actor=actor, tables=tables, delete_link=delete_link)


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
@app.route('/actor/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def actor_insert(code, origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    forms = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, forms[code])
    if form.validate_on_submit():
        actor = save(form, None, code, origin)
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('actor_insert', code=code, origin_id=origin_id))
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-actor')
        return redirect(url_for('actor_view', id_=actor.id))
    return render_template('actor/insert.html', form=form, code=code, origin=origin)


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


def save(form, entity=None, code=None, origin=None):
    openatlas.get_cursor().execute('BEGIN')
    entity = entity if entity else EntityMapper.insert(code, form.name.data)
    entity.name = form.name.data
    entity.description = form.description.data
    entity.update()
    entity.save_dates(form)
    entity.save_nodes(form)
    if origin:
        origin.link('P67', entity)
    openatlas.get_cursor().execute('COMMIT')
    return entity
