from typing import Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import (BooleanField, FieldList, HiddenField, IntegerField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import InputRequired, Optional as OptValidator

from openatlas import app, logger
from openatlas.forms.date import DateForm
from openatlas.forms.util import build_form2
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis, InvalidGeomException
from openatlas.models.overlay import Overlay
from openatlas.models.place import get_structure
from openatlas.models.reference import Reference
from openatlas.models.user import User
from openatlas.util.display import (add_edit_link, add_remove_link, get_base_table_data,
                                    get_entity_data, get_profile_image_table_link, link, uc_first)
from openatlas.util.tab import Tab
from openatlas.util.table import Table
from openatlas.util.util import is_authorized, required_group, was_modified


class PlaceForm(DateForm):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    geonames_id = IntegerField('GeoNames Id', [OptValidator()])
    geonames_precision = SelectField(choices=app.config['REFERENCE_PRECISION'],
                                     default='close match')
    wikidata_id = StringField('Wikidata Id', [OptValidator()])
    wikidata_precision = SelectField(choices=app.config['REFERENCE_PRECISION'], default='')
    alias = FieldList(StringField(''), description=_('tooltip alias'))
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    insert_continue_sub = SubmitField(_('insert and continue'))
    gis_points = HiddenField(default='[]')
    gis_polygons = HiddenField(default='[]')
    gis_lines = HiddenField(default='[]')
    continue_ = HiddenField()
    opened = HiddenField()

    def validate(self) -> bool:
        valid = DateForm.validate(self)
        # Todo: remove no cover after form refactor
        if self.wikidata_id.data:  # pragma: no cover
            if self.wikidata_id.data[0].upper() != 'Q' or not self.wikidata_id.data[1:].isdigit():
                self.wikidata_id.errors.append(uc_first(_('wrong format')))
                valid = False
            else:
                self.wikidata_id.data = uc_first(self.wikidata_id.data)
        for name in g.external:
            if hasattr(self, name + '_id'):
                if getattr(self, name + '_id').data and not getattr(self, name + '_precision').data:
                    valid = False
                    getattr(self, name + '_id').errors.append(uc_first(_('precision required')))
        return valid


class FeatureForm(DateForm):
    name = StringField(_('name'), [InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    gis_points = HiddenField(default='[]')
    gis_polygons = HiddenField(default='[]')
    gis_lines = HiddenField(default='[]')
    insert_and_continue = SubmitField(_('insert and continue'))
    insert_continue_sub = SubmitField(_('insert and continue'))
    insert_continue_human_remains = SubmitField(_('insert and continue'))
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
    for place in Entity.get_by_system_type('place',
                                           nodes=True,
                                           aliases=current_user.settings['table_show_aliases']):
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
        form = build_form2(FeatureForm, 'Feature')
        form.insert_continue_sub.label.text += ' ' + _('with') + ' ' + _('stratigraphic unit')
        del form.insert_continue_human_remains
    elif origin and origin.system_type == 'feature':
        title = 'stratigraphic unit'
        form = build_form2(FeatureForm, 'Stratigraphic Unit')
        form.insert_continue_sub.label.text += ' ' + _('with') + ' ' + _('find')
        form.insert_continue_human_remains.label.text += ' ' + _('with') + ' ' + _('human remains')
    elif origin and origin.system_type == 'stratigraphic unit':
        if system_type == 'human_remains':  # URL param system_type only used for human remains
            title = 'human remains'
            form = build_form2(FeatureForm, 'Human Remains')
        else:
            title = 'find'
            form = build_form2(FeatureForm, 'Find')
        del form.insert_continue_sub, form.insert_continue_human_remains
    else:
        title = 'place'
        form = build_form2(PlaceForm, 'Place')
        form.insert_continue_sub.label.text += ' ' + _('with') + ' ' + _('feature')
        geonames_buttons = True if current_user.settings['module_geonames'] else False
        if origin:
            del form.insert_and_continue, form.insert_continue_sub
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


@app.route('/place/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def place_update(id_: int) -> Union[str, Response]:
    object_ = Entity.get_by_id(id_, nodes=True, aliases=True, view_name='place')
    location = object_.get_linked_entity_safe('P53', nodes=True)
    geonames_buttons = False
    if object_.system_type == 'feature':
        form = build_form2(FeatureForm, 'Feature', object_, request, location)
    elif object_.system_type == 'stratigraphic unit':
        form = build_form2(FeatureForm, 'Stratigraphic Unit', object_, request, location)
    elif object_.system_type == 'find':
        form = build_form2(FeatureForm, 'Find', object_, request, location)
    elif object_.system_type == 'human remains':
        form = build_form2(FeatureForm, 'Human Remains', object_, request, location)
    else:
        geonames_buttons = True if current_user.settings['module_geonames'] else False
        form = build_form2(PlaceForm, 'Place', object_, request, location)
    if hasattr(form, 'insert_continue_sub'):
        del form.insert_continue_sub
    if hasattr(form, 'insert_continue_human_remains'):
        del form.insert_continue_human_remains
    if form.validate_on_submit():
        if was_modified(form, object_):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(object_.id)['modifier'])
            return render_template('place/update.html',
                                   form=form,
                                   structure=get_structure(object_),
                                   object_=object_,
                                   modifier=modifier)
        save(form, object_, location)
        return redirect(url_for('entity_view', id_=id_))

    if object_.system_type == 'place':
        for alias in object_.aliases.values():
            form.alias.append_entry(alias)
        form.alias.append_entry('')
    for name in g.external:
        if hasattr(form, name + '_id') and current_user.settings['module_' + name]:
            link_ = Reference.get_link(object_, name)
            if link_ and not getattr(form, name + '_id').data:
                reference = link_.domain
                getattr(form, name + '_id').data = reference.name if reference else ''
                getattr(form, name + '_precision').data = g.nodes[link_.type.id].name
    structure = get_structure(object_)
    return render_template('place/update.html',
                           form=form,
                           object_=object_,
                           structure=structure,
                           gis_data=Gis.get_all([object_], structure),
                           overlays=Overlay.get_by_object(object_),
                           geonames_buttons=geonames_buttons)


def place_view(obj: Entity) -> str:
    tabs = {name: Tab(name, origin=obj) for name in [
        'info', 'source', 'event', 'actor', 'reference', 'file']}
    if obj.system_type == 'place':
        tabs['feature'] = Tab('feature', origin=obj)
    elif obj.system_type == 'feature':
        tabs['stratigraphic_unit'] = Tab('stratigraphic_unit', origin=obj)
    elif obj.system_type == 'stratigraphic unit':
        tabs['find'] = Tab('find', origin=obj,)
        tabs['human_remains'] = Tab('human_remains', origin=obj)
    obj.note = User.get_note(obj)
    location = obj.get_linked_entity_safe('P53', nodes=True)
    profile_image_id = obj.get_profile_image_id()
    if current_user.settings['module_map_overlay'] and is_authorized('editor'):
        tabs['file'].table.header.append(uc_first(_('overlay')))
    overlays = Overlay.get_by_object(obj)
    for link_ in obj.get_links('P67', inverse=True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':
            extension = data[3]
            data.append(get_profile_image_table_link(domain, obj, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
            if is_authorized('editor') and current_user.settings['module_map_overlay']:
                if extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    if domain.id in overlays:
                        data = add_edit_link(data,
                                             url_for('overlay_update', id_=overlays[domain.id].id))
                    else:
                        data.append(link(_('link'), url_for('overlay_insert',
                                                            image_id=domain.id,
                                                            place_id=obj.id,
                                                            link_id=link_.id)))
                else:  # pragma: no cover
                    data.append('')
        if domain.view_name not in ['source', 'file']:
            data.append(link_.description)
            data = add_edit_link(
                data,
                url_for('reference_link_update', link_id=link_.id, origin_id=obj.id))
            if domain.system_type.startswith('external reference'):
                obj.external_references.append(link_)
        data = add_remove_link(data, domain.name, link_, obj, domain.view_name)
        tabs[domain.view_name].table.rows.append(data)
    event_ids = []  # Keep track of already inserted events to prevent doubles
    for event in location.get_linked_entities(['P7', 'P26', 'P27'], inverse=True):
        tabs['event'].table.rows.append(get_base_table_data(event))
        event_ids.append(event.id)
    for event in obj.get_linked_entities('P24', inverse=True):
        if event.id not in event_ids:  # Don't add again if already in table
            tabs['event'].table.rows.append(get_base_table_data(event))
    for link_ in location.get_links(['P74', 'OA8', 'OA9'], inverse=True):
        actor = Entity.get_by_id(link_.domain.id, view_name='actor')
        tabs['actor'].table.rows.append([link(actor),
                                         g.properties[link_.property.code].name,
                                         actor.class_.name,
                                         actor.first,
                                         actor.last,
                                         actor.description])
    structure = get_structure(obj)
    if structure:
        for entity in structure['subunits']:
            data = get_base_table_data(entity)
            tabs[entity.system_type.replace(' ', '_')].table.rows.append(data)
    gis_data = Gis.get_all([obj], structure)
    if gis_data['gisPointSelected'] == '[]' \
            and gis_data['gisPolygonSelected'] == '[]' \
            and gis_data['gisLineSelected'] == '[]' \
            and (not structure or not structure['super_id']):
        gis_data = {}
    return render_template('place/view.html',
                           entity=obj,
                           tabs=tabs,
                           overlays=overlays,
                           info=get_entity_data(obj, location),
                           gis_data=gis_data,
                           structure=structure,
                           profile_image_id=profile_image_id)


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
        Reference.update(form, object_)
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
        elif form.continue_.data in ['sub', 'human_remains']:
            url = url_for('place_insert', origin_id=object_.id, system_type=form.continue_.data)
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
