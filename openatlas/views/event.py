from typing import Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.date import DateForm
from openatlas.forms.forms import TableField, TableMultiField, build_form
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.table import Table
from openatlas.util.util import get_base_table_data, link, required_group, uc_first, was_modified
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
@app.route('/event/<action>/<int:id_>')
@required_group('readonly')
def event_index(action: Optional[str] = None, id_: Optional[int] = None) -> str:
    if id_ and action == 'delete':
        Entity.delete_(id_)
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
    table = Table(Table.HEADERS['event'] + ['description'],
                  defs=[{'className': 'dt-body-right', 'targets': [3, 4]}])
    for event in Entity.get_by_codes('event'):
        data = get_base_table_data(event)
        data.append(event.description)
        table.rows.append(data)
    return render_template('event/index.html', table=table)


def prepare_form(form: EventForm, code: str) -> FlaskForm:
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
def event_insert(code: str, origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
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


@app.route('/event/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def event_update(id_: int) -> Union[str, Response]:
    event = Entity.get_by_id(id_, nodes=True, view_name='event')
    form = prepare_form(build_form(EventForm, 'Event', event, request), event.class_.code)
    form.event_id.data = event.id
    if form.validate_on_submit():
        if was_modified(form, event):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(event.id)['modifier'])
            return render_template('event/update.html', form=form, event=event, modifier=modifier)
        save(form, event)
        return redirect(url_for('entity_view', id_=id_))
    super_event = event.get_linked_entity('P117')
    form.event.data = super_event.id if super_event else ''
    if event.class_.code == 'E9':  # Form data for move
        place_from = event.get_linked_entity('P27')
        form.place_from.data = place_from.get_linked_entity_safe('P53',
                                                                 True).id if place_from else ''
        place_to = event.get_linked_entity('P26')
        form.place_to.data = place_to.get_linked_entity_safe('P53', True).id if place_to else ''
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
        form.place.data = place.get_linked_entity_safe('P53', True).id if place else ''
    if event.class_.code == 'E8':  # Form data for acquisition
        form.given_place.data = [entity.id for entity in event.get_linked_entities('P24')]
    return render_template('event/update.html', form=form, event=event)


@app.route('/event/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def event_add_reference(id_: int) -> Union[str, Response]:
    event = Entity.get_by_id(id_, view_name='event')
    form = AddReferenceForm()
    if form.validate_on_submit():
        event.link_string('P67', form.reference.data, description=form.page.data, inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-reference')
    form.page.label.text = uc_first(_('page / link text'))
    return render_template('add_reference.html', entity=event, form=form)


def save(form: FlaskForm,
         event: Optional[Entity] = None,
         code: Optional[str] = None,
         origin: Optional[Entity] = None) -> str:
    g.cursor.execute('BEGIN')
    try:
        log_action = 'insert'
        if event:
            log_action = 'update'
            event.delete_links(['P7', 'P24', 'P25', 'P26', 'P27', 'P117'])
        elif code:
            event = Entity.insert(code, form.name.data)
        else:
            abort(400)  # pragma: no cover, either event or code has to be provided
        event.update(form)
        if form.event.data:
            event.link_string('P117', form.event.data)
        if form.place and form.place.data:
            event.link('P7', Link.get_linked_entity_safe(int(form.place.data), 'P53'))
        if event.class_.code == 'E8' and form.given_place.data:  # Link place for acquisition
            event.link_string('P24', form.given_place.data)
        if event.class_.code == 'E9':  # Move
            if form.object.data:  # Moved objects
                event.link_string('P25', form.object.data)
            if form.person.data:  # Moved persons
                event.link_string('P25', form.person.data)
            if form.place_from.data:  # Link place for move from
                linked_place = Link.get_linked_entity_safe(int(form.place_from.data), 'P53')
                event.link('P27', linked_place)
            if form.place_to.data:  # Link place for move to
                event.link('P26', Link.get_linked_entity_safe(int(form.place_to.data), 'P53'))
        url = url_for('entity_view', id_=event.id)
        if origin:
            url = url_for('entity_view', id_=origin.id) + '#tab-event'
            if origin.view_name == 'reference':
                link_id = origin.link('P67', event)[0]
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif origin.view_name == 'source':
                origin.link('P67', event)
            elif origin.view_name == 'actor':
                link_id = event.link('P11', origin)[0]
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
