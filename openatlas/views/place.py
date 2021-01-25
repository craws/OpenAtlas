from typing import Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis, InvalidGeomException
from openatlas.models.overlay import Overlay
from openatlas.models.place import get_structure
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.display import link
from openatlas.util.util import required_group, was_modified


@app.route('/place/insert', methods=['POST', 'GET'])
@app.route('/place/insert/<int:origin_id>', methods=['POST', 'GET'])
@app.route('/place/insert/<int:origin_id>/<system_type>', methods=['POST', 'GET'])
@required_group('contributor')
def place_insert(origin_id: Optional[int] = None,
                 system_type: Optional[str] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    geonames_module = False
    title = 'place'
    form = build_form('place', origin=origin)
    if not origin:
        geonames_module = True if ReferenceSystem.get_by_name('GeoNames').forms else False
    elif origin.system_type == 'place':
        title = 'feature'
        form = build_form('feature', origin=origin)
    elif origin.system_type == 'feature':
        title = 'stratigraphic unit'
        form = build_form('stratigraphic_unit', origin=origin)
    elif origin.system_type == 'stratigraphic unit' and system_type == 'human_remains':
        title = 'human remains'
        form = build_form('human_remains')
    elif origin.system_type == 'stratigraphic unit':
        title = 'find'
        form = build_form('find')

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
                           geonames_module=geonames_module,
                           overlays=overlays)


@app.route('/place/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def place_update(id_: int) -> Union[str, Response]:
    object_ = Entity.get_by_id(id_, nodes=True, aliases=True, view_name='place')
    location = object_.get_linked_entity_safe('P53', nodes=True)
    geonames_module = False
    if object_.system_type == 'feature':
        form = build_form('feature', object_, location=location)
    elif object_.system_type == 'stratigraphic unit':
        form = build_form('stratigraphic_unit', object_, location=location)
    elif object_.system_type == 'find':
        form = build_form('find', object_, location=location)
    elif object_.system_type == 'human remains':
        form = build_form('human_remains', object_, location=location)
    else:
        geonames_module = True if ReferenceSystem.get_by_name('GeoNames').forms else False
        form = build_form('place', object_, location=location)
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
    structure = get_structure(object_)
    return render_template('place/update.html',
                           form=form,
                           object_=object_,
                           structure=structure,
                           gis_data=Gis.get_all([object_], structure),
                           overlays=Overlay.get_by_object(object_),
                           geonames_module=geonames_module)


def save(form: FlaskForm,
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
        ReferenceSystem.update_links(form, object_)
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
        if hasattr(form, 'continue_') and form.continue_.data == 'yes':
            url = url_for('place_insert',
                          origin_id=origin.id if origin else None,
                          system_type=system_type if system_type else None)
        elif hasattr(form, 'continue_') and form.continue_.data in ['sub', 'human_remains']:
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
