from typing import Any, List, Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.display import link, uc_first
from openatlas.util.util import required_group, was_modified


@app.route('/insert/<class_>', methods=['POST', 'GET'])
@app.route('/insert/<class_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def insert(class_: str, origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    if class_ in app.config['CLASS_CODES']['actor']:
        # Todo: can't use g.classes[class_].name because it's already translated, needs fixing.
        form_name = {'E21': 'person', 'E74': 'group', 'E40': 'legal_body'}
        form = build_form(form_name[class_], code=class_, origin=origin)
    elif class_ in app.config['CLASS_CODES']['event']:
        # Todo: it's inconsistently to actor that event has only one form for different classes.
        form = build_form('event', origin=origin, code=class_)
    else:
        form = build_form(class_, origin=origin)
    if form.validate_on_submit():
        return redirect(save(form, class_=class_, origin=origin))
    if hasattr(form, 'alias'):
        form.alias.append_entry('')
    view_name = app.config['CODE_CLASS'][class_] if class_ in g.classes else _(class_)
    if origin:
        populate_insert_form(form, view_name, class_, origin)
    return render_template('entity/insert.html',
                           form=form,
                           crumb=get_crumb(view_name, class_, origin),
                           class_=class_,
                           origin=origin,
                           view_name=view_name)


def get_crumb(view_name: str, class_: str, origin: Union[Entity, None]) -> List[Any]:
    if origin:
        name = '+ ' + (g.classes[class_].name if class_ in g.classes else uc_first(_(class_)))
        return [[_(origin.view_name), url_for('index', class_=origin.view_name)], origin, name]
    return [[_(view_name), url_for('index', class_=view_name)],
            '+ ' + (g.classes[class_].name if class_ in g.classes else uc_first(_(class_)))]


@app.route('/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def update(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_, nodes=True, aliases=True)
    if entity.view_name == 'actor':
        form = build_form(g.classes[entity.class_.code].name.lower().replace(' ', '_'), entity)
    else:
        form = build_form(entity.view_name, entity)
    if entity.view_name == 'event':
        form.event_id.data = entity.id
    if form.validate_on_submit():
        if was_modified(form, entity):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            return render_template(
                'entity/update.html',
                form=form,
                entity=entity,
                modifier=link(logger.get_log_for_advanced_view(entity.id)['modifier']))
        return redirect(save(form, entity))
    populate_update_form(form, entity)
    return render_template('entity/update.html',
                           form=form,
                           entity=entity,
                           crumb=[[_(entity.view_name), url_for('index', class_=entity.view_name)],
                                  link(entity),
                                  _('edit')])


def populate_insert_form(form: FlaskForm, view_name: str, class_: str, origin: Entity) -> None:
    if view_name == 'actor':
        if origin.system_type == 'place':
            form.residence.data = origin.id
    elif view_name == 'event':
        if origin.class_.code == 'E84':
            form.object.data = [origin.id]
        elif origin.class_.code == 'E18':
            if class_ == 'E9':
                form.place_from.data = origin.id
            else:
                form.place.data = origin.id


def populate_update_form(form: FlaskForm, entity: Entity) -> None:
    if entity.view_name == 'actor':
        residence = entity.get_linked_entity('P74')
        form.residence.data = residence.get_linked_entity_safe('P53', True).id if residence else ''
        first = entity.get_linked_entity('OA8')
        form.begins_in.data = first.get_linked_entity_safe('P53', True).id if first else ''
        last = entity.get_linked_entity('OA9')
        form.ends_in.data = last.get_linked_entity_safe('P53', True).id if last else ''
        for alias in entity.aliases.values():
            form.alias.append_entry(alias)
        form.alias.append_entry('')
    elif entity.view_name == 'event':
        super_event = entity.get_linked_entity('P117')
        form.event.data = super_event.id if super_event else ''
        if entity.class_.code == 'E9':  # Form data for move
            place_from = entity.get_linked_entity('P27')
            form.place_from.data = place_from.get_linked_entity_safe('P53',
                                                                     True).id if place_from else ''
            place_to = entity.get_linked_entity('P26')
            form.place_to.data = place_to.get_linked_entity_safe('P53', True).id if place_to else ''
            person_data = []
            object_data = []
            for entity in entity.get_linked_entities('P25'):
                if entity.class_.code == 'E21':
                    person_data.append(entity.id)
                elif entity.class_.code == 'E84':
                    object_data.append(entity.id)
            form.person.data = person_data
            form.object.data = object_data
        else:
            place = entity.get_linked_entity('P7')
            form.place.data = place.get_linked_entity_safe('P53', True).id if place else ''
        if entity.class_.code == 'E8':  # Form data for acquisition
            form.given_place.data = [entity.id for entity in entity.get_linked_entities('P24')]
    elif entity.view_name == 'source':
        form.information_carrier.data = [item.id for item in
                                         entity.get_linked_entities('P128', inverse=True)]


def save(form: FlaskForm,
         entity: Optional[Entity] = None,
         class_: Optional[str] = '',
         origin: Optional[Entity] = None) -> Union[str, Response]:
    g.cursor.execute('BEGIN')
    action = 'update'
    try:
        if not entity:
            action = 'insert'
            if class_ == 'source':
                entity = Entity.insert('E33', form.name.data, 'source content')
            else:
                entity = Entity.insert(class_, form.name.data)
        entity.update(form)
        update_links(entity, form, action)
        url = get_redirect_url(form, entity, class_, origin)
        logger.log_user(entity.id, action)
        g.cursor.execute('COMMIT')
        flash(_('entity created') if action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        if action == 'update':
            url = url_for('insert', class_=class_, origin_id=origin.id if origin else None)
        else:
            url = url_for(url_for('entity_index', class_=entity.view_name))
    return url


def update_links(entity: Entity, form, action: str) -> None:
    # Todo: it would be better to only save changes and not delete/recreate all links

    if entity.view_name in ['actor', 'event']:
        ReferenceSystem.update_links(form, entity)

    if entity.view_name == 'actor':
        if action == 'update':
            entity.delete_links(['P74', 'OA8', 'OA9'])
        if form.residence.data:
            object_ = Entity.get_by_id(form.residence.data, view_name='place')
            entity.link('P74', object_.get_linked_entity_safe('P53'))
        if form.begins_in.data:
            object_ = Entity.get_by_id(form.begins_in.data, view_name='place')
            entity.link('OA8', object_.get_linked_entity_safe('P53'))
        if form.ends_in.data:
            object_ = Entity.get_by_id(form.ends_in.data, view_name='place')
            entity.link('OA9', object_.get_linked_entity_safe('P53'))
    if entity.view_name == 'event':
        if action == 'update':
            entity.delete_links(['P7', 'P24', 'P25', 'P26', 'P27', 'P117'])
        if form.event.data:
            entity.link_string('P117', form.event.data)
        if hasattr(form, 'place') and form.place.data:
            entity.link('P7', Link.get_linked_entity_safe(int(form.place.data), 'P53'))
        if entity.class_.code == 'E8' and form.given_place.data:  # Link place for acquisition
            entity.link_string('P24', form.given_place.data)
        if entity.class_.code == 'E9':  # Move
            if form.object.data:  # Moved objects
                entity.link_string('P25', form.object.data)
            if form.person.data:  # Moved persons
                entity.link_string('P25', form.person.data)
            if form.place_from.data:  # Link place for move from
                linked_place = Link.get_linked_entity_safe(int(form.place_from.data), 'P53')
                entity.link('P27', linked_place)
            if form.place_to.data:  # Link place for move to
                entity.link('P26', Link.get_linked_entity_safe(int(form.place_to.data), 'P53'))
    elif entity.view_name == 'source':
        if action == 'update':
            entity.delete_links(['P128'], inverse=True)
        if form.information_carrier.data:
            entity.link_string('P128', form.information_carrier.data, inverse=True)


def get_redirect_url(form: FlaskForm,
                     entity: Entity,
                     class_: Optional[str] = '',
                     origin: Optional[Entity] = None) -> str:
    url = url_for('entity_view', id_=entity.id)
    if origin:
        url = url_for('entity_view', id_=origin.id) + '#tab-' + entity.view_name
        if origin.view_name == 'reference':
            link_id = origin.link('P67', entity)[0]
            url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
        elif origin.view_name in ['source', 'file']:
            origin.link('P67', entity)
        elif entity.view_name == 'source' and origin.class_.code != 'E84':
            entity.link('P67', origin)
        elif origin.view_name == 'event':  # Involvement, coming from actor
            link_id = origin.link('P11', entity)[0]
            url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
        elif origin.view_name == 'actor':  # Involvement, coming from event
            link_id = entity.link('P11', origin)[0]
            url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
        elif origin.view_name == entity.view_name:
            link_id = origin.link('OA7', entity)[0]
            url = url_for('relation_update', id_=link_id, origin_id=origin.id)
    if hasattr(form, 'continue_') and form.continue_.data == 'yes':
        url = url_for('insert', class_=class_, origin_id=origin.id if origin else None)
    return url
