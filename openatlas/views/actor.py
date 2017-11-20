# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_form
from openatlas.models.entity import EntityMapper, Entity
from openatlas.models.link import LinkMapper
from openatlas.util.util import (truncate_string, required_group, append_node_data,
                                 build_delete_link, build_remove_link, get_base_table_data,
                                 uc_first)


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
    tables['source'] = {
        'name': 'source',
        'header': app.config['TABLE_HEADERS']['source'] + ['description', ''],
        'data': []}
    tables['reference'] = {
        'name': 'reference',
        'header': app.config['TABLE_HEADERS']['reference'] + ['pages', '', ''],
        'data': []}
    for link_ in actor.get_links('P67', True):
        name = app.config['CODE_CLASS'][link_.domain.class_.code]
        unlink_url = url_for('actor_view', id_=actor.id, unlink_id=link_.id) + '#tab' + name
        data = get_base_table_data(link_.domain)
        if name == 'source':
            data.append(truncate_string(link_.domain.description))
        else:
            data.append(truncate_string(link_.description))
            update_url = url_for('reference_link_update', link_id=link_.id, origin_id=actor.id)
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        data.append(build_remove_link(unlink_url, link_.domain.name))
        tables[name]['data'].append(data)
    delete_link = build_delete_link(url_for('actor_delete', id_=actor.id), actor.name)
    return render_template('actor/view.html', actor=actor, tables=tables, delete_link=delete_link)


@app.route('/actor')
@required_group('readonly')
def actor_index():
    header = app.config['TABLE_HEADERS']['actor'] + ['description']
    table = {'name': 'actor', 'header': header, 'data': []}
    for actor in EntityMapper.get_by_codes('actor'):
        data = get_base_table_data(actor)
        data.append(truncate_string(actor.description))
        table['data'].append(data)
    return render_template('actor/index.html', table=table)


@app.route('/actor/insert/<code>', methods=['POST', 'GET'])
@app.route('/actor/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def actor_insert(code, origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    forms = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, forms[code])
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        result = save(form, None, code, origin)
        flash(_('entity created'), 'info')
        if not isinstance(result, Entity):
            return redirect(url_for('reference_link_update', link_id=result, origin_id=origin_id))
        if form.continue_.data == 'yes':
            return redirect(url_for('actor_insert', code=code, origin_id=origin_id))
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-actor')
        return redirect(url_for('actor_view', id_=result.id))
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
    link_ = None
    if origin:
        if origin.class_.code in app.config['CLASS_CODES']['reference']:
            link_ = origin.link('P67', entity)
        else:
            origin.link('P67', entity)
    openatlas.get_cursor().execute('COMMIT')
    return link_ if link_ else entity
