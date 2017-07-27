# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template, url_for, flash
from flask_babel import gettext, lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.util.util import uc_first, link, truncate_string, required_group


class EventForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('description')))
    continue_ = HiddenField()


@app.route('/event/view/<int:event_id>')
@required_group('readonly')
def event_view(event_id):
    event = EntityMapper.get_by_id(event_id)
    return render_template('event/view.html', event=event)


@app.route('/event')
@required_group('readonly')
def event_index():
    tables = {'event': {
        'name': 'event',
        'header': [_('name'), _('class'), _('info')],
        'data': []}}
    for event in EntityMapper.get_by_codes(['E7', 'E8', 'E12', 'E6']):
        tables['event']['data'].append([
            link(event),
            openatlas.classes[event.class_.id].name,
            truncate_string(event.description)
        ])
    return render_template('event/index.html', tables=tables)


@app.route('/event/insert/<code>', methods=['POST', 'GET'])
@required_group('editor')
def event_insert(code):
    form = EventForm()
    if form.validate_on_submit() and form.name.data != openatlas.app.config['EVENT_ROOT_NAME']:
        event = EntityMapper.insert(code, form.name.data, form.description.data)
        flash(gettext('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('event_insert', code=code))
        return redirect(url_for('event_view', event_id=event.id))
    return render_template('event/insert.html', form=form, code=code)


@app.route('/event/delete/<int:event_id>')
@required_group('editor')
def event_delete(event_id):
    if EntityMapper.get_by_id(event_id).name == openatlas.app.config['EVENT_ROOT_NAME']:
        flash(gettext('error forbidden'), 'error')
        return redirect(url_for('event_index'))
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(event_id)
    openatlas.get_cursor().execute('COMMIT')
    flash(gettext('entity deleted'), 'info')
    return redirect(url_for('event_index'))


@app.route('/event/update/<int:event_id>', methods=['POST', 'GET'])
@required_group('editor')
def event_update(event_id):
    event = EntityMapper.get_by_id(event_id)
    form = EventForm()
    if event.name == openatlas.app.config['EVENT_ROOT_NAME']:
        flash(gettext('error forbidden'), 'error')
        return redirect(url_for('event_index'))
    if form.validate_on_submit() and form.name.data != openatlas.app.config['EVENT_ROOT_NAME']:
        event.name = form.name.data
        event.description = form.description.data
        event.update()
        flash(gettext('entity updated'), 'info')
        return redirect(url_for('event_view', event_id=event.id))
    form.name.data = event.name
    form.description.data = event.description
    return render_template('event/update.html', form=form, event=event)
