# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, render_template, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_custom_form
from openatlas.models.entity import EntityMapper
from openatlas.util.util import link, required_group, truncate_string


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
        'header': [_('name'), _('class'), _('first'), _('last'), _('info')],
        'data': []}}
    for event in EntityMapper.get_by_codes(['E7', 'E8', 'E12', 'E6']):
        tables['event']['data'].append([
            link(event),
            openatlas.classes[event.class_.id].name,
            format(event.first),
            format(event.last),
            truncate_string(event.description)])
    return render_template('event/index.html', tables=tables)


@app.route('/event/insert/<code>', methods=['POST', 'GET'])
@required_group('editor')
def event_insert(code):
    nodes = {}
    for node_id in openatlas.node.NodeMapper.get_hierarchy_by_name('Date value type').subs:
        nodes[openatlas.nodes[node_id].name] = node_id
    form = build_custom_form(EventForm, 'Event')
    if form.validate_on_submit() and form.name.data != openatlas.app.config['EVENT_ROOT_NAME']:
        openatlas.get_cursor().execute('BEGIN')
        event = EntityMapper.insert(code, form.name.data, form.description.data)
        event.save_dates(form)
        openatlas.get_cursor().execute('COMMIT')
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('event_insert', code=code))
        return redirect(url_for('event_view', id_=event.id))
    return render_template('event/insert.html', form=form, code=code)


@app.route('/event/delete/<int:id_>')
@required_group('editor')
def event_delete(id_):
    if EntityMapper.get_by_id(id_).name == openatlas.app.config['EVENT_ROOT_NAME']:
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
    form = EventForm()
    if event.name == openatlas.app.config['EVENT_ROOT_NAME']:
        flash(_('error forbidden'), 'error')
        return redirect(url_for('event_index'))
    if form.validate_on_submit() and form.name.data != openatlas.app.config['EVENT_ROOT_NAME']:
        event.name = form.name.data
        event.description = form.description.data
        openatlas.get_cursor().execute('BEGIN')
        event.update()
        event.save_dates(form)
        openatlas.get_cursor().execute('COMMIT')
        flash(_('info update'), 'info')
        return redirect(url_for('event_view', id_=id_))
    form.name.data = event.name
    form.description.data = event.description
    form.populate_dates(event)
    return render_template('event/update.html', form=form, event=event)


@app.route('/event/view/<int:id_>')
@required_group('readonly')
def event_view(id_):
    event = EntityMapper.get_by_id(id_)
    event.set_dates()
    data = {'info': [(_('name'), event.name)]}
    return render_template('event/view.html', event=event, data=data)
