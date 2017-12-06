# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_form
from openatlas.models.entity import EntityMapper, Entity
from openatlas.models.link import LinkMapper
from openatlas.util.util import (truncate_string, required_group, append_node_data,
                                 build_remove_link, get_base_table_data, uc_first, link)


class PlaceForm(DateForm):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/place')
@required_group('readonly')
def place_index():
    table = {'name': 'place', 'header': app.config['TABLE_HEADERS']['place'], 'data': []}
    for place in EntityMapper.get_by_codes('place'):
        table['data'].append(get_base_table_data(place))
    return render_template('place/index.html', table=table)


@app.route('/place/insert', methods=['POST', 'GET'])
@app.route('/place/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def place_insert(origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = build_form(PlaceForm, 'Place')
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        result = save(form, None, None, origin)
        flash(_('entity created'), 'info')
        if not isinstance(result, Entity):
            return redirect(url_for('reference_link_update', link_id=result, origin_id=origin_id))
        if form.continue_.data == 'yes':
            return redirect(url_for('place_insert', origin_id=origin_id))
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-place')
        return redirect(url_for('place_view', id_=result.id))
    return render_template('place/insert.html', form=form, origin=origin)


@app.route('/place/view/<int:id_>')
@app.route('/place/view/<int:id_>/<int:unlink_id>')
@required_group('readonly')
def place_view(id_, unlink_id=None):
    object_ = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
    object_.set_dates()
    location = object_.get_linked_entity('P53')
    tables = {'info': []}
    append_node_data(tables['info'], object_, location)
    tables['source'] = {
        'name': 'source',
        'header': app.config['TABLE_HEADERS']['source'] + ['description', ''],
        'data': []}
    tables['reference'] = {
        'name': 'reference',
        'header': app.config['TABLE_HEADERS']['reference'] + ['pages', '', ''],
        'data': []}
    for link_ in object_.get_links('P67', True):
        name = app.config['CODE_CLASS'][link_.domain.class_.code]
        unlink_url = url_for('place_view', id_=object_.id, unlink_id=link_.id) + '#tab-' + name
        data = get_base_table_data(link_.domain)
        if name == 'source':
            data.append(truncate_string(link_.domain.description))
        else:
            data.append(truncate_string(link_.description))
            update_url = url_for('reference_link_update', link_id=link_.id, origin_id=object_.id)
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        data.append(build_remove_link(unlink_url, link_.domain.name))
        tables[name]['data'].append(data)
    tables['event'] = {
        'name': 'event',
        'header': app.config['TABLE_HEADERS']['event'],
        'data': []}
    for event in location.get_linked_entities('P7', True):
        data = get_base_table_data(event)
        tables['event']['data'].append(data)
    for event in object_.get_linked_entities('P24', True):
        data = get_base_table_data(event)
        tables['event']['data'].append(data)
    tables['actor'] = {
        'name': 'actor',
        'header': [_('actor'), _('property'), _('class'), _('first'), _('last')],
        'data': []}
    for link_ in location.get_links(['P74', 'OA8', 'OA9'], True):
        actor = EntityMapper.get_by_id(link_.domain.id)
        tables['actor']['data'].append([
            link(actor),
            openatlas.properties[link_.property.code].name,
            actor.class_.name,
            actor.first,
            actor.last])
    return render_template('place/view.html', object_=object_, tables=tables)


@app.route('/place/delete/<int:id_>')
@required_group('editor')
def place_delete(id_):
    place = EntityMapper.get_by_id(id_)
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(place.get_linked_entity('P53'))
    EntityMapper.delete(id_)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('place_index'))


@app.route('/place/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def place_update(id_):
    object_ = EntityMapper.get_by_id(id_)
    object_.set_dates()
    location = object_.get_linked_entity('P53')
    form = build_form(PlaceForm, 'Place', object_, request, location)
    if form.validate_on_submit():
        save(form, object_, location)
        flash(_('info update'), 'info')
        return redirect(url_for('place_view', id_=id_))
    return render_template('place/update.html', form=form, object_=object_)


def save(form, object_=None, location=None, origin=None):
    openatlas.get_cursor().execute('BEGIN')
    if not object_:
        object_ = EntityMapper.insert('E18', form.name.data)
        location = EntityMapper.insert('E53', 'Location of ' + form.name.data, 'place location')
        object_.link('P53', location)
    object_.name = form.name.data
    object_.description = form.description.data
    object_.update()
    object_.save_dates(form)
    object_.save_nodes(form)
    location.name = 'Location of ' + form.name.data
    location.update()
    location.save_nodes(form)
    link_ = None
    if origin:
        if origin.class_.code in app.config['CLASS_CODES']['reference']:
            link_ = origin.link('P67', object_)
        else:
            origin.link('P67', object_)
    openatlas.get_cursor().execute('COMMIT')
    return link_ if link_ else object_
