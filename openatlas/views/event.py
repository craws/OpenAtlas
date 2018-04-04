# Created by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from openatlas import app, logger
from openatlas.forms.forms import DateForm, TableField, TableMultiField, build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import (display_remove_link, get_base_table_data, get_entity_data,
                                 get_view_name, is_authorized, link, required_group,
                                 truncate_string, uc_first, was_modified)


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
    table = {'id': 'event', 'header': header, 'data': []}
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
        return redirect(save(form, code=code, origin=origin))
    return render_template('event/insert.html', form=form, code=code, origin=origin)


@app.route('/event/delete/<int:id_>')
@required_group('editor')
def event_delete(id_):
    g.cursor.execute('BEGIN')
    try:
        EntityMapper.delete(id_)
        logger.log_user(id_, 'delete')
        g.cursor.execute('COMMIT')
        flash(_('entity deleted'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
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
            modifier = link(logger.get_log_for_advanced_view(event.id)['modifier'])
            return render_template('event/update.html', form=form, event=event, modifier=modifier)
        save(form, event)
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
        'file': {'id': 'files', 'data': [], 'header': app.config['TABLE_HEADERS']['file']},
        'subs': {'id': 'sub-event', 'data': [], 'header': app.config['TABLE_HEADERS']['event']},
        'actor': {
            'id': 'actor', 'data': [],
            'header': ['actor', 'class', 'involvement', 'first', 'last', 'description']},
        'source': {
            'id': 'source', 'data': [],
            'header': app.config['TABLE_HEADERS']['source'] + ['description']},
        'reference': {
            'id': 'reference', 'data': [],
            'header': app.config['TABLE_HEADERS']['reference'] + ['pages']}}
    for link_ in event.get_links(['P11', 'P14', 'P22', 'P23']):
        first = link_.first
        if not link_.first and event.first:
            first = '<span class="inactive" style="float:right">' + str(event.first) + '</span>'
        last = link_.last
        if not link_.last and event.last:
            last = '<span class="inactive" style="float:right">' + str(event.last) + '</span>'
        data = ([
            link(link_.range),
            g.classes[link_.range.class_.code].name,
            link_.type.name if link_.type else '',
            first,
            last,
            truncate_string(link_.description)])
        if is_authorized('editor'):
            unlink_url = url_for('event_view', id_=event.id, unlink_id=link_.id) + '#tab-actor'
            update_url = url_for('involvement_update', id_=link_.id, origin_id=event.id)
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, link_.range.name))
        tables['actor']['data'].append(data)
    for link_ in event.get_links('P67', True):
        data = get_base_table_data(link_.domain)
        view_name = get_view_name(link_.domain)
        if view_name not in ['source', 'file']:
            data.append(truncate_string(link_.description))
            if is_authorized('editor'):
                update_url = url_for('reference_link_update', link_id=link_.id, origin_id=event.id)
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('editor'):
            unlink = url_for('event_view', id_=event.id, unlink_id=link_.id) + '#tab-' + view_name
            data.append(display_remove_link(unlink, link_.domain.name))
        tables[view_name]['data'].append(data)
    for sub_event in event.get_linked_entities('P117', True):
        tables['subs']['data'].append(get_base_table_data(sub_event))
    return render_template('event/view.html', event=event, tables=tables)


def save(form, event=None, code=None, origin=None):
    g.cursor.execute('BEGIN')
    try:
        log_action = 'update'
        if event:
            LinkMapper.delete_by_codes(event, ['P117', 'P7', 'P22', 'P23', 'P24'])
        else:
            log_action = 'insert'
            event = EntityMapper.insert(code, form.name.data)
        event.name = form.name.data
        event.description = form.description.data
        event.update()
        event.save_dates(form)
        event.save_nodes(form)
        url = url_for('event_view', id_=event.id)
        if form.event.data:
            event.link('P117', int(form.event.data))
        if form.place.data:
            place = LinkMapper.get_linked_entity(int(form.place.data), 'P53')
            event.link('P7', place)
        if event.class_.code == 'E8':  # Links for acquisition
            if form.recipient.data:
                event.link('P22', ast.literal_eval(form.recipient.data))
            event.link('P23', ast.literal_eval(form.donor.data) if form.donor.data else None)
            if form.given_place.data:
                event.link('P24', ast.literal_eval(form.given_place.data))
        if origin:
            view_name = get_view_name(origin)
            url = url_for(view_name + '_view', id_=origin.id) + '#tab-event'
            if view_name == 'reference':
                link_id = origin.link('P67', event)
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif view_name == 'source':
                origin.link('P67', event)
            elif view_name == 'actor':
                link_id = event.link('P11', origin)
                url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
            elif view_name == 'file':
                origin.link('P67', event)
        if form.continue_.data == 'yes':
            url = url_for('event_insert', code=code, origin_id=origin.id if origin else None)
        g.cursor.execute('COMMIT')
        logger.log_user(event.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('event_index')
    return url
