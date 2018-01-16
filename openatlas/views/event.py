# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import flash, render_template, url_for, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

import openatlas
from openatlas import app
from openatlas.forms.forms import DateForm, build_form, TableField, TableMultiField
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper, Link
from openatlas.util.util import (required_group, truncate_string, get_entity_data, uc_first,
                                 build_remove_link, get_base_table_data, link, is_authorized,
                                 was_modified)


class EventForm(DateForm):
    name = StringField(_('name'), [DataRequired()])
    event = TableField(_('sub event of'))
    place = TableField(_('location'))
    event_id = HiddenField()
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()
    # acquisition
    recipient = TableMultiField()
    donor = TableMultiField()
    given_place = TableMultiField()

    def validate(self, extra_validators=None):
        """Check if selected super event is allowed"""
        # Todo: also check if super is not a sub event of itself (recursively)
        valid = DateForm.validate(self)
        if self.event.data:
            if str(self.event.data) == str(self.event_id.data):
                self.event.errors.append(_('error node self as super'))
                valid = False
        return valid


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
    if code != 'E8':
        del form.recipient, form.donor, form.given_place
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        result = save(form, None, code, origin)
        if not result:  # pragma: no cover
            return render_template('event/insert.html', form=form, code=code, origin=origin)
        flash(_('entity created'), 'info')
        if isinstance(result, Link) and result.property_code == 'P67':
            return redirect(url_for('reference_link_update', link_id=result, origin_id=origin_id))
        if form.continue_.data == 'yes':
            return redirect(url_for('event_insert', code=code, origin_id=origin_id))
        if origin:
            if origin.class_.code in app.config['CLASS_CODES']['actor']:
                return redirect(url_for('involvement_update', id_=result, origin_id=origin_id))
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-event')
        return redirect(url_for('event_view', id_=result.id))
    return render_template('event/insert.html', form=form, code=code, origin=origin)


@app.route('/event/delete/<int:id_>')
@required_group('editor')
def event_delete(id_):
    openatlas.get_cursor().execute('BEGIN')
    try:
        EntityMapper.delete(id_)
        openatlas.logger.log_user(id_, 'delete')
        openatlas.get_cursor().execute('COMMIT')
        flash(_('entity deleted'), 'info')
    except Exception as e:  # pragma: no cover
        openatlas.get_cursor().execute('ROLLBACK')
        openatlas.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    return redirect(url_for('event_index'))


