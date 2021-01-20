from typing import Dict, List, Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.user import User
from openatlas.util.display import (add_edit_link, add_remove_link, add_system_data, add_type_data,
                                    format_entry_begin, format_entry_end, get_appearance,
                                    get_base_table_data, get_profile_image_table_link, link)
from openatlas.util.tab import Tab
from openatlas.util.util import is_authorized, required_group, was_modified


@app.route('/actor/insert/<code>', methods=['POST', 'GET'])
@app.route('/actor/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def actor_insert(code: str, origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    form = build_form(g.classes[code].name.lower().replace(' ', '_'), code=code, origin=origin)
    if form.validate_on_submit():
        return redirect(save(form, code=code, origin=origin))
    form.alias.append_entry('')
    if origin and origin.system_type == 'place':
        form.residence.data = origin_id
    return render_template('actor/insert.html', form=form, code=code, origin=origin)


@app.route('/actor/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def actor_update(id_: int) -> Union[str, Response]:
    actor = Entity.get_by_id(id_, nodes=True, aliases=True, view_name='actor')
    form = build_form(g.classes[actor.class_.code].name.lower().replace(' ', '_'), actor)
    if form.validate_on_submit():
        if was_modified(form, actor):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(actor.id)['modifier'])
            return render_template('actor/update.html', form=form, actor=actor, modifier=modifier)
        save(form, actor)
        return redirect(url_for('entity_view', id_=id_))
    residence = actor.get_linked_entity('P74')
    form.residence.data = residence.get_linked_entity_safe('P53', True).id if residence else ''
    first = actor.get_linked_entity('OA8')
    form.begins_in.data = first.get_linked_entity_safe('P53', True).id if first else ''
    last = actor.get_linked_entity('OA9')
    form.ends_in.data = last.get_linked_entity_safe('P53', True).id if last else ''
    for alias in actor.aliases.values():
        form.alias.append_entry(alias)
    form.alias.append_entry('')
    return render_template('actor/update.html', form=form, actor=actor)


def save(form: FlaskForm,
         actor: Optional[Entity] = None,
         code: str = '',
         origin: Optional[Entity] = None) -> Union[str, Response]:
    g.cursor.execute('BEGIN')
    try:
        log_action = 'update'
        if actor:
            actor.delete_links(['P74', 'OA8', 'OA9'])
        else:
            actor = Entity.insert(code, form.name.data)
            log_action = 'insert'
        actor.update(form)
        ReferenceSystem.update_links(form, actor)
        if form.residence.data:
            object_ = Entity.get_by_id(form.residence.data, view_name='place')
            actor.link('P74', object_.get_linked_entity_safe('P53'))
        if form.begins_in.data:
            object_ = Entity.get_by_id(form.begins_in.data, view_name='place')
            actor.link('OA8', object_.get_linked_entity_safe('P53'))
        if form.ends_in.data:
            object_ = Entity.get_by_id(form.ends_in.data, view_name='place')
            actor.link('OA9', object_.get_linked_entity_safe('P53'))

        url = url_for('entity_view', id_=actor.id)
        if origin:
            if origin.view_name == 'reference':
                link_id = origin.link('P67', actor)[0]
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif origin.view_name in ['source', 'file']:
                origin.link('P67', actor)
                url = url_for('entity_view', id_=origin.id) + '#tab-actor'
            elif origin.view_name == 'event':
                link_id = origin.link('P11', actor)[0]
                url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
            elif origin.view_name == 'actor':
                link_id = origin.link('OA7', actor)[0]
                url = url_for('relation_update', id_=link_id, origin_id=origin.id)
            elif origin.view_name == 'place':
                url = url_for('entity_view', id_=origin.id) + '#tab-actor'
        if hasattr(form, 'continue_') and form.continue_.data == 'yes':
            url = url_for('actor_insert', code=code)
        logger.log_user(actor.id, log_action)
        g.cursor.execute('COMMIT')
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        return redirect(url_for('actor_index'))
    return url


def actor_view(actor: Entity) -> str:
    tabs = {name: Tab(name, origin=actor) for name in [
        'info', 'source', 'event', 'relation', 'member_of', 'member', 'reference', 'file']}
    profile_image_id = actor.get_profile_image_id()
    for link_ in actor.get_links('P67', True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':
            extension = data[3]
            data.append(get_profile_image_table_link(domain, actor, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if domain.view_name not in ['source', 'file']:
            data.append(link_.description)
            data = add_edit_link(data, url_for('reference_link_update',
                                               link_id=link_.id,
                                               origin_id=actor.id))
            if domain.view_name == 'reference_system':
                actor.reference_systems.append(link_)
                continue
        data = add_remove_link(data, domain.name, link_, actor, domain.view_name)
        tabs[domain.view_name].table.rows.append(data)

    # Todo: Performance - getting every place of every object for every event is very costly
    event_links = actor.get_links(['P11', 'P14', 'P22', 'P23', 'P25'], True)

    objects = []
    for link_ in event_links:
        event = link_.domain
        places = event.get_linked_entities(['P7', 'P26', 'P27'])
        link_.object_ = None
        for place in places:
            object_ = place.get_linked_entity_safe('P53', True)
            objects.append(object_)
            link_.object_ = object_  # Needed later for first/last appearance info
        first = link_.first
        if not link_.first and event.first:
            first = '<span class="inactive">' + event.first + '</span>'
        last = link_.last
        if not link_.last and event.last:
            last = '<span class="inactive">' + event.last + '</span>'
        data = [link(event),
                g.classes[event.class_.code].name,
                link(link_.type),
                first,
                last,
                link_.description]
        data = add_edit_link(data, url_for('involvement_update', id_=link_.id, origin_id=actor.id))
        data = add_remove_link(data, link_.domain.name, link_, actor, 'event')
        tabs['event'].table.rows.append(data)

    # Add info of dates and places
    begin_place = actor.get_linked_entity('OA8')
    begin_object = None
    if begin_place:
        begin_object = begin_place.get_linked_entity_safe('P53', True)
        objects.append(begin_object)
    end_place = actor.get_linked_entity('OA9')
    end_object = None
    if end_place:
        end_object = end_place.get_linked_entity_safe('P53', True)
        objects.append(end_object)

    residence_place = actor.get_linked_entity('P74')
    residence_object = None
    if residence_place:
        residence_object = residence_place.get_linked_entity_safe('P53', True)
        objects.append(residence_object)

    # Collect data for info tab
    appears_first, appears_last = get_appearance(event_links)
    info: Dict[str, Union[str, List[str]]] = {
        _('alias'): list(actor.aliases.values()),
        _('born') if actor.class_.code == 'E21' else _('begin'):
            format_entry_begin(actor, begin_object),
        _('died') if actor.class_.code == 'E21' else _('end'): format_entry_end(actor, end_object),
        _('appears first'): appears_first,
        _('appears last'): appears_last,
        _('residence'): link(residence_object) if residence_object else ''}
    add_type_data(actor, info)
    add_system_data(actor, info)

    for link_ in actor.get_links('OA7') + actor.get_links('OA7', True):
        type_ = ''
        if actor.id == link_.domain.id:
            related = link_.range
            if link_.type:
                type_ = link(link_.type.get_name_directed(),
                             url_for('entity_view', id_=link_.type.id))
        else:
            related = link_.domain
            if link_.type:
                type_ = link(link_.type.get_name_directed(True),
                             url_for('entity_view', id_=link_.type.id))
        data = [type_, link(related), link_.first, link_.last, link_.description]
        data = add_edit_link(data, url_for('relation_update', id_=link_.id, origin_id=actor.id))
        data = add_remove_link(data, related.name, link_, actor, 'relation')
        tabs['relation'].table.rows.append(data)
    for link_ in actor.get_links('P107', True):
        data = [link(link_.domain), link(link_.type), link_.first, link_.last, link_.description]
        data = add_edit_link(data, url_for('member_update', id_=link_.id, origin_id=actor.id))
        data = add_remove_link(data, link_.domain.name, link_, actor, 'member-of')
        tabs['member_of'].table.rows.append(data)
    if actor.class_.code not in app.config['CLASS_CODES']['group']:
        del tabs['member']
    else:
        for link_ in actor.get_links('P107'):
            data = [link(link_.range), link(link_.type), link_.first, link_.last, link_.description]
            if is_authorized('contributor'):
                data.append(link(_('edit'),
                                 url_for('member_update', id_=link_.id, origin_id=actor.id)))
            data = add_remove_link(data, link_.range.name, link_, actor, 'member')
            tabs['member'].table.rows.append(data)
    gis_data = Gis.get_all(objects) if objects else None
    if gis_data and gis_data['gisPointSelected'] == '[]' and gis_data['gisPolygonSelected'] == '[]':
        gis_data = None
    actor.note = User.get_note(actor)
    return render_template('actor/view.html',
                           entity=actor,
                           info=info,
                           tabs=tabs,
                           gis_data=gis_data,
                           profile_image_id=profile_image_id)
