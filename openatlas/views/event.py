# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, render_template, url_for, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import (link, required_group, truncate_string, append_node_data,
                                 build_delete_link, build_remove_link)


class EventForm(DateForm):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/event')
@required_group('readonly')
def event_index():
    tables = {'event': {
        'name': 'event',
        'header': [_('name'), _('class'), _('type'), _('first'), _('last'), _('info')],
        'data': []}}
    for event in EntityMapper.get_by_codes('event'):
        tables['event']['data'].append([
            link(event),
            openatlas.classes[event.class_.id].name,
            event.print_base_type(),
            format(event.first),
            format(event.last),
            truncate_string(event.description)])
    return render_template('event/index.html', tables=tables)


@app.route('/event/insert/<code>', methods=['POST', 'GET'])
@app.route('/event/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def event_insert(code, origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = build_form(EventForm, 'Event')
    if form.validate_on_submit() and form.name.data != app.config['EVENT_ROOT_NAME']:
        event = save(form, None, code, origin)
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('event_insert', code=code, origin_id=origin_id))
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-event')
        return redirect(url_for('event_view', id_=event.id))
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
    tables['source'] = {'name': 'source', 'header': ['name', 'type', 'info', ''], 'data': []}
    for link_ in event.get_links('P67', True):
        name = app.config['CODE_CLASS'][link_.domain.class_.code]
        entity = link_.domain
        unlink_url = url_for('event_view', id_=event.id, unlink_id=link_.id) + '#tab-' + name
        tables['source']['data'].append([
            link(entity),
            entity.print_base_type(),
            truncate_string(entity.description),
            build_remove_link(unlink_url, entity.name)])
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
    if origin:
        origin.link('P67', entity)
    openatlas.get_cursor().execute('COMMIT')
    return entity
