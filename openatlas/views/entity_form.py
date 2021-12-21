import os
from typing import Any, Dict, List, Optional, Union

from flask import flash, g, render_template, session, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.database.connect import Transaction
from openatlas.forms.form import build_form
from openatlas.forms.util import (
    populate_insert_form, populate_update_form, process_form_data)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis, InvalidGeomException
from openatlas.models.overlay import Overlay
from openatlas.models.place import get_structure
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.util.image_processing import ImageProcessing
from openatlas.util.util import (
    is_authorized, link, required_group, was_modified)


@app.route('/insert/<class_>', methods=['POST', 'GET'])
@app.route('/insert/<class_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def insert(
        class_: str,
        origin_id: Optional[int] = None) -> Union[str, Response]:
    check_insert_access(class_)
    origin = Entity.get_by_id(origin_id) if origin_id else None
    form = build_form(class_, origin=origin)
    if form.validate_on_submit():
        if class_ == 'file':
            return redirect(insert_files(form, origin))
        return redirect(save(form, class_=class_, origin=origin))
    populate_insert_form(form, class_, origin)
    place_info = get_place_info_for_insert(g.classes[class_].view, origin)
    return render_template(
        'entity/insert.html',
        form=form,
        view_name=g.classes[class_].view,
        gis_data=place_info['gis_data'],
        geonames_module=check_geonames_module(class_),
        writable=os.access(app.config['UPLOAD_DIR'], os.W_OK),
        overlays=place_info['overlays'],
        title=_(g.classes[class_].view),
        crumbs=add_crumbs(
            class_,
            origin,
            place_info['structure'],
            insert_=True))


