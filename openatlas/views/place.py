# Created by Alexander Watzinger and others. Please see README.md for licensing information
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


class FeatureForm(DateForm):
    name = StringField(_('name'), [DataRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    gis_points = HiddenField()
    gis_polygons = HiddenField()
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/place')
@required_group('readonly')
def place_index():
    table = {'id': 'place', 'header': app.config['TABLE_HEADERS']['place'], 'data': []}
    for place in EntityMapper.get_by_system_type('place'):
        table['data'].append(get_base_table_data(place))
    return render_template('place/index.html', table=table, gis_data=GisMapper.get_all())


@app.route('/place/insert', methods=['POST', 'GET'])
@app.route('/place/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def place_insert(origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    if origin and origin.system_type == 'place':
        title = 'feature'
        form = build_form(FeatureForm, 'Feature')
    elif origin and origin.system_type == 'feature':
        title = 'stratigraphic unit'
        form = build_form(FeatureForm, 'Stratigraphic Unit')
    elif origin and origin.system_type == 'stratigraphic_unit':
        title = 'find'
        form = build_form(FeatureForm, 'Find')
    else:
        title = 'place'
        form = build_form(PlaceForm, 'Place')
    if origin \
            and origin.system_type not in ['place', 'feature', 'stratigraphic_unit'] \
            and hasattr(form, 'insert_and_continue'):
        del form.insert_and_continue
    if form.validate_on_submit():
        return redirect(save(form, origin=origin))
    if title == 'place':
        form.alias.append_entry('')
    gis_data = GisMapper.get_all()
    place = None
    feature = None
    if origin and origin.system_type == 'stratigraphic_unit':
        feature = origin.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    elif origin and origin.system_type == 'feature':
        place = origin.get_linked_entity('P46', True)
    return render_template('place/insert.html', form=form, title=title, place=place,
                           gis_data=gis_data, feature=feature, origin=origin)


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
    if object_.system_type == 'place':
        tables['feature'] = {'id': 'feature', 'data': [],
                             'header': app.config['TABLE_HEADERS']['place'] + [_('description')]}
    if object_.system_type == 'feature':
        tables['stratigraphic_unit'] = {
            'id': 'stratigraphic', 'data': [], 'header':
            app.config['TABLE_HEADERS']['place'] + [_('description')]}
    if object_.system_type == 'stratigraphic_unit':
        tables['find'] = {'id': 'find', 'data': [],
                          'header': app.config['TABLE_HEADERS']['place'] + [_('description')]}
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
    has_subunits = False
    for entity in object_.get_linked_entities('P46'):
        has_subunits = True
        data = get_base_table_data(entity)
        data.append(truncate_string(entity.description))
        tables[entity.system_type]['data'].append(data)
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
    place = None
    feature = None
    stratigraphic_unit = None
    if object_.system_type == 'find':
        stratigraphic_unit = object_.get_linked_entity('P46', True)
        feature = stratigraphic_unit.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    elif object_.system_type == 'stratigraphic_unit':
        feature = object_.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    elif object_.system_type == 'feature':
        place = object_.get_linked_entity('P46', True)
    return render_template('place/view.html', object_=object_, tables=tables, gis_data=gis_data,
                           place=place, feature=feature, stratigraphic_unit=stratigraphic_unit,
                           has_subunits=has_subunits)


@app.route('/place/delete/<int:id_>')
@required_group('editor')
def place_delete(id_):
    entity = EntityMapper.get_by_id(id_)
    if entity.get_linked_entities('P46'):
        flash(_('Deletion not possible if subunits exists'), 'error')
        return redirect(url_for('place_view', id_=id_))
    system_type = entity.system_type
    parent = None if system_type == 'place' else LinkMapper.get_linked_entity(id_, 'P46', True)
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
    url = url_for('place_index')
    if parent:
        url = url_for('place_view', id_=parent.id) + '#tab-' + system_type
    return redirect(url)


@app.route('/place/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def place_update(id_):
    object_ = EntityMapper.get_by_id(id_)
    object_.set_dates()
    location = object_.get_linked_entity('P53')
    if object_.system_type == 'feature':
        form = build_form(FeatureForm, 'Feature', object_, request, location)
    elif object_.system_type == 'stratigraphic_unit':
        form = build_form(FeatureForm, 'Stratigraphic Unit', object_, request, location)
    elif object_.system_type == 'find':
        form = build_form(FeatureForm, 'Find', object_, request, location)
    else:
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
    if object_.system_type == 'place':
        form.alias.append_entry('')
    gis_data = GisMapper.get_all(object_.id)
    place = None
    feature = None
    stratigraphic_unit = None
    if object_.system_type == 'find':
        stratigraphic_unit = object_.get_linked_entity('P46', True)
        feature = stratigraphic_unit.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    if object_.system_type == 'stratigraphic_unit':
        feature = object_.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    elif object_.system_type == 'feature':
        place = object_.get_linked_entity('P46', True)
    return render_template('place/update.html', form=form, object_=object_, gis_data=gis_data,
                           place=place, feature=feature, stratigraphic_unit=stratigraphic_unit)


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
            if origin and origin.system_type == 'stratigraphic_unit':
                object_ = EntityMapper.insert('E22', form.name.data, 'find')
            else:
                system_type = 'place'
                if origin and origin.system_type == 'place':
                    system_type = 'feature'
                elif origin and origin.system_type == 'feature':
                    system_type = 'stratigraphic_unit'
                object_ = EntityMapper.insert('E18', form.name.data, system_type)
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
        if hasattr(form, 'alias'):
            for alias in form.alias.data:
                if alias.strip():  # check if it isn't empty
                    object_.link('P1', EntityMapper.insert('E41', alias))
        url = url_for('place_view', id_=object_.id)
        if origin:
            url = url_for(get_view_name(origin) + '_view', id_=origin.id) + '#tab-place'
            if get_view_name(origin) == 'reference':
                link_id = origin.link('P67', object_)
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif origin.system_type in ['place', 'feature', 'stratigraphic_unit']:
                url = url_for('place_view', id_=object_.id)
                origin.link('P46', object_)
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
