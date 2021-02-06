import os
from typing import Any, Dict, List, Optional, Union

import psycopg2
from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis, InvalidGeomException
from openatlas.models.link import Link
from openatlas.models.overlay import Overlay
from openatlas.models.place import get_structure
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.display import link, uc_first
from openatlas.util.util import is_authorized, required_group, was_modified


@app.route('/insert/<class_>', methods=['POST', 'GET'])
@app.route('/insert/<class_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def insert(class_: str, origin_id: Optional[int] = None) -> Union[str, Response]:
    if class_ == 'reference system' and not is_authorized('manager'):
        abort(403)  # pragma: no cover
    origin = Entity.get_by_id(origin_id) if origin_id else None
    if class_ in app.config['CLASS_CODES']['actor']:
        # Todo: can't use g.classes[class_].name because it's already translated, needs fixing.
        form_name = {'E21': 'person', 'E74': 'group', 'E40': 'legal_body'}
        form = build_form(form_name[class_], code=class_, origin=origin)
    elif class_ in app.config['CLASS_CODES']['event']:
        # Todo: it's inconsistently to actor that event has only one form for different classes.
        form = build_form('event', origin=origin, code=class_)
    elif class_ == 'E84':
        form = build_form('information_carrier', origin=origin)
    else:
        form = build_form(class_, origin=origin)
    if form.validate_on_submit():
        return redirect(save(form, class_=class_, origin=origin))
    if hasattr(form, 'alias'):
        form.alias.append_entry('')
    view_name = app.config['CODE_CLASS'][class_] if class_ in g.classes else class_
    if class_ in ['feature', 'stratigraphic_unit', 'find', 'human_remains']:
        view_name = 'place'
    elif class_ in ['bibliography', 'edition', 'external_reference']:
        view_name = 'reference'
    geonames_module = False
    if origin:
        populate_insert_form(form, view_name, class_, origin)
    else:
        geonames_module = True if ReferenceSystem.get_by_name('GeoNames').forms else False

    # Archaeological sub units
    structure = None
    gis_data = None
    overlays = None
    if view_name == 'place':
        structure = get_structure(super_=origin)
        gis_data = Gis.get_all([origin] if origin else None, structure)
        overlays = Overlay.get_by_object(origin) if origin and origin.class_.code == 'E18' else None
    return render_template(
        'entity/insert.html',
        form=form,
        class_=class_,
        origin=origin,
        view_name=view_name,
        structure=structure,
        gis_data=gis_data,
        geonames_module=geonames_module,
        writeable=True if os.access(app.config['UPLOAD_DIR'], os.W_OK) else False,  # For files
        overlays=overlays,
        title=_(view_name),
        crumbs=add_crumbs(view_name, class_, origin, structure, insert_=True),)


def add_crumbs(view_name: str,
               class_: str,
               origin: Union[Entity, None],
               structure: Optional[Dict[str, Any]],
               insert_: Optional[bool] = False) -> List[Any]:
    crumbs = [[_(origin.view_name.replace('_', ' ')) if origin else _(view_name.replace('_', ' ')),
               url_for('index', class_=origin.view_name if origin else view_name)],
              link(origin)]
    if structure:
        crumbs = [[_('place'), url_for('index', class_='place')],
                  structure['place'] if origin.system_type != 'place' else '',
                  structure['feature'],
                  structure['stratigraphic_unit'],
                  link(origin)]
    if insert_:
        crumbs = crumbs + ['+ ' + (g.classes[class_].name if class_ in g.classes else uc_first(
            _(class_.replace('_', ' '))))]
    else:
        crumbs = crumbs + [_('edit')]
    return crumbs


@app.route('/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def update(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_, nodes=True, aliases=True)
    if entity.system_type == 'reference system' and not is_authorized('manager'):
        abort(403)  # pragma: no cover
    if not entity.view_name:
        abort(422)  # pragma: no cover

    # Archaeological sub units
    geonames_module = False
    structure = None
    location = None
    gis_data = None
    overlays = None

    if entity.view_name == 'actor':
        form = build_form(g.classes[entity.class_.code].name.lower().replace(' ', '_'), entity)
    elif entity.view_name in ['object', 'reference']:
        form = build_form(entity.system_type.replace(' ', '_'), entity)
    elif entity.view_name == 'place':
        structure = get_structure(entity)
        location = entity.get_linked_entity_safe('P53', nodes=True)
        gis_data = Gis.get_all([entity], structure)
        overlays = Overlay.get_by_object(entity)
        if entity.system_type == 'feature':
            form = build_form('feature', entity, location=location)
        elif entity.system_type == 'stratigraphic unit':
            form = build_form('stratigraphic_unit', entity, location=location)
        elif entity.system_type == 'find':
            form = build_form('find', entity, location=location)
        elif entity.system_type == 'human remains':
            form = build_form('human_remains', entity, location=location)
        else:
            geonames_module = True if ReferenceSystem.get_by_name('GeoNames').forms else False
            form = build_form('place', entity, location=location)
    else:
        form = build_form(entity.view_name, entity)

    if entity.view_name == 'event':
        form.event_id.data = entity.id
    elif entity.class_.code == 'E32':  # reference system
        form.name.render_kw['readonly'] = 'readonly'
    if form.validate_on_submit():
        if was_modified(form, entity):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            return render_template(
                'entity/update.html',
                form=form,
                entity=entity,
                structure=structure,
                modifier=link(logger.get_log_for_advanced_view(entity.id)['modifier']))
        return redirect(save(form, entity, location=location))
    populate_update_form(form, entity)
    return render_template('entity/update.html',
                           form=form,
                           entity=entity,
                           structure=structure,
                           gis_data=gis_data,
                           overlays=overlays,
                           geonames_module=geonames_module,
                           title=entity.name,
                           crumbs=add_crumbs(view_name=entity.view_name,
                                             class_=entity.class_.name,
                                             origin=entity,
                                             structure=structure))


def populate_insert_form(form: FlaskForm, view_name: str, class_: str, origin: Entity) -> None:
    if view_name == 'source':
        if origin and origin.class_.code == 'E84':
            form.information_carrier.data = [origin.id]
    if view_name == 'actor':
        if origin.system_type == 'place':
            form.residence.data = origin.id
    elif view_name == 'event':
        if origin.class_.code == 'E84':
            form.object.data = [origin.id]
        elif origin.class_.code == 'E18':
            if class_ == 'E9':
                form.place_from.data = origin.id
            else:
                form.place.data = origin.id


def populate_update_form(form: FlaskForm, entity: Entity) -> None:
    if hasattr(form, 'alias'):
        for alias in entity.aliases.values():
            form.alias.append_entry(alias)
        form.alias.append_entry('')
    if entity.view_name == 'actor':
        residence = entity.get_linked_entity('P74')
        form.residence.data = residence.get_linked_entity_safe('P53', True).id if residence else ''
        first = entity.get_linked_entity('OA8')
        form.begins_in.data = first.get_linked_entity_safe('P53', True).id if first else ''
        last = entity.get_linked_entity('OA9')
        form.ends_in.data = last.get_linked_entity_safe('P53', True).id if last else ''
    elif entity.view_name == 'event':
        super_event = entity.get_linked_entity('P117')
        form.event.data = super_event.id if super_event else ''
        if entity.class_.code == 'E9':  # Form data for move
            place_from = entity.get_linked_entity('P27')
            form.place_from.data = place_from.get_linked_entity_safe('P53',
                                                                     True).id if place_from else ''
            place_to = entity.get_linked_entity('P26')
            form.place_to.data = place_to.get_linked_entity_safe('P53', True).id if place_to else ''
            person_data = []
            object_data = []
            for entity in entity.get_linked_entities('P25'):
                if entity.class_.code == 'E21':
                    person_data.append(entity.id)
                elif entity.class_.code == 'E84':
                    object_data.append(entity.id)
            form.person.data = person_data
            form.object.data = object_data
        else:
            place = entity.get_linked_entity('P7')
            form.place.data = place.get_linked_entity_safe('P53', True).id if place else ''
        if entity.class_.code == 'E8':  # Form data for acquisition
            form.given_place.data = [entity.id for entity in entity.get_linked_entities('P24')]
    elif entity.view_name == 'source':
        form.information_carrier.data = [item.id for item in
                                         entity.get_linked_entities('P128', inverse=True)]


def save(form: FlaskForm,
         entity: Optional[Union[Entity, ReferenceSystem]] = None,
         class_: Optional[str] = '',
         origin: Optional[Entity] = None,
         location: Optional[Entity] = None) -> Union[str, Response]:
    g.cursor.execute('BEGIN')
    action = 'update'
    try:
        if not entity:
            action = 'insert'
            if class_ == 'source':
                entity = Entity.insert('E33', form.name.data, 'source content')
            elif class_ == 'file':
                entity = Entity.insert('E31', form.name.data, 'file')
            elif class_ == 'E84':
                entity = Entity.insert('E84', form.name.data, 'information carrier')
            elif class_ in ['place', 'human_remains', 'stratigraphic_unit', 'feature', 'find']:
                if class_ == 'human_remains':
                    entity = Entity.insert('E20', form.name.data, 'human remains')
                elif origin and origin.system_type == 'stratigraphic unit':
                    entity = Entity.insert('E22', form.name.data, 'find')
                else:
                    system_type = 'place'
                    if origin and origin.system_type == 'place':
                        system_type = 'feature'
                    elif origin and origin.system_type == 'feature':
                        system_type = 'stratigraphic unit'
                    entity = Entity.insert('E18', form.name.data, system_type)
                location = Entity.insert('E53', 'Location of ' + form.name.data, 'place location')
                entity.link('P53', location)
            elif class_ in ('bibliography', 'edition', 'external_reference'):
                entity = Entity.insert('E31', form.name.data, class_.replace('_', ' '))
            elif class_ == 'reference_system':
                entity = ReferenceSystem.insert_system(form)
            else:
                entity = Entity.insert(class_, form.name.data)
            if entity.view_name == 'file':
                file_ = request.files['file']
                # Add an 'a' to prevent emtpy filename, this won't affect stored information
                filename = secure_filename('a' + file_.filename)  # type: ignore
                new_name = '{id}.{ext}'.format(id=entity.id, ext=filename.rsplit('.', 1)[1].lower())
                file_.save(str(app.config['UPLOAD_DIR'] / new_name))

        if entity.class_.code == 'E32':  # reference system
            entity.name = entity.name if hasattr(entity, 'system') and entity.system \
                else form.name.data
            entity.description = form.description.data
            entity.website_url = form.website_url.data if form.website_url.data else None
            entity.resolver_url = form.resolver_url.data if form.resolver_url.data else None
            entity.placeholder = form.placeholder.data if form.placeholder.data else None
            entity.update_system(form)
            if hasattr(form, 'forms'):
                entity.add_forms(form)
        else:
            entity.update(form)
        update_links(entity, form, action, location)
        url = link_and_get_redirect_url(form, entity, class_, origin)
        logger.log_user(entity.id, action)
        g.cursor.execute('COMMIT')
        flash(_('entity created') if action == 'insert' else _('info update'), 'info')
    except InvalidGeomException as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed because of invalid geom', e)
        flash(_('Invalid geom entered'), 'error')
        if action == 'update':
            url = url_for('update', id_=entity.id, origin_id=origin.id if origin else None)
        else:
            url = url_for('index', class_=entity.view_name)
    except psycopg2.IntegrityError:
        g.cursor.execute('ROLLBACK')
        flash(_('error name exists'), 'error')  # Could happen e.g. with reference system
        url = url_for('index', class_='reference_system')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        if action == 'update':
            url = url_for('update', id_=entity.id, origin_id=origin.id if origin else None)
        else:
            view_name = class_
            if view_name in ['feature', 'stratigraphic_unit', 'find', 'human_remains']:
                view_name = 'place'
            url = url_for('index', class_=view_name)
    return url


def update_links(entity: Entity, form, action: str, location: Optional[Entity] = None) -> None:
    # Todo: it would be better to only save changes and not delete/recreate all links

    if entity.view_name in ['actor', 'event', 'place']:
        ReferenceSystem.update_links(form, entity)

    if entity.view_name == 'actor':
        if action == 'update':
            entity.delete_links(['P74', 'OA8', 'OA9'])
        if form.residence.data:
            object_ = Entity.get_by_id(form.residence.data)
            entity.link('P74', object_.get_linked_entity_safe('P53'))
        if form.begins_in.data:
            object_ = Entity.get_by_id(form.begins_in.data)
            entity.link('OA8', object_.get_linked_entity_safe('P53'))
        if form.ends_in.data:
            object_ = Entity.get_by_id(form.ends_in.data)
            entity.link('OA9', object_.get_linked_entity_safe('P53'))
    if entity.view_name == 'event':
        if action == 'update':
            entity.delete_links(['P7', 'P24', 'P25', 'P26', 'P27', 'P117'])
        if form.event.data:
            entity.link_string('P117', form.event.data)
        if hasattr(form, 'place') and form.place.data:
            entity.link('P7', Link.get_linked_entity_safe(int(form.place.data), 'P53'))
        if entity.class_.code == 'E8' and form.given_place.data:  # Link place for acquisition
            entity.link_string('P24', form.given_place.data)
        if entity.class_.code == 'E9':  # Move
            if form.object.data:  # Moved objects
                entity.link_string('P25', form.object.data)
            if form.person.data:  # Moved persons
                entity.link_string('P25', form.person.data)
            if form.place_from.data:  # Link place for move from
                linked_place = Link.get_linked_entity_safe(int(form.place_from.data), 'P53')
                entity.link('P27', linked_place)
            if form.place_to.data:  # Link place for move to
                entity.link('P26', Link.get_linked_entity_safe(int(form.place_to.data), 'P53'))
    elif entity.view_name == 'place':
        if action == 'update':
            Gis.delete_by_entity(entity)
        location.update(form)
        Gis.insert(location, form)
    elif entity.view_name == 'source':
        if action == 'update':
            entity.delete_links(['P128'], inverse=True)
        if form.information_carrier.data:
            entity.link_string('P128', form.information_carrier.data, inverse=True)


def link_and_get_redirect_url(form: FlaskForm,
                              entity: Entity,
                              class_: Optional[str] = '',
                              origin: Optional[Entity] = None) -> str:
    url = url_for('entity_view', id_=entity.id)
    if origin:
        url = url_for('entity_view', id_=origin.id) + '#tab-' + entity.view_name
        if origin.view_name == 'reference':
            link_id = origin.link('P67', entity)[0]
            url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
        elif entity.system_type == 'file':
            entity.link('P67', origin)
            url = url_for('entity_view', id_=origin.id) + '#tab-file'
        elif entity.view_name == 'reference':
            link_id = entity.link('P67', origin)[0]
            url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
        elif origin.view_name in ['place', 'feature', 'stratigraphic unit']:
            url = url_for('entity_view', id_=entity.id)
            origin.link('P46', entity)
        elif origin.view_name in ['source', 'file']:
            origin.link('P67', entity)
        elif entity.view_name == 'source' and origin.class_.code != 'E84':
            entity.link('P67', origin)
        elif origin.view_name == 'event':  # Involvement, coming from actor
            link_id = origin.link('P11', entity)[0]
            url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
        elif origin.view_name == 'actor' and entity.view_name == 'event':
            link_id = entity.link('P11', origin)[0]  # Involvement, coming from event
            url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
        elif origin.view_name == 'actor' and entity.view_name == 'actor':
            link_id = origin.link('OA7', entity)[0]  # Actor with actor relation
            url = url_for('relation_update', id_=link_id, origin_id=origin.id)
    if hasattr(form, 'continue_') and form.continue_.data == 'yes':
        url = url_for('insert', class_=class_, origin_id=origin.id if origin else None)
    elif hasattr(form, 'continue_') and form.continue_.data in ['sub', 'human_remains']:
        class_ = form.continue_.data
        if class_ == 'sub':
            if entity.system_type == 'place':
                class_ = 'feature'
            elif entity.system_type == 'feature':
                class_ = 'stratigraphic_unit'
            elif entity.system_type == 'stratigraphic unit':
                class_ = 'find'
        url = url_for('insert', class_=class_, origin_id=entity.id)
    return url
