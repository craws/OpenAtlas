# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import FieldList, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import DateForm, build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.gis import GisMapper, InvalidGeomException
from openatlas.util.util import (display_remove_link, get_base_table_data, get_entity_data,
                                 get_profile_image_table_link, is_authorized, link, required_group,
                                 truncate_string, uc_first, was_modified)


class PlaceForm(DateForm):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    alias = FieldList(StringField(''), description=_('tooltip alias'))
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    gis_points = HiddenField(default='[]')
    gis_polygons = HiddenField(default='[]')
    gis_lines = HiddenField(default='[]')
    continue_ = HiddenField()
    opened = HiddenField()


class FeatureForm(DateForm):
    name = StringField(_('name'), [InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    gis_points = HiddenField()
    gis_polygons = HiddenField()
    gis_lines = HiddenField()
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/place')
@required_group('readonly')
def place_index():
    table = {'id': 'place', 'header': app.config['TABLE_HEADERS']['place'], 'data': []}
    for place in EntityMapper.get_by_system_type('place', nodes=True, aliases=True):
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
    elif origin and origin.system_type == 'stratigraphic unit':
        title = 'find'
        form = build_form(FeatureForm, 'Find')
    else:
        title = 'place'
        form = build_form(PlaceForm, 'Place')
    if origin \
            and origin.system_type not in ['place', 'feature', 'stratigraphic unit'] \
            and hasattr(form, 'insert_and_continue'):
        del form.insert_and_continue
    if form.validate_on_submit():
        return redirect(save(form, origin=origin))
    if title == 'place':
        form.alias.append_entry('')
    gis_data = GisMapper.get_all()
    place = None
    feature = None
    if origin and origin.system_type == 'stratigraphic unit':
        feature = origin.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    elif origin and origin.system_type == 'feature':
        place = origin.get_linked_entity('P46', True)
    return render_template('place/insert.html', form=form, title=title, place=place,
                           gis_data=gis_data, feature=feature, origin=origin)


@app.route('/place/view/<int:id_>')
@required_group('readonly')
def place_view(id_):
    object_ = EntityMapper.get_by_id(id_, nodes=True, aliases=True)
    location = object_.get_linked_entity('P53')
    tables = {
        'info': get_entity_data(object_, location),
        'file': {'id': 'files', 'data': [],
                 'header': app.config['TABLE_HEADERS']['file'] + [_('main image')]},
        'source': {'id': 'source', 'data': [], 'header': app.config['TABLE_HEADERS']['source']},
        'event': {'id': 'event', 'data': [], 'header': app.config['TABLE_HEADERS']['event']},
        'reference': {'id': 'reference', 'data': [],
                      'header': app.config['TABLE_HEADERS']['reference'] + ['page / link text']},
        'actor': {'id': 'actor', 'data': [],
                  'header': [_('actor'), _('property'), _('class'), _('first'), _('last')]}}
    if object_.system_type == 'place':
        tables['feature'] = {'id': 'feature', 'data': [],
                             'header': app.config['TABLE_HEADERS']['place'] + [_('description')]}
    if object_.system_type == 'feature':
        tables['stratigraphic-unit'] = {
            'id': 'stratigraphic', 'data': [],
            'header': app.config['TABLE_HEADERS']['place'] + [_('description')]}
    if object_.system_type == 'stratigraphic unit':
        tables['find'] = {'id': 'find', 'data': [],
                          'header': app.config['TABLE_HEADERS']['place'] + [_('description')]}
    profile_image_id = object_.get_profile_image_id()
    for link_ in object_.get_links('P67', True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':  # pragma: no cover
            extension = data[3].replace('.', '')
            data.append(get_profile_image_table_link(domain, object_, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if domain.view_name not in ['source', 'file']:
            data.append(truncate_string(link_.description))
            if domain.system_type == 'external reference':
                object_.external_references.append(link_)
            if is_authorized('editor'):
                url = url_for('reference_link_update', link_id=link_.id, origin_id=object_.id)
                data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('editor'):
            url = url_for('link_delete', id_=link_.id, origin_id=object_.id)
            data.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name]['data'].append(data)
    event_ids = []  # Keep track of already inserted events to prevent doubles
    for event in location.get_linked_entities(['P7'], True):
        tables['event']['data'].append(get_base_table_data(event))
        event_ids.append(event.id)
    for event in object_.get_linked_entities(['P24'], True):
        if event.id not in event_ids:  # Don't add again if already in table
            tables['event']['data'].append(get_base_table_data(event))
    has_subunits = False
    for entity in object_.get_linked_entities('P46'):
        has_subunits = True
        data = get_base_table_data(entity)
        data.append(truncate_string(entity.description))
        tables[entity.system_type.replace(' ', '-')]['data'].append(data)
    for link_ in location.get_links(['P74', 'OA8', 'OA9'], True):
        actor = EntityMapper.get_by_id(link_.domain.id)
        tables['actor']['data'].append([link(actor),
                                        g.properties[link_.property.code].name,
                                        actor.class_.name,
                                        actor.first,
                                        actor.last])
    gis_data = GisMapper.get_all(object_) if location else None
    if gis_data['gisPointSelected'] == '[]' and gis_data['gisPolygonSelected'] == '[]'\
            and gis_data['gisLineSelected'] == '[]':
        gis_data = None
    place = None
    feature = None
    stratigraphic_unit = None
    if object_.system_type == 'find':
        stratigraphic_unit = object_.get_linked_entity('P46', True)
        feature = stratigraphic_unit.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    elif object_.system_type == 'stratigraphic unit':
        feature = object_.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    elif object_.system_type == 'feature':
        place = object_.get_linked_entity('P46', True)
    return render_template('place/view.html', object_=object_, tables=tables, gis_data=gis_data,
                           place=place, feature=feature, stratigraphic_unit=stratigraphic_unit,
                           has_subunits=has_subunits, profile_image_id=profile_image_id)


@app.route('/place/delete/<int:id_>')
@required_group('editor')
def place_delete(id_):
    entity = EntityMapper.get_by_id(id_)
    parent = None if entity.system_type == 'place' else entity.get_linked_entity('P46', True)
    if entity.get_linked_entities('P46'):
        flash(_('Deletion not possible if subunits exists'), 'error')
        return redirect(url_for('place_view', id_=id_))
    entity.delete()
    logger.log_user(id_, 'delete')
    flash(_('entity deleted'), 'info')
    if parent:
        return redirect(url_for('place_view', id_=parent.id) + '#tab-' + entity.system_type)
    return redirect(url_for('place_index'))


@app.route('/place/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def place_update(id_):
    object_ = EntityMapper.get_by_id(id_, nodes=True, aliases=True)
    location = object_.get_linked_entity('P53')
    if object_.system_type == 'feature':
        form = build_form(FeatureForm, 'Feature', object_, request, location)
    elif object_.system_type == 'stratigraphic unit':
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
    if object_.system_type == 'place':
        for alias in object_.aliases.values():
            form.alias.append_entry(alias)
        form.alias.append_entry('')
    gis_data = GisMapper.get_all(object_)
    place = None
    feature = None
    stratigraphic_unit = None
    if object_.system_type == 'find':
        stratigraphic_unit = object_.get_linked_entity('P46', True)
        feature = stratigraphic_unit.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    if object_.system_type == 'stratigraphic unit':
        feature = object_.get_linked_entity('P46', True)
        place = feature.get_linked_entity('P46', True)
    elif object_.system_type == 'feature':
        place = object_.get_linked_entity('P46', True)
    return render_template('place/update.html', form=form, object_=object_, gis_data=gis_data,
                           place=place, feature=feature, stratigraphic_unit=stratigraphic_unit)


def save(form, object_=None, location=None, origin=None):
    g.cursor.execute('BEGIN')
    log_action = 'update'
    try:
        if object_:
            for alias in object_.get_linked_entities('P1'):
                alias.delete()
            GisMapper.delete_by_entity(location)
        else:
            log_action = 'insert'
            if origin and origin.system_type == 'stratigraphic unit':
                object_ = EntityMapper.insert('E22', form.name.data, 'find')
            else:
                system_type = 'place'
                if origin and origin.system_type == 'place':
                    system_type = 'feature'
                elif origin and origin.system_type == 'feature':
                    system_type = 'stratigraphic unit'
                object_ = EntityMapper.insert('E18', form.name.data, system_type)
            location = EntityMapper.insert('E53', 'Location of ' + form.name.data, 'place location')
            object_.link('P53', location)
        object_.name = form.name.data
        object_.description = form.description.data
        object_.set_dates(form)
        object_.update()
        object_.save_nodes(form)
        location.name = 'Location of ' + form.name.data
        location.update()
        location.save_nodes(form)
        if hasattr(form, 'alias'):
            for alias in form.alias.data:
                if alias.strip():  # Check if it isn't empty
                    object_.link('P1', EntityMapper.insert('E41', alias))
        url = url_for('place_view', id_=object_.id)
        if origin:
            url = url_for(origin.view_name + '_view', id_=origin.id) + '#tab-place'
            if origin.view_name == 'reference':
                link_id = origin.link('P67', object_)
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif origin.system_type in ['place', 'feature', 'stratigraphic unit']:
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
    except InvalidGeomException as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed because of invalid geom', e)
        flash(_('Invalid geom entered'), 'error')
        url = url_for('place_index') if log_action == 'insert' else url_for('place_view',
                                                                            id_=object_.id)
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('place_index') if log_action == 'insert' else url_for('place_view',
                                                                            id_=object_.id)
    return url