@app.route('/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def update(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_, types=True, aliases=True)
    check_update_access(entity)
    place_info = get_place_info_for_update(entity)
    form = build_form(
        entity.class_.name,
        entity,
        location=place_info['location'])
    if form.validate_on_submit():
        if isinstance(entity, Type) and not check_type(entity, form):
            return redirect(url_for('view', id_=entity.id))
        if was_modified(form, entity):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            return render_template(
                'entity/update.html',
                form=form,
                entity=entity,
                modifier=link(logger.get_log_info(entity.id)['modifier']))
        return redirect(save(form, entity))
    populate_update_form(form, entity)
    if entity.class_.view in ['artifact', 'place']:
        entity.set_image_for_places()
    return render_template(
        'entity/update.html',
        form=form,
        entity=entity,
        gis_data=place_info['gis_data'],
        overlays=place_info['overlays'],
        geonames_module=check_geonames_module(entity.class_.name),
        title=entity.name,
        crumbs=add_crumbs(
            class_=entity.class_.name,
            origin=entity,
            structure=place_info['structure']))


def add_crumbs(
        class_: str,
        origin: Union[Entity, None],
        structure: Optional[Dict[str, Any]],
        insert_: Optional[bool] = False) -> List[Any]:
    view = g.classes[class_].view
    label = origin.class_.name if origin else view
    if label in g.class_view_mapping:
        label = g.class_view_mapping[label]
    label = _(label.replace('_', ' '))
    crumbs = [
        [label, url_for('index', view=origin.class_.view if origin else view)],
        link(origin)]
    if structure:
        crumbs = [
            [_('place'), url_for('index', view='place')],
            structure['place']
            if origin and origin.class_.name != 'place' else '',
            structure['feature'],
            structure['stratigraphic_unit'],
            link(origin)]
    if view == 'type':
        crumbs = [[_('types'), url_for('type_index')]]
        if isinstance(origin, Type) and origin.root:
            for type_id in origin.root:
                crumbs += [link(g.types[type_id])]
        crumbs += [origin]
    sibling_count = 0
    if origin \
            and origin.class_.name == 'stratigraphic_unit' \
            and structure \
            and insert_:
        for item in structure['siblings']:
            if item.class_.name == class_:  # pragma: no cover
                sibling_count += 1
    siblings = f" ({sibling_count} {_('exists')})" if sibling_count else ''
    return crumbs + \
        [f'+ {g.classes[class_].label}{siblings}' if insert_ else _('edit')]


def check_geonames_module(class_: str) -> bool:
    return class_ == 'place' and ReferenceSystem.get_by_name('GeoNames').classes


def check_insert_access(class_: str) -> None:
    if class_ not in g.classes \
            or not g.classes[class_].view \
            or not is_authorized(g.classes[class_].write_access):
        abort(403)  # pragma: no cover


def check_update_access(entity: Entity) -> None:
    check_insert_access(entity.class_.name)
    if isinstance(entity, Type) and (
            entity.category == 'system'
            or entity.category == 'standard' and not entity.root):
        abort(403)


def check_type(entity: Type, form: FlaskForm) -> bool:
    valid = True
    root = g.types[entity.root[0]]
    new_super_id = getattr(form, str(root.id)).data
    new_super = g.types[int(new_super_id)] if new_super_id else None
    if new_super:
        if new_super.id == entity.id:
            flash(_('error type self as super'), 'error')
            valid = False
        if new_super.root and entity.id in new_super.root:
            flash(_('error type sub as super'), 'error')
            valid = False
    return valid


def get_place_info_for_insert(
        class_view: str,
        origin: Optional[Entity]) -> Dict[str, Any]:
    if class_view not in ['artifact', 'place']:
        return {'structure': None, 'gis_data': None, 'overlays': None}
    structure = get_structure(super_=origin)
    return {
        'structure': structure,
        'gis_data': Gis.get_all([origin] if origin else None, structure),
        'overlays': Overlay.get_by_object(origin)
        if origin and origin.class_.view == 'place' else None}


def get_place_info_for_update(entity: Entity) -> Dict[str, Any]:
    if entity.class_.view not in ['artifact', 'place']:
        return {
            'structure': None,
            'gis_data': None,
            'overlays': None,
            'location': None}
    structure = get_structure(entity)
    return {
        'structure': structure,
        'gis_data': Gis.get_all([entity], structure),
        'overlays': Overlay.get_by_object(entity),
        'location': entity.get_linked_entity_safe('P53', types=True)}


def insert_files(
        form: FlaskForm,
        origin: Optional[Entity] = None) -> Union[str, Response]:
    filenames = []
    url = url_for('index', view=g.classes['file'].view)
    try:
        Transaction.begin()
        entity_name = form.name.data.strip()
        for count, file in enumerate(form.file.data):
            entity = Entity.insert('file', file.filename)
            url = get_redirect_url(form, entity, 'file', origin)
            # Add 'a' to prevent emtpy temporary filename, has no side effects
            filename = secure_filename(f'a{file.filename}')
            new_name = f"{entity.id}.{filename.rsplit('.', 1)[1].lower()}"
            file.save(str(app.config['UPLOAD_DIR'] / new_name))
            filenames.append(new_name)
            if session['settings']['image_processing']:
                ImageProcessing.resize_image(new_name)
            if len(form.file.data) > 1:
                form.name.data = f'{entity_name}_{str(count + 1).zfill(2)}'
                if origin:
                    url = f"{url_for('view', id_=origin.id)}#tab-file"
            entity.update(process_form_data(form, entity, origin))
            logger.log_user(entity.id, 'insert')
        Transaction.commit()
        flash(_('entity created'), 'info')
    except Exception as e:  # pragma: no cover
        Transaction.rollback()
        for filename in filenames:
            (app.config['UPLOAD_DIR'] / filename).unlink()
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('index', view=g.classes['file'].view)
    return url


def save(
        form: FlaskForm,
        entity: Optional[Entity] = None,
        class_: Optional[str] = None,
        origin: Optional[Entity] = None) -> Union[str, Response]:
    Transaction.begin()
    action = 'update' if entity else 'insert'
    try:
        if not entity:
            entity = insert_entity(form, class_)
            if class_ == 'source_translation' and origin:
                origin.link('P73', entity)
        redirect_link_id = entity.update(
            data=process_form_data(form, entity, origin),
            new=(action == 'insert'))
        logger.log_user(entity.id, action)
        Transaction.commit()
        url = get_redirect_url(form, entity, class_, origin, redirect_link_id)
        flash(
            _('entity created') if action == 'insert' else _('info update'),
            'info')
    except InvalidGeomException as e:  # pragma: no cover
        Transaction.rollback()
        logger.log('error', 'database', 'invalid geom', e)
        flash(_('Invalid geom entered'), 'error')
        url = url_for('index', view=g.classes[class_].view)
        if action == 'update' and entity:
            url = url_for(
                'update',
                id_=entity.id,
                origin_id=origin.id if origin else None)
    except Exception as e:  # pragma: no cover
        Transaction.rollback()
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        if action == 'update' and entity:
            url = url_for(
                'update',
                id_=entity.id,
                origin_id=origin.id if origin else None)
        else:
            url = url_for('index', view=g.classes[class_].view)
            if class_ in ['administrative_unit', 'type']:
                url = url_for('type_index')
    return url


def insert_entity(form: FlaskForm, class_: str) \
        -> Union[Entity, Type, ReferenceSystem]:
    if class_ == 'reference_system':
        return ReferenceSystem.insert_system({
            'name': form.name.data,
            'description': form.description.data,
            'website_url': form.website_url.data,
            'resolver_url': form.resolver_url.data})
    entity = Entity.insert(class_, form.name.data)
    if class_ == 'artifact' or g.classes[class_].view == 'place':
        entity.link(
            'P53',
            Entity.insert('object_location', f'Location of {form.name.data}'))
    return entity


def get_redirect_url(
        form: FlaskForm,
        entity: Entity,
        class_: str,
        origin: Union[Entity, None] = None,
        redirect_link_id: Union[Entity, None] = None) -> str:
    if redirect_link_id:
        return url_for('link_update', id_=redirect_link_id, origin_id=origin.id)
    url = url_for('view', id_=entity.id)
    if origin and class_ not in \
            ('administrative_unit', 'source_translation', 'type'):
        url = f"{url_for('view', id_=origin.id)}#tab-{entity.class_.view}"
        if entity.class_.name == 'file':
            url = f"{url_for('view', id_=origin.id)}#tab-file"
        elif origin.class_.view in ['place', 'feature', 'stratigraphic_unit']:
            url = url_for('view', id_=entity.id)
    if hasattr(form, 'continue_') and form.continue_.data == 'yes':
        url = url_for(
            'insert',
            class_=class_,
            origin_id=origin.id if origin else None)
        if class_ in ('administrative_unit', 'type'):
            root_id = origin.root[0] \
                if isinstance(origin, Type) and origin.root else origin.id
            super_id = getattr(form, str(root_id)).data
            url = url_for(
                'insert',
                class_=class_,
                origin_id=str(super_id) if super_id else root_id)
    elif hasattr(form, 'continue_') \
            and form.continue_.data in ['sub', 'human_remains']:
        class_ = form.continue_.data
        if class_ == 'sub':
            if entity.class_.name == 'place':
                class_ = 'feature'
            elif entity.class_.name == 'feature':
                class_ = 'stratigraphic_unit'
            elif entity.class_.name == 'stratigraphic_unit':
                class_ = 'artifact'
        url = url_for('insert', class_=class_, origin_id=entity.id)
    return url
