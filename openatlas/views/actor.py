# Created by Alexander Watzinger and others. Please see README.md for licensing information

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import FieldList, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import DateForm, TableField, build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.gis import GisMapper
from openatlas.util.util import (display_remove_link, get_appearance, get_base_table_data,
                                 get_entity_data, get_profile_image_table_link, is_authorized, link,
                                 required_group, truncate_string, uc_first, was_modified)


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


@app.route('/actor/view/<int:id_>')
@required_group('readonly')
def actor_view(id_):
    actor = EntityMapper.get_by_id(id_)
    objects = []
    info = get_entity_data(actor)
    residence = actor.get_linked_entity('P74')
    if residence:
        object_ = residence.get_linked_entity('P53', True)
        objects.append(object_)
        info.append((uc_first(_('residence')), link(object_)))

    first = actor.get_linked_entity('OA8')
    if first:
        object_ = first.get_linked_entity('P53', True)
        objects.append(object_)
        info.append((uc_first(_('born in') if actor.class_.code == 'E21' else _('begins in')),
                     link(object_)))
    last = actor.get_linked_entity('OA9')
    if last:
        object_ = last.get_linked_entity('P53', True)
        objects.append(object_)
        info.append((uc_first(_('died in') if actor.class_.code == 'E21' else _('ends at')),
                     link(object_)))
    tables = {
        'info': info,
        'file': {'id': 'files', 'data': [],
                 'header': app.config['TABLE_HEADERS']['file'] + [_('main image')]},
        'source': {'id': 'source', 'data': [], 'header': app.config['TABLE_HEADERS']['source']},
        'reference': {'id': 'reference', 'data': [],
                      'header': app.config['TABLE_HEADERS']['reference'] + ['pages']},
        'event': {'id': 'event', 'data': [],
                  'header': ['event', 'class', 'involvement', 'first', 'last', 'description']},
        'relation': {'id': 'relation', 'data': [], 'sort': 'sortList:[[0,0]]',
                     'header': ['relation', 'actor', 'first', 'last', 'description']},
        'member_of': {'id': 'member_of', 'data': [],
                      'header': ['member of', 'function', 'first', 'last', 'description']}}
    profile_image_id = actor.get_profile_image_id()
    for link_ in actor.get_links('P67', True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':
            extension = data[3].replace('.', '')
            data.append(get_profile_image_table_link(domain, actor, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if domain.view_name not in ['source', 'file']:
            data.append(truncate_string(link_.description))
            if is_authorized('editor'):
                update_url = url_for('reference_link_update', link_id=link_.id, origin_id=actor.id)
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('editor'):
            url = url_for('link_delete', id_=link_.id, origin_id=actor.id)
            data.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name]['data'].append(data)

    # Todo: Performance - getting every place of every object for every event is very costly
    event_links = actor.get_links(['P11', 'P14', 'P22', 'P23'], True)

    for link_ in event_links:
        event = link_.domain
        place = event.get_linked_entity('P7')
        if place:
            objects.append(place.get_linked_entity('P53', True))
        first = link_.first
        if not link_.first and event.first:
            first = '<span class="inactive" style="float:right;">' + event.first + '</span>'
        last = link_.last
        if not link_.last and event.last:
            last = '<span class="inactive" style="float:right;">' + event.last + '</span>'
        data = ([link(event), g.classes[event.class_.code].name,
                 link_.type.name if link_.type else '', first, last,
                 truncate_string(link_.description)])
        if is_authorized('editor'):
            update_url = url_for('involvement_update', id_=link_.id, origin_id=actor.id)
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=actor.id) + '#tab-event'
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, link_.domain.name))
        tables['event']['data'].append(data)
    appears_first, appears_last = get_appearance(event_links)
    info.append((_('appears first'), appears_first))
    info.append((_('appears last'), appears_last))
    for link_ in actor.get_links('OA7') + actor.get_links('OA7', True):
        if actor.id == link_.domain.id:
            type_ = link_.type.get_name_directed() if link_.type else ''
            related = link_.range
        else:
            type_ = link_.type.get_name_directed(True) if link_.type else ''
            related = link_.domain
        data = ([type_, link(related), link_.first, link_.last, truncate_string(link_.description)])
        if is_authorized('editor'):
            update_url = url_for('relation_update', id_=link_.id, origin_id=actor.id)
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=actor.id) + '#tab-relation'
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, related.name))
        tables['relation']['data'].append(data)
    for link_ in actor.get_links('P107', True):
        data = ([link(link_.domain), link_.type.name if link_.type else '',
                 link_.first, link_.last, truncate_string(link_.description)])
        if is_authorized('editor'):
            update_url = url_for('member_update', id_=link_.id, origin_id=actor.id)
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=actor.id) + '#tab-member-of'
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, link_.domain.name))
        tables['member_of']['data'].append(data)
    if actor.class_.code in app.config['CLASS_CODES']['group']:
        tables['member'] = {'id': 'member', 'data': [],
                            'header': ['member', 'function', 'first', 'last', 'description']}
        for link_ in actor.get_links('P107'):
            data = ([link(link_.range), link_.type.name if link_.type else '',
                     link_.first, link_.last, truncate_string(link_.description)])
            if is_authorized('editor'):
                update_url = url_for('member_update', id_=link_.id, origin_id=actor.id)
                unlink_url = url_for('link_delete', id_=link_.id,
                                     origin_id=actor.id) + '#tab-member'
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
                data.append(display_remove_link(unlink_url, link_.range.name))
            tables['member']['data'].append(data)
    gis_data = GisMapper.get_all(objects) if objects else None
    if gis_data and gis_data['gisPointSelected'] == '[]':
        gis_data = None
    return render_template('actor/view.html', actor=actor, tables=tables, gis_data=gis_data,
                           profile_image_id=profile_image_id)