@app.route('/event/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def event_update(id_):
    event = EntityMapper.get_by_id(id_)
    event.set_dates()
    form = build_form(EventForm, 'Event', event, request)
    if event.class_.code != 'E8':
        del form.recipient, form.donor, form.given_place
    form.event_id.data = event.id
    if form.validate_on_submit():
        if was_modified(form, event):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = openatlas.logger.get_log_for_advanced_view(event.id)['modifier_name']
            return render_template('event/update.html', form=form, event=event, modifier=modifier)
        if save(form, event):
            flash(_('info update'), 'info')
        return redirect(url_for('event_view', id_=id_))
    super_event = event.get_linked_entity('P117')
    form.event.data = super_event.id if super_event else ''
    place = event.get_linked_entity('P7')
    form.place.data = place.get_linked_entity('P53', True).id if place else ''
    if event.class_.code == 'E8':  # Form data for acquisition
        form.recipient.data = [entity.id for entity in event.get_linked_entities('P22')]
        form.donor.data = [entity.id for entity in event.get_linked_entities('P23')]
        form.given_place.data = [entity.id for entity in event.get_linked_entities('P24')]
    return render_template('event/update.html', form=form, event=event)


@app.route('/event/view/<int:id_>')
@app.route('/event/view/<int:id_>/<int:unlink_id>')
@required_group('readonly')
def event_view(id_, unlink_id=None):
    event = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
        flash(_('link removed'), 'info')
    event.set_dates()
    tables = {
        'info': get_entity_data(event),
        'actor': {
            'name': 'actor',
            'header': ['actor', 'class', 'involvement', 'first', 'last', 'description'],
            'data': []}}
    for link_ in event.get_links(['P11', 'P14', 'P22', 'P23']):
        first = link_.first
        if not link_.first and event.first:
            first = '<span class="inactive" style="float:right">' + str(event.first) + '</span>'
        last = link_.last
        if not link_.last and event.last:
            last = '<span class="inactive" style="float:right">' + str(event.last) + '</span>'
        data = ([
            link(link_.range),
            openatlas.classes[link_.range.class_.code].name,
            link_.type.name if link_.type else '',
            first,
            last,
            truncate_string(link_.description)])
        if is_authorized('editor'):
            unlink_url = url_for('event_view', id_=event.id, unlink_id=link_.id) + '#tab-actor'
            update_url = url_for('involvement_update', id_=link_.id, origin_id=event.id)
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(build_remove_link(unlink_url, link_.range.name))
        tables['actor']['data'].append(data)
    tables['source'] = {
        'name': 'source',
        'header': app.config['TABLE_HEADERS']['source'] + ['description'],
        'data': []}
    tables['reference'] = {
        'name': 'reference',
        'header': app.config['TABLE_HEADERS']['reference'] + ['pages'],
        'data': []}
    for link_ in event.get_links('P67', True):
        name = app.config['CODE_CLASS'][link_.domain.class_.code]
        data = get_base_table_data(link_.domain)
        if name == 'source':
            data.append(truncate_string(link_.domain.description))
        else:
            data.append(truncate_string(link_.description))
            if is_authorized('editor'):
                update_url = url_for('reference_link_update', link_id=link_.id, origin_id=event.id)
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('editor'):
            unlink_url = url_for('event_view', id_=event.id, unlink_id=link_.id) + '#tab-' + name
            data.append(build_remove_link(unlink_url, link_.domain.name))
        tables[name]['data'].append(data)
    tables['subs'] = {
        'name': 'sub-event',
        'header': app.config['TABLE_HEADERS']['event'],
        'data': []}
    for sub_event in event.get_linked_entities('P117', True):
        tables['subs']['data'].append(get_base_table_data(sub_event))
    return render_template('event/view.html', event=event, tables=tables)


def save(form, event=None, code=None, origin=None):
    openatlas.get_cursor().execute('BEGIN')
    try:
        if event:
            LinkMapper.delete_by_codes(event, ['P117', 'P7', 'P22', 'P23', 'P24'])
            openatlas.logger.log_user(event.id, 'update')
        else:
            event = EntityMapper.insert(code, form.name.data)
            openatlas.logger.log_user(event.id, 'insert')
        event.name = form.name.data
        event.description = form.description.data
        event.update()
        event.save_dates(form)
        event.save_nodes(form)
        if form.event.data:
            event.link('P117', int(form.event.data))
        if form.place.data:
            place = LinkMapper.get_linked_entity(int(form.place.data), 'P53')
            event.link('P7', place)
        if event.class_.code == 'E8':  # Links for acquisition
            event.link('P22', ast.literal_eval(form.recipient.data) if form.recipient.data else None)
            event.link('P23', ast.literal_eval(form.donor.data) if form.donor.data else None)
            if form.given_place.data:
                event.link('P24', ast.literal_eval(form.given_place.data))
        link_ = None
        if origin:
            if origin.class_.code in app.config['CLASS_CODES']['reference']:
                link_ = origin.link('P67', event)
            elif origin.class_.code in app.config['CLASS_CODES']['source']:
                origin.link('P67', event)
            elif origin.class_.code in app.config['CLASS_CODES']['actor']:
                link_ = event.link('P11', origin)
        openatlas.get_cursor().execute('COMMIT')
    except Exception as e:  # pragma: no cover
        openatlas.get_cursor().execute('ROLLBACK')
        openatlas.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        return
    return link_ if link_ else event
