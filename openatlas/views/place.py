from typing import Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import (BooleanField, FieldList, HiddenField, IntegerField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import InputRequired, Optional as OptValidator

from openatlas import app, logger
from openatlas.forms.date import DateForm
from openatlas.forms.forms import build_form, build_table_form
from openatlas.models.entity import Entity
from openatlas.models.geonames import Geonames
from openatlas.models.gis import Gis, InvalidGeomException
from openatlas.models.overlay import Overlay
from openatlas.models.place import get_structure
from openatlas.util.table import Table
from openatlas.util.util import get_base_table_data, link, required_group, uc_first, was_modified
from openatlas.views.reference import AddReferenceForm


class PlaceForm(DateForm):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    geonames_id = IntegerField('GeoNames Id', [OptValidator()], description=_('tooltip geonames'))
    geonames_precision = BooleanField('exact match')
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
    gis_points = HiddenField(default='[]')
    gis_polygons = HiddenField(default='[]')
    gis_lines = HiddenField(default='[]')
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/place')
@app.route('/place/<action>/<int:id_>')
@required_group('readonly')
def place_index(action: Optional[str] = None, id_: Optional[int] = None) -> Union[str, Response]:
    if id_ and action == 'delete':
        entity = Entity.get_by_id(id_)
        parent = None if entity.system_type == 'place' else entity.get_linked_entity('P46', True)
        if entity.get_linked_entities(['P46']):
            flash(_('Deletion not possible if subunits exists'), 'error')
            return redirect(url_for('entity_view', id_=id_))
        entity.delete()
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
        if parent:
            tab = '#tab-' + entity.system_type.replace(' ', '-')
            return redirect(url_for('entity_view', id_=parent.id) + tab)
    table = Table(Table.HEADERS['place'], defs=[{'className': 'dt-body-right', 'targets': [2, 3]}])
    aliases = current_user.settings['table_show_aliases']
    for place in Entity.get_by_system_type('place', nodes=True, aliases=aliases):
        table.rows.append(get_base_table_data(place))
    return render_template('place/index.html', table=table, gis_data=Gis.get_all())


@app.route('/place/insert', methods=['POST', 'GET'])
@app.route('/place/insert/<int:origin_id>', methods=['POST', 'GET'])
@app.route('/place/insert/<int:origin_id>/<system_type>', methods=['POST', 'GET'])
@required_group('contributor')
def place_insert(origin_id: Optional[int] = None,
                 system_type: Optional[str] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    geonames_buttons = False
    if origin and origin.system_type == 'place':
        title = 'feature'
        form = build_form(FeatureForm, 'Feature')
    elif origin and origin.system_type == 'feature':
        title = 'stratigraphic unit'
        form = build_form(FeatureForm, 'Stratigraphic Unit')
    elif origin and origin.system_type == 'stratigraphic unit':
        if system_type == 'human_remains':  # URL param system_type only used for human remains
            title = 'human remains'
            form = build_form(FeatureForm, 'Human Remains')
        else:
            title = 'find'
            form = build_form(FeatureForm, 'Find')
    else:
        title = 'place'
        form = build_form(PlaceForm, 'Place')
        geonames_buttons = True if current_user.settings['module_geonames'] else False
    if origin and origin.system_type not in ['place', 'feature', 'stratigraphic unit'] \
            and hasattr(form, 'insert_and_continue'):
        del form.insert_and_continue
    if hasattr(form, 'geonames_id') and not current_user.settings['module_geonames']:
        del form.geonames_id, form.geonames_precision  # pragma: no cover
    if form.validate_on_submit():
        return redirect(save(form, origin=origin, system_type=system_type))

    if title == 'place':
        form.alias.append_entry('')
    structure = get_structure(super_=origin)
    gis_data = Gis.get_all([origin] if origin else None, structure)
    overlays = Overlay.get_by_object(origin) if origin and origin.class_.code == 'E18' else None
    return render_template('place/insert.html',
                           form=form,
                           title=title,
                           origin=origin,
                           structure=structure,
                           gis_data=gis_data,
                           geonames_buttons=geonames_buttons,
                           overlays=overlays)


@app.route('/place/add/source/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def place_add_source(id_: int) -> Union[str, Response]:
    object_ = Entity.get_by_id(id_, view_name='place')
    if request.method == 'POST':
        if request.form['checkbox_values']:
            object_.link_string('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-source')
    form = build_table_form('source', object_.get_linked_entities('P67', inverse=True))
    return render_template('add_source.html', entity=object_, form=form)


@app.route('/place/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def place_add_reference(id_: int) -> Union[str, Response]:
    object_ = Entity.get_by_id(id_, view_name='place')
    form = AddReferenceForm()
    if form.validate_on_submit():
        object_.link_string('P67', form.reference.data, description=form.page.data, inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-reference')
    form.page.label.text = uc_first(_('page / link text'))
    return render_template('add_reference.html', entity=object_, form=form)


@app.route('/place/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def place_add_file(id_: int) -> Union[str, Response]:
    object_ = Entity.get_by_id(id_, view_name='place')
    if request.method == 'POST':
        if request.form['checkbox_values']:
            object_.link_string('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-file')
    form = build_table_form('file', object_.get_linked_entities('P67', inverse=True))
    return render_template('add_file.html', entity=object_, form=form)


@app.route('/place/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def place_update(id_: int) -> Union[str, Response]:
    object_ = Entity.get_by_id(id_, nodes=True, aliases=True, view_name='place')
    location = object_.get_linked_entity_safe('P53', nodes=True)
    geonames_buttons = False
    if object_.system_type == 'feature':
        form = build_form(FeatureForm, 'Feature', object_, request, location)
    elif object_.system_type == 'stratigraphic unit':
        form = build_form(FeatureForm, 'Stratigraphic Unit', object_, request, location)
    elif object_.system_type == 'find':
        form = build_form(FeatureForm, 'Find', object_, request, location)
    elif object_.system_type == 'human remains':
        form = build_form(FeatureForm, 'Human Remains', object_, request, location)
    else:
        geonames_buttons = True if current_user.settings['module_geonames'] else False
        form = build_form(PlaceForm, 'Place', object_, request, location)
    if hasattr(form, 'geonames_id') and not current_user.settings['module_geonames']:
        del form.geonames_id, form.geonames_precision  # pragma: no cover
    if form.validate_on_submit():
        if was_modified(form, object_):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(object_.id)['modifier'])
            return render_template('place/update.html',
                                   form=form,
                                   object_=object_,
                                   modifier=modifier)
        save(form, object_, location)
        return redirect(url_for('entity_view', id_=id_))
    if object_.system_type == 'place':
        for alias in object_.aliases.values():
            form.alias.append_entry(alias)
        form.alias.append_entry('')
    if hasattr(form, 'geonames_id') and current_user.settings['module_geonames']:
        geonames_link = Geonames.get_geonames_link(object_)
        if geonames_link:
            geonames_entity = geonames_link.domain
            form.geonames_id.data = geonames_entity.name if geonames_entity else ''
            exact_match = True if g.nodes[geonames_link.type.id].name == 'exact match' else False
            form.geonames_precision.data = exact_match
    structure = get_structure(object_)
    return render_template('place/update.html',
                           form=form,
                           object_=object_,
                           structure=structure,
                           gis_data=Gis.get_all([object_], structure),
                           overlays=Overlay.get_by_object(object_),
                           geonames_buttons=geonames_buttons)


def save(form: DateForm,
         object__: Optional[Entity] = None,
         location_: Optional[Entity] = None,
         origin: Optional[Entity] = None,
         system_type: Optional[str] = None) -> str:
    g.cursor.execute('BEGIN')
    log_action = 'update'
    try:
        if object__ and location_:
            object_ = object__
            location = location_
            Gis.delete_by_entity(location)
        else:
            log_action = 'insert'
            if system_type == 'human_remains':
                object_ = Entity.insert('E20', form.name.data, 'human remains')
            elif origin and origin.system_type == 'stratigraphic unit':
                object_ = Entity.insert('E22', form.name.data, 'find')
            else:
                system_type = 'place'
                if origin and origin.system_type == 'place':
                    system_type = 'feature'
                elif origin and origin.system_type == 'feature':
                    system_type = 'stratigraphic unit'
                object_ = Entity.insert('E18', form.name.data, system_type)
            location = Entity.insert('E53', 'Location of ' + form.name.data, 'place location')
            object_.link('P53', location)
        object_.update(form)
        location.update(form)
        if hasattr(form, 'geonames_id') and current_user.settings['module_geonames']:
            Geonames.update_geonames(form, object_)
        url = url_for('entity_view', id_=object_.id)
        if origin:
            url = url_for('entity_view', id_=origin.id) + '#tab-place'
            if origin.view_name == 'reference':
                link_id = origin.link('P67', object_)[0]
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif origin.system_type in ['place', 'feature', 'stratigraphic unit']:
                url = url_for('entity_view', id_=object_.id)
                origin.link('P46', object_)
            else:
                origin.link('P67', object_)
        Gis.insert(location, form)
        g.cursor.execute('COMMIT')
        if form.continue_.data == 'yes':
            url = url_for('place_insert',
                          origin_id=origin.id if origin else None,
                          system_type=system_type if system_type else None)
        logger.log_user(object_.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except InvalidGeomException as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed because of invalid geom', e)
        flash(_('Invalid geom entered'), 'error')
        url = url_for('place_index') if log_action == 'insert' else url_for('place_index')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('place_index') if log_action == 'insert' else url_for('place_index')
    return url