@app.route('/actor')
@required_group('readonly')
def actor_index():
    header = app.config['TABLE_HEADERS']['actor'] + ['description']
    table = {'id': 'actor', 'header': header, 'data': []}
    for actor in EntityMapper.get_by_codes('actor'):
        data = get_base_table_data(actor)
        data.append(truncate_string(actor.description))
        table['data'].append(data)
    return render_template('actor/index.html', table=table)


@app.route('/actor/insert/<code>', methods=['POST', 'GET'])
@app.route('/actor/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def actor_insert(code, origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
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


@app.route('/actor/delete/<int:id_>')
@required_group('editor')
def actor_delete(id_):
    EntityMapper.delete(id_)
    logger.log_user(id_, 'delete')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('actor_index'))


@app.route('/actor/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def actor_update(id_):
    actor = EntityMapper.get_by_id(id_)
    code_class = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, code_class[actor.class_.code], actor, request)
    if form.validate_on_submit():
        if was_modified(form, actor):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(actor.id)['modifier'])
            return render_template('actor/update.html', form=form, actor=actor, modifier=modifier)
        save(form, actor)
        return redirect(url_for('actor_view', id_=id_))
    residence = actor.get_linked_entity('P74')
    form.residence.data = residence.get_linked_entity('P53', True).id if residence else ''
    first = actor.get_linked_entity('OA8')
    form.begins_in.data = first.get_linked_entity('P53', True).id if first else ''
    last = actor.get_linked_entity('OA9')
    form.ends_in.data = last.get_linked_entity('P53', True).id if last else ''
    for alias in [x.name for x in actor.get_linked_entities('P131')]:
        form.alias.append_entry(alias)
    form.alias.append_entry('')
    if actor.class_.code == 'E21':
        form.begins_in.label.text = _('born in')
        form.ends_in.label.text = _('died in')
    return render_template('actor/update.html', form=form, actor=actor)


def save(form, actor=None, code=None, origin=None):
    g.cursor.execute('BEGIN')
    try:
        log_action = 'update'
        if actor:
            actor.delete_links(['P74', 'OA8', 'OA9'])
            for alias in actor.get_linked_entities('P131'):
                alias.delete()
        else:
            actor = EntityMapper.insert(code, form.name.data)
            log_action = 'insert'
        actor.name = form.name.data
        actor.description = form.description.data
        actor.set_dates(form)
        actor.update()
        actor.save_nodes(form)
        url = url_for('actor_view', id_=actor.id)
        if form.residence.data:
            object_ = EntityMapper.get_by_id(form.residence.data)
            actor.link('P74', object_.get_linked_entity('P53'))
        if form.begins_in.data:
            object_ = EntityMapper.get_by_id(form.begins_in.data)
            actor.link('OA8', object_.get_linked_entity('P53'))
        if form.ends_in.data:
            object_ = EntityMapper.get_by_id(form.ends_in.data)
            actor.link('OA9', object_.get_linked_entity('P53'))
        for alias in form.alias.data:
            if alias.strip():  # Check if it isn't empty
                actor.link('P131', EntityMapper.insert('E82', alias))
        if origin:
            if origin.view_name == 'reference':
                link_id = origin.link('P67', actor)
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif origin.view_name == 'source':
                origin.link('P67', actor)
                url = url_for('source_view', id_=origin.id) + '#tab-actor'
            elif origin.view_name == 'event':
                link_id = origin.link('P11', actor)
                url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
            elif origin.view_name == 'actor':
                link_id = origin.link('OA7', actor)
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
