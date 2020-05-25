from typing import Dict, List, Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import FieldList, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.date import DateForm
from openatlas.forms.forms import TableField, build_form
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.user import User
from openatlas.util.table import Table
from openatlas.util.util import (add_system_data, add_type_data, button, display_remove_link,
                                 format_entry_begin, format_entry_end, get_appearance,
                                 get_base_table_data, get_profile_image_table_link,
                                 is_authorized, link, required_group, uc_first, was_modified)


class ActorForm(DateForm):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    alias = FieldList(StringField(''), description=_('tooltip alias'))
    residence = TableField(_('residence'))
    begins_in = TableField()
    ends_in = TableField()
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/actor')
@app.route('/actor/<action>/<int:id_>')
@required_group('readonly')
def actor_index(action: Optional[str] = None, id_: Optional[int] = None) -> str:
    if id_ and action == 'delete':
        Entity.delete_(id_)
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
    table = Table(Table.HEADERS['actor'] + ['description'],
                  defs=[{'className': 'dt-body-right', 'targets': [2, 3]}])
    for actor in Entity.get_by_menu_item('actor'):
        data = get_base_table_data(actor)
        data.append(actor.description)
        table.rows.append(data)
    return render_template('actor/index.html', table=table)


@app.route('/actor/insert/<code>', methods=['POST', 'GET'])
@app.route('/actor/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def actor_insert(code: str, origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    code_class = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, code_class[code])
    if form.validate_on_submit():
        return redirect(save(form, code=code, origin=origin))
    form.alias.append_entry('')
    if origin:
        del form.insert_and_continue
    if code == 'E21':
        form.begins_in.label.text = _('born in')
        form.ends_in.label.text = _('died in')
    return render_template('actor/insert.html', form=form, code=code, origin=origin)


@app.route('/actor/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def actor_update(id_: int) -> Union[str, Response]:
    actor = Entity.get_by_id(id_, nodes=True, aliases=True, view_name='actor')
    code_class = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, code_class[actor.class_.code], actor, request)
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
    if actor.class_.code == 'E21':
        form.begins_in.label.text = _('born in')
        form.ends_in.label.text = _('died in')
    return render_template('actor/update.html', form=form, actor=actor)


def save(form: ActorForm,
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
            elif origin.view_name == 'source':
                origin.link('P67', actor)
                url = url_for('entity_view', id_=origin.id) + '#tab-actor'
            elif origin.view_name == 'event':
                link_id = origin.link('P11', actor)[0]
                url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
            elif origin.view_name == 'actor':
                link_id = origin.link('OA7', actor)[0]
                url = url_for('relation_update', id_=link_id, origin_id=origin.id)
        if form.continue_.data == 'yes' and code:
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
    tabs = {'info': {
                'header': _('info')},
            'source': {
                'header': _('source'),
                'table': Table(Table.HEADERS['source']),
                'buttons': [button(_('add'), url_for('entity_add_source', id_=actor.id)),
                            button(_('source'), url_for('source_insert', origin_id=actor.id))]},
            'event': {
                'header': _('event'),
                'buttons': [button(_('add'), url_for('involvement_insert', origin_id=actor.id))],
                'table': Table(['event', 'class', 'involvement', 'first', 'last', 'description'],
                               defs=[{'className': 'dt-body-right', 'targets': [3, 4]}])},
            'relation': {
                'header': _('relation'),
                'buttons': [button(_('add'), url_for('relation_insert', origin_id=actor.id))],
                'table': Table(['relation', 'actor', 'first', 'last', 'description'],
                               defs=[{'className': 'dt-body-right', 'targets': [2, 3]}])},
            'member_of': {
                'header': _('member of'),
                'buttons': [button(_('add'), url_for('membership_insert', origin_id=actor.id))],
                'table': Table(['member of', 'function', 'first', 'last', 'description'],
                               defs=[{'className': 'dt-body-right', 'targets': [2, 3]}])},
            'member': {
                'header':
                    _('member') if actor.class_.code in app.config['CLASS_CODES']['group'] else '',
                'buttons': [button(_('add'), url_for('member_insert', origin_id=actor.id))],
                'table': Table(['member', 'function', 'first', 'last', 'description'],
                               defs=[{'className': 'dt-body-right', 'targets': [2, 3]}])},
            'reference': {
                'header': _('reference'),
                'table': Table(Table.HEADERS['reference'] + ['page / link text']),
                'buttons': [button(_('add'), url_for('entity_add_reference', id_=actor.id)),
                            button(_('bibliography'), url_for('reference_insert',
                                                              code='bibliography',
                                                              origin_id=actor.id)),
                            button(_('edition'), url_for('reference_insert',
                                                         code='edition',
                                                         origin_id=actor.id)),
                            button(_('external reference'), url_for('reference_insert',
                                                                    code='external_reference',
                                                                    origin_id=actor.id))]},
            'file': {
                'header': _('files'),
                'table': Table(Table.HEADERS['file'] + [_('main image')]),
                'buttons': [button(_('add'), url_for('entity_add_file', id_=actor.id)),
                            button(_('file'), url_for('file_insert', origin_id=actor.id))]}}
    for code in app.config['CLASS_CODES']['actor']:
        tabs['relation']['buttons'].append(
            button(g.classes[code].name, url_for('actor_insert', code=code, origin_id=actor.id)))
    for code in app.config['CLASS_CODES']['event']:
        tabs['event']['buttons'].append(
            button(g.classes[code].name, url_for('event_insert', code=code, origin_id=actor.id)))

    actor.note = User.get_note(actor)
    profile_image_id = actor.get_profile_image_id()
    for link_ in actor.get_links('P67', True):
        domain = link_.domain
        data_ = get_base_table_data(domain)
        if domain.view_name == 'file':
            extension = data_[3].replace('.', '')
            data_.append(
                get_profile_image_table_link(domain, actor, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if domain.view_name not in ['source', 'file']:
            data_.append(link_.description)
            if domain.system_type == 'external reference':
                actor.external_references.append(link_)
            if is_authorized('contributor'):
                url = url_for('reference_link_update', link_id=link_.id, origin_id=actor.id)
                data_.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=actor.id)
            data_.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tabs[domain.view_name]['table'].rows.append(data_)

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
            first = '<span class="inactive" style="float:right;">' + event.first + '</span>'
        last = link_.last
        if not link_.last and event.last:
            last = '<span class="inactive" style="float:right;">' + event.last + '</span>'
        data = ([link(event),
                 g.classes[event.class_.code].name,
                 link_.type.name if link_.type else '',
                 first,
                 last,
                 link_.description])
        if is_authorized('contributor'):
            update_url = url_for('involvement_update', id_=link_.id, origin_id=actor.id)
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=actor.id) + '#tab-event'
            if link_.domain.class_.code != 'E9':
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            else:
                data.append('')
            data.append(display_remove_link(unlink_url, link_.domain.name))
        tabs['event']['table'].rows.append(data)

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
        if actor.id == link_.domain.id:
            type_ = link_.type.get_name_directed() if link_.type else ''
            related = link_.range
        else:
            type_ = link_.type.get_name_directed(True) if link_.type else ''
            related = link_.domain
        data = (
            [type_, link(related), link_.first, link_.last, link_.description])
        if is_authorized('contributor'):
            update_url = url_for('relation_update', id_=link_.id, origin_id=actor.id)
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=actor.id) + '#tab-relation'
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, related.name))
        tabs['relation']['table'].rows.append(data)
    for link_ in actor.get_links('P107', True):
        data = ([link(link_.domain),
                 link_.type.name if link_.type else '',
                 link_.first,
                 link_.last,
                 link_.description])
        if is_authorized('contributor'):
            update_url = url_for('member_update', id_=link_.id, origin_id=actor.id)
            unlink_url = url_for('link_delete', id_=link_.id,
                                 origin_id=actor.id) + '#tab-member-of'
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, link_.domain.name))
        tabs['member_of']['table'].rows.append(data)
    if actor.class_.code in app.config['CLASS_CODES']['group']:
        for link_ in actor.get_links('P107'):
            data = ([link(link_.range),
                     link_.type.name if link_.type else '',
                     link_.first,
                     link_.last,
                     link_.description])
            if is_authorized('contributor'):
                update_url = url_for('member_update', id_=link_.id, origin_id=actor.id)
                unlink_url = url_for('link_delete', id_=link_.id,
                                     origin_id=actor.id) + '#tab-member'
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
                data.append(display_remove_link(unlink_url, link_.range.name))
            tabs['member']['table'].rows.append(data)
    gis_data = Gis.get_all(objects) if objects else None
    if gis_data:
        if gis_data['gisPointSelected'] == '[]' and gis_data['gisPolygonSelected'] == '[]':
            gis_data = None
    return render_template('actor/view.html',
                           actor=actor,
                           info=info,
                           tabs=tabs,
                           gis_data=gis_data,
                           profile_image_id=profile_image_id)
