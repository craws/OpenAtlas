# Created 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import FieldList, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from openatlas import app, logger
from openatlas.forms.forms import DateForm, build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.gis import GisMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import (display_remove_link, get_base_table_data, get_entity_data,
                                 is_authorized, link, required_group, truncate_string, uc_first,
                                 was_modified, get_view_name)


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
        return redirect(save(form, origin=origin))
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
        'file': {'id': 'files', 'data': [], 'header': app.config['TABLE_HEADERS']['file']},
        'source': {'id': 'source', 'data': [], 'header': app.config['TABLE_HEADERS']['source']},
        'event': {'id': 'event', 'data': [], 'header': app.config['TABLE_HEADERS']['event']},
        'reference': {
            'id': 'reference', 'data': [],
            'header': app.config['TABLE_HEADERS']['reference'] + ['pages']},
        'actor': {
            'id': 'actor', 'data': [],
            'header': [_('actor'), _('property'), _('class'), _('first'), _('last')]}}
    for link_ in object_.get_links('P67', True):
        data = get_base_table_data(link_.domain)
        view_name = get_view_name(link_.domain)
        if view_name not in ['source', 'file']:
            data.append(truncate_string(link_.description))
            if is_authorized('editor'):
                url = url_for('reference_link_update', link_id=link_.id, origin_id=object_.id)
                data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('editor'):
            url = url_for('place_view', id_=object_.id, unlink_id=link_.id) + '#tab-' + view_name
            data.append(display_remove_link(url, link_.domain.name))
        tables[view_name]['data'].append(data)
    for event in location.get_linked_entities(['P7', 'P24'], True):
        tables['event']['data'].append(get_base_table_data(event))
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
        logger.log_user(id_, 'delete')
        g.cursor.execute('COMMIT')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
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
            modifier = link(logger.get_log_for_advanced_view(object_.id)['modifier'])
            return render_template(
                'place/update.html', form=form, object_=object_, modifier=modifier)
        save(form, object_, location)
        return redirect(url_for('place_view', id_=id_))
    for alias in [x.name for x in object_.get_linked_entities('P1')]:
        form.alias.append_entry(alias)
    form.alias.append_entry('')
    gis_data = GisMapper.get_all(object_.id)
    return render_template('place/update.html', form=form, object_=object_, gis_data=gis_data)


def save(form, object_=None, location=None, origin=None):
    g.cursor.execute('BEGIN')
    try:
        log_action = 'update'
        if object_:
            for alias in object_.get_linked_entities('P1'):
                alias.delete()
            GisMapper.delete_by_entity(location)
        else:
            log_action = 'insert'
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
        for alias in form.alias.data:
            if alias.strip():  # check if it isn't empty
                object_.link('P1', EntityMapper.insert('E41', alias))
        url = url_for('place_view', id_=object_.id)
        if origin:
            view_name = get_view_name(origin)
            url = url_for(get_view_name(origin) + '_view', id_=origin.id) + '#tab-place'
            if view_name == 'reference':
                link_id = origin.link('P67', object_)
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            else:
                origin.link('P67', object_)
        GisMapper.insert(location, form)
        g.cursor.execute('COMMIT')
        if form.continue_.data == 'yes':
            url = url_for('place_insert', origin_id=origin.id if origin else None)
        logger.log_user(object_.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('place_index')
    return url
