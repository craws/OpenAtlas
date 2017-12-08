# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_form, TableField
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper, Link
from openatlas.util.util import (truncate_string, required_group, append_node_data,
                                 build_remove_link, get_base_table_data, uc_first, link)


class ActorForm(DateForm):
    name = StringField(_('name'), validators=[InputRequired()])
    residence = TableField(_('residence'))
    appears_first = TableField(_('appears first'))
    appears_last = TableField(_('appears last'))
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/actor/view/<int:id_>')
@app.route('/actor/view/<int:id_>/<int:unlink_id>')
@required_group('readonly')
def actor_view(id_, unlink_id=None):
    actor = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
    actor.set_dates()
    tables = {'info': []}
    append_node_data(tables['info'], actor)
    tables['source'] = {
        'name': 'source',
        'header': app.config['TABLE_HEADERS']['source'] + ['description', ''],
        'data': []}
    tables['reference'] = {
        'name': 'reference',
        'header': app.config['TABLE_HEADERS']['reference'] + ['pages', '', ''],
        'data': []}
    for link_ in actor.get_links('P67', True):
        name = app.config['CODE_CLASS'][link_.domain.class_.code]
        data = get_base_table_data(link_.domain)
        if name == 'source':
            data.append(truncate_string(link_.domain.description))
        else:
            data.append(truncate_string(link_.description))
            update_url = url_for('reference_link_update', link_id=link_.id, origin_id=actor.id)
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        unlink_url = url_for('actor_view', id_=actor.id, unlink_id=link_.id) + '#tab' + name
        data.append(build_remove_link(unlink_url, link_.domain.name))
        tables[name]['data'].append(data)
    tables['event'] = {
        'name': 'event',
        'header': ['event', 'class', 'involvement', 'first', 'last', 'description'],
        'data': []}
    for link_ in actor.get_links(['P11', 'P14', 'P22', 'P23'], True):
        event = link_.domain
        first = link_.first
        if not link_.first and event.first:
            first = '<span class="inactive" style="float:right">' + str(event.first) + '</span>'
        last = link_.last
        if not link_.last and event.last:
            last = '<span class="inactive" style="float:right">' + str(event.last) + '</span>'
        update_url = url_for('involvement_update', id_=link_.id, origin_id=actor.id)
        unlink_url = url_for('actor_view', id_=actor.id, unlink_id=link_.id) + '#tab-event'
        tables['event']['data'].append([
            link(event),
            openatlas.classes[event.class_.code].name,
            openatlas.nodes[link_.type_id].name if link_.type_id else '',
            first,
            last,
            truncate_string(link_.description),
            '<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>',
            build_remove_link(unlink_url, link_.range.name)])
    return render_template('actor/view.html', actor=actor, tables=tables)


@app.route('/actor')
@required_group('readonly')
def actor_index():
    header = app.config['TABLE_HEADERS']['actor'] + ['description']
    table = {'name': 'actor', 'header': header, 'data': []}
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
    forms = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, forms[code])
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        result = save(form, None, code, origin)
        flash(_('entity created'), 'info')
        if isinstance(result, Link) and result.property_code == 'P67':
            return redirect(url_for('reference_link_update', link_id=result, origin_id=origin_id))
        if form.continue_.data == 'yes':
            return redirect(url_for('actor_insert', code=code, origin_id=origin_id))
        if origin:
            if origin.class_.code in app.config['CLASS_CODES']['event']:
                return redirect(url_for('involvement_update', id_=result, origin_id=origin_id))
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-actor')
        return redirect(url_for('actor_view', id_=result.id))
    return render_template('actor/insert.html', form=form, code=code, origin=origin)


@app.route('/actor/delete/<int:id_>')
@required_group('editor')
def actor_delete(id_):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(id_)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('actor_index'))


@app.route('/actor/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def actor_update(id_):
    actor = EntityMapper.get_by_id(id_)
    actor.set_dates()
    forms = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, forms[actor.class_.code], actor, request)
    if form.validate_on_submit():
        save(form, actor)
        flash(_('info update'), 'info')
        return redirect(url_for('actor_view', id_=id_))
    residence = actor.get_linked_entity('P74')
    form.residence.data = residence.get_linked_entity('P53', True).id if residence else ''
    first = actor.get_linked_entity('OA8')
    form.appears_first.data = first.get_linked_entity('P53', True).id if first else ''
    last = actor.get_linked_entity('OA9')
    form.appears_last.data = last.get_linked_entity('P53', True).id if last else ''
    return render_template('actor/update.html', form=form, actor=actor)


def save(form, actor=None, code=None, origin=None):
    openatlas.get_cursor().execute('BEGIN')
    if actor:
        LinkMapper.delete_by_codes(actor, ['P74', 'OA8', 'OA9'])
    else:
        actor = EntityMapper.insert(code, form.name.data)
    actor.name = form.name.data
    actor.description = form.description.data
    actor.update()
    actor.save_dates(form)
    actor.save_nodes(form)
    if form.residence.data:
        object_ = EntityMapper.get_by_id(form.residence.data)
        actor.link('P74', object_.get_linked_entity('P53'))
    if form.appears_first.data:
        object_ = EntityMapper.get_by_id(form.appears_first.data)
        actor.link('OA8', object_.get_linked_entity('P53'))
    if form.appears_last.data:
        object_ = EntityMapper.get_by_id(form.appears_last.data)
        actor.link('OA9', object_.get_linked_entity('P53'))
    link_ = None
    if origin:
        if origin.class_.code in app.config['CLASS_CODES']['reference']:
            link_ = origin.link('P67', actor)
        elif origin.class_.code in app.config['CLASS_CODES']['source']:
            origin.link('P67', actor)
        elif origin.class_.code in app.config['CLASS_CODES']['event']:
            link_ = origin.link('P11', actor)
    openatlas.get_cursor().execute('COMMIT')
    return link_ if link_ else actor
