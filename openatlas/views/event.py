# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, render_template, url_for, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_form
from openatlas.models.entity import EntityMapper, Entity
from openatlas.models.link import LinkMapper
from openatlas.util.util import (required_group, truncate_string, append_node_data,
                                 build_delete_link, build_remove_link, get_base_table_data,
                                 uc_first, link)


class EventForm(DateForm):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/event')
@required_group('readonly')
def event_index():
    header = app.config['TABLE_HEADERS']['event'] + ['description']
    table = {'name': 'event', 'header': header, 'data': []}
    for event in EntityMapper.get_by_codes('event'):
        data = get_base_table_data(event)
        data.append(truncate_string(event.description))
        table['data'].append(data)
    return render_template('event/index.html', table=table)


@app.route('/event/insert/<code>', methods=['POST', 'GET'])
@app.route('/event/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def event_insert(code, origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = build_form(EventForm, 'Event')
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit() and form.name.data != app.config['EVENT_ROOT_NAME']:
        result = save(form, None, code, origin)
        flash(_('entity created'), 'info')
        if not isinstance(result, Entity):
            return redirect(url_for('reference_link_update', link_id=result, origin_id=origin_id))
        if form.continue_.data == 'yes':
            return redirect(url_for('event_insert', code=code, origin_id=origin_id))
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-event')
        return redirect(url_for('event_view', id_=result.id))
    return render_template('event/insert.html', form=form, code=code, origin=origin)


@app.route('/event/delete/<int:id_>')
@required_group('editor')
def event_delete(id_):
    if EntityMapper.get_by_id(id_).name == app.config['EVENT_ROOT_NAME']:
        flash(_('error forbidden'), 'error')
        return redirect(url_for('event_index'))
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(id_)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('event_index'))


@app.route('/event/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def event_update(id_):
    event = EntityMapper.get_by_id(id_)
    event.set_dates()
    form = build_form(EventForm, 'Event', event, request)
    if event.name == app.config['EVENT_ROOT_NAME']:
        flash(_('error forbidden'), 'error')
        return redirect(url_for('event_index'))
    if form.validate_on_submit() and form.name.data != app.config['EVENT_ROOT_NAME']:
        save(form, event)
        flash(_('info update'), 'info')
        return redirect(url_for('event_view', id_=id_))
    return render_template('event/update.html', form=form, event=event)


@app.route('/event/view/<int:id_>')
@app.route('/event/view/<int:id_>/<int:unlink_id>')
@required_group('readonly')
def event_view(id_, unlink_id=None):
    event = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
    event.set_dates()
    tables = {'info': []}
    append_node_data(tables['info'], event)
    tables['actor'] = {
        'name': 'actor',
        'header': app.config['TABLE_HEADERS']['actor'] + ['involvement', '', ''],
        'data': []}
    for link_ in event.get_links(['P11', 'P14', 'P22', 'P23']):
        tables['actor']['data'].append ([
            link(link_.range),
            openatlas.classes[link_.range.class_.id].name,
            'todo first',
            'todo last',
            'todo involvement',
            'todo edit',
            'todo delete'])
    tables['source'] = {
        'name': 'source',
        'header': app.config['TABLE_HEADERS']['source'] + ['description', ''],
        'data': []}
    tables['reference'] = {
        'name': 'reference',
        'header': app.config['TABLE_HEADERS']['reference'] + ['pages', '', ''],
        'data': []}
    for link_ in event.get_links('P67', True):
        name = app.config['CODE_CLASS'][link_.domain.class_.code]
        unlink_url = url_for('event_view', id_=event.id, unlink_id=link_.id) + '#tab-' + name
        data = get_base_table_data(link_.domain)
        if name == 'source':
            data.append(truncate_string(link_.domain.description))
        else:
            data.append(truncate_string(link_.description))
            update_url = url_for('reference_link_update', link_id=link_.id, origin_id=event.id)
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        data.append(build_remove_link(unlink_url, link_.domain.name))
        tables[name]['data'].append(data)
    delete_link = build_delete_link(url_for('event_delete', id_=event.id), event.name)
    return render_template('event/view.html', event=event, delete_link=delete_link, tables=tables)


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
