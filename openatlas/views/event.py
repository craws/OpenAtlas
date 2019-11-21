# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import (DateForm, TableField, TableMultiField, build_form,
                                   build_table_form)
from openatlas.models.entity import EntityMapper
from openatlas.models.gis import GisMapper
from openatlas.models.link import LinkMapper
from openatlas.models.user import UserMapper
from openatlas.util.table import Table
from openatlas.util.util import (display_remove_link, get_base_table_data, get_entity_data,
                                 get_profile_image_table_link, is_authorized, link, required_group,
                                 truncate_string, uc_first, was_modified)
from openatlas.views.reference import AddReferenceForm


class EventForm(DateForm):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    event = TableField(_('sub event of'))
    place = TableField(_('location'))
    place_from = TableField(_('from'))
    place_to = TableField(_('to'))
    object = TableMultiField()
    person = TableMultiField()
    event_id = HiddenField()
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()
    given_place = TableMultiField(_('given place'))

    def validate(self) -> bool:
        """ Check if selected super event is allowed."""
        # Todo: also check if super is not a sub event of itself (recursively)
        valid = DateForm.validate(self)
        if self.event.data:
            if str(self.event.data) == str(self.event_id.data):
                self.event.errors.append(_('error node self as super'))
                valid = False
        return valid


@app.route('/event')
@required_group('readonly')
def event_index() -> str:
    table = Table(Table.HEADERS['event'] + ['description'],
                  defs='[{className: "dt-body-right", targets: [3,4]}]')
    for event in EntityMapper.get_by_codes('event'):
        data = get_base_table_data(event)
        data.append(truncate_string(event.description))
        table.rows.append(data)
    return render_template('event/index.html', table=table)


def prepare_form(form: EventForm, code: str):
    if code != 'E8':
        del form.given_place
    if code == 'E9':
        del form.place
    else:
        del form.place_from
        del form.place_to
        del form.object
        del form.person
    return form


@app.route('/event/insert/<code>', methods=['POST', 'GET'])
@app.route('/event/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def event_insert(code: str, origin_id=None) -> Union[str, Response]:
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = prepare_form(build_form(EventForm, 'Event'), code)
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        return redirect(save(form, code=code, origin=origin))
    if origin:
        if origin.class_.code == 'E84':
            form.object.data = [origin.id]
        elif origin.class_.code == 'E18':
            if code == 'E9':
                form.place_from.data = origin.id
            else:
                form.place.data = origin.id
    return render_template('event/insert.html', form=form, code=code, origin=origin)


@app.route('/event/delete/<int:id_>')
@required_group('contributor')
def event_delete(id_: int) -> Response:
    EntityMapper.delete(id_)
    logger.log_user(id_, 'delete')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('event_index'))


