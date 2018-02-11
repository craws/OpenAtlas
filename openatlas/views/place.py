# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash, request, g
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField, FieldList
from wtforms.validators import DataRequired

import openatlas
from openatlas import app
from openatlas.forms.forms import DateForm, build_form
from openatlas.models.entity import EntityMapper, Entity
from openatlas.models.gis import GisMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import (build_remove_link, required_group, get_entity_data, uc_first, link,
                                 truncate_string, get_base_table_data, is_authorized, was_modified)


class PlaceForm(DateForm):
    name = StringField(_('name'), [DataRequired()])
    alias = FieldList(StringField(''), description=_('tooltip alias'))
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    gis_points = HiddenField()
    gis_polygons = HiddenField()
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/place')
@required_group('readonly')
def place_index():
    table = {'id': 'place', 'header': app.config['TABLE_HEADERS']['place'], 'data': []}
    for place in EntityMapper.get_by_codes('place'):
        table['data'].append(get_base_table_data(place))
    return render_template('place/index.html', table=table, gis_data=GisMapper.get_all())


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
        if not result:  # pragma: no cover
            gis_data = GisMapper.get_all()
            return render_template('place/insert.html', form=form, origin=origin, gis_data=gis_data)
        flash(_('entity created'), 'info')
        if not isinstance(result, Entity):
            return redirect(url_for('reference_link_update', link_id=result, origin_id=origin_id))
        if form.continue_.data == 'yes':
            return redirect(url_for('place_insert', origin_id=origin_id))
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-place')
        return redirect(url_for('place_view', id_=result.id))
    form.alias.append_entry('')
    gis_data = GisMapper.get_all()
    return render_template('place/insert.html', form=form, origin=origin, gis_data=gis_data)


@app.route('/place/view/<int:id_>')
@app.route('/place/view/<int:id_>/<int:unlink_id>')
@required_group('readonly')
def place_view(id_, unlink_id=None):
    object_ = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
        flash(_('link removed'), 'info')
    object_.set_dates()
    location = object_.get_linked_entity('P53')
    tables = {
        'info': get_entity_data(object_, location),
        'source': {
            'id': 'source', 'header': app.config['TABLE_HEADERS']['source'] + ['description'],
            'data': []},
        'reference': {
            'id': 'reference', 'header': app.config['TABLE_HEADERS']['reference'] + ['pages'],
            'data': []}}
    for link_ in object_.get_links('P67', True):
        name = app.config['CODE_CLASS'][link_.domain.class_.code]
        data = get_base_table_data(link_.domain)
        if name == 'source':
            data.append(truncate_string(link_.domain.description))
        else:
            data.append(truncate_string(link_.description))
            if is_authorized('editor'):
                url = url_for('reference_link_update', link_id=link_.id, origin_id=object_.id)
                data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('editor'):
            unlink_url = url_for('place_view', id_=object_.id, unlink_id=link_.id) + '#tab-' + name
            data.append(build_remove_link(unlink_url, link_.domain.name))
        tables[name]['data'].append(data)
    tables['event'] = {
        'id': 'event',
        'header': app.config['TABLE_HEADERS']['event'],
        'data': []}
    for event in location.get_linked_entities(['P7', 'P24'], True):
        tables['event']['data'].append(get_base_table_data(event))
    tables['actor'] = {
        'id': 'actor',
        'header': [_('actor'), _('property'), _('class'), _('first'), _('last')],
        'data': []}
    for link_ in location.get_links(['P74', 'OA8', 'OA9'], True):
        actor = EntityMapper.get_by_id(link_.domain.id)
        tables['actor']['data'].append([
            link(actor),
            g.properties[link_.property.code].name,
            actor.class_.name,
            actor.first,
            actor.last])
    gis_data = GisMapper.get_all(object_.id) if location else None
    if gis_data['gisPointSelected'] == '[]' and gis_data['gisPolygonSelected'] == '[]':
        gis_data = None
    return render_template('place/view.html', object_=object_, tables=tables, gis_data=gis_data)


@app.route('/place/delete/<int:id_>')
@required_group('editor')
def place_delete(id_):
    g.cursor.execute('BEGIN')
    try:
        EntityMapper.delete(id_)
        openatlas.logger.log_user(id_, 'delete')
        g.cursor.execute('COMMIT')
    except Exception as e:
        g.cursor.execute('ROLLBACK')
        openatlas.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
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
        if was_modified(form, object_):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(openatlas.logger.get_log_for_advanced_view(object_.id)['modifier'])
            return render_template(
                'place/update.html', form=form, object_=object_, modifier=modifier)
        if save(form, object_, location):
            flash(_('info update'), 'info')
        return redirect(url_for('place_view', id_=id_))
    for alias in [x.name for x in object_.get_linked_entities('P1')]:
        form.alias.append_entry(alias)
    form.alias.append_entry('')
    gis_data = GisMapper.get_all(object_.id)
    return render_template('place/update.html', form=form, object_=object_, gis_data=gis_data)


def save(form, object_=None, location=None, origin=None):
    g.cursor.execute('BEGIN')
    try:
        if object_:
            for alias in object_.get_linked_entities('P1'):
                alias.delete()
            GisMapper.delete_by_entity(location)
            openatlas.logger.log_user(object_.id, 'update')
        else:
            object_ = EntityMapper.insert('E18', form.name.data)
            location = EntityMapper.insert('E53', 'Location of ' + form.name.data, 'place location')
            object_.link('P53', location)
            openatlas.logger.log_user(object_.id, 'insert')
        object_.name = form.name.data
        object_.description = form.description.data
        object_.update()
        object_.save_dates(form)
        object_.save_nodes(form)
        location.name = 'Location of ' + form.name.data
        location.update()
        location.save_nodes(form)
        for alias in form.alias.data:
            if alias.strip():  # check if it isn't empty
                object_.link('P1', EntityMapper.insert('E41', alias))
        link_ = None
        if origin:
            if origin.class_.code in app.config['CLASS_CODES']['reference']:
                link_ = origin.link('P67', object_)
            else:
                origin.link('P67', object_)
        GisMapper.insert(location, form)
        g.cursor.execute('COMMIT')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        openatlas.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        return
    return link_ if link_ else object_