@app.route('/event/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def event_update(id_: int) -> Union[str, Response]:
    event = EntityMapper.get_by_id(id_, nodes=True, view_name='event')
    form = prepare_form(build_form(EventForm, 'Event', event, request), event.class_.code)
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
    if event.class_.code == 'E9':  # Form data for move
        place_from = event.get_linked_entity('P27')
        form.place_from.data = place_from.get_linked_entity('P53', True).id if place_from else ''
        place_to = event.get_linked_entity('P26')
        form.place_to.data = place_to.get_linked_entity('P53', True).id if place_to else ''
        person_data = []
        object_data = []
        for entity in event.get_linked_entities('P25'):
            if entity.class_.code == 'E21':
                person_data.append(entity.id)
            elif entity.class_.code == 'E84':
                object_data.append(entity.id)
        form.person.data = person_data
        form.object.data = object_data
    else:
        place = event.get_linked_entity('P7')
        form.place.data = place.get_linked_entity('P53', True).id if place else ''
    if event.class_.code == 'E8':  # Form data for acquisition
        form.given_place.data = [entity.id for entity in event.get_linked_entities('P24')]
    return render_template('event/update.html', form=form, event=event)


@app.route('/event/view/<int:id_>')
@required_group('readonly')
def event_view(id_: int) -> str:
    event = EntityMapper.get_by_id(id_, nodes=True, view_name='event')
    event.note = UserMapper.get_note(event)
    tables = {'file': Table(Table.HEADERS['file'] + [_('main image')]),
              'subs': Table(Table.HEADERS['event']),
              'source': Table(Table.HEADERS['source']),
              'actor': Table(['actor', 'class', 'involvement', 'first', 'last', 'description'],
                             defs='[{className: "dt-body-right", targets: [3,4]}]'),
              'reference': Table(Table.HEADERS['reference'] + ['page / link text'])}
    for link_ in event.get_links(['P11', 'P14', 'P22', 'P23']):
        first = link_.first
        if not link_.first and event.first:
            first = '<span class="inactive" style="float:right;">' + event.first + '</span>'
        last = link_.last
        if not link_.last and event.last:
            last = '<span class="inactive" style="float:right;">' + event.last + '</span>'
        data = ([link(link_.range),
                 g.classes[link_.range.class_.code].name,
                 link_.type.name if link_.type else '',
                 first, last,
                 truncate_string(link_.description)])
        if is_authorized('contributor'):
            update_url = url_for('involvement_update', id_=link_.id, origin_id=event.id)
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=event.id) + '#tab-actor'
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, link_.range.name))
        tables['actor'].rows.append(data)
    profile_image_id = event.get_profile_image_id()
    for link_ in event.get_links('P67', True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':
            extension = data[3].replace('.', '')
            data.append(get_profile_image_table_link(domain, event, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if domain.view_name not in ['source', 'file']:
            if domain.system_type == 'external reference':
                event.external_references.append(link_)
            data.append(truncate_string(link_.description))
            if is_authorized('contributor'):
                url = url_for('reference_link_update', link_id=link_.id, origin_id=event.id)
                data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=event.id)
            data.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name].rows.append(data)
    for sub_event in event.get_linked_entities('P117', inverse=True, nodes=True):
        tables['subs'].rows.append(get_base_table_data(sub_event))
    objects = []
    for location in event.get_linked_entities(['P7', 'P26', 'P27']):
        objects.append(location.get_linked_entity('P53', True))
    return render_template('event/view.html', event=event, tables=tables,
                           info=get_entity_data(event), profile_image_id=profile_image_id,
                           gis_data=GisMapper.get_all(objects) if objects else None)


@app.route('/event/add/source/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def event_add_source(id_: int) -> Union[str, Response]:
    event = EntityMapper.get_by_id(id_, view_name='event')
    if request.method == 'POST':
        if request.form['checkbox_values']:
            event.link('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('event_view', id_=id_) + '#tab-source')
    form = build_table_form('source', event.get_linked_entities('P67', inverse=True))
    return render_template('add_source.html', entity=event, form=form)


@app.route('/event/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def event_add_reference(id_: int) -> Union[str, Response]:
    event = EntityMapper.get_by_id(id_, view_name='event')
    form = AddReferenceForm()
    if form.validate_on_submit():
        event.link('P67', form.reference.data, description=form.page.data, inverse=True)
        return redirect(url_for('event_view', id_=id_) + '#tab-reference')
    form.page.label.text = uc_first(_('page / link text'))
    return render_template('add_reference.html', entity=event, form=form)


@app.route('/event/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def event_add_file(id_: int) -> Union[str, Response]:
    event = EntityMapper.get_by_id(id_, view_name='event')
    if request.method == 'POST':
        if request.form['checkbox_values']:
            event.link('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('event_view', id_=id_) + '#tab-file')
    form = build_table_form('file', event.get_linked_entities('P67', inverse=True))
    return render_template('add_file.html', entity=event, form=form)


def save(form: FlaskForm, event=None, code: str = None, origin=None) -> str:
    g.cursor.execute('BEGIN')
    try:
        log_action = 'insert'
        if event:
            log_action = 'update'
            event.delete_links(['P7', 'P24', 'P25', 'P26', 'P27', 'P117'])
        else:
            event = EntityMapper.insert(code, form.name.data)
        event.name = form.name.data
        event.description = form.description.data
        event.set_dates(form)
        event.update()
        event.save_nodes(form)
        if form.event.data:
            event.link('P117', int(form.event.data))
        if form.place and form.place.data:
            event.link('P7', LinkMapper.get_linked_entity(int(form.place.data), 'P53'))
        if event.class_.code == 'E8' and form.given_place.data:  # Link place for acquisition
            event.link('P24', form.given_place.data)
        if event.class_.code == 'E9':  # Move
            if form.object.data:  # Moved objects
                event.link('P25', form.object.data)
            if form.person.data:  # Moved persons
                event.link('P25', form.person.data)
            if form.place_from.data:  # Link place for move from
                event.link('P27', LinkMapper.get_linked_entity(int(form.place_from.data), 'P53'))
            if form.place_to.data:  # Link place for move to
                event.link('P26', LinkMapper.get_linked_entity(int(form.place_to.data), 'P53'))
        url = url_for('event_view', id_=event.id)
        if origin:
            url = url_for(origin.view_name + '_view', id_=origin.id) + '#tab-event'
            if origin.view_name == 'reference':
                link_id = origin.link('P67', event)
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif origin.view_name == 'source':
                origin.link('P67', event)
            elif origin.view_name == 'actor':
                link_id = event.link('P11', origin)
                url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
            elif origin.view_name == 'file':
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
