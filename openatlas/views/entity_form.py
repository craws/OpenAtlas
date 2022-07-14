import os
from typing import Any, Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.database.connect import Transaction
from openatlas.forms import base_manager
from openatlas.forms.form import get_entity_form
from openatlas.forms.util import populate_insert_form, process_form_data
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis, InvalidGeomException
from openatlas.models.overlay import Overlay
from openatlas.models.place import get_structure
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.util.image_processing import resize_image
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
    manager = get_entity_form(class_, origin=origin)
    if manager.form.validate_on_submit():
        if class_ == 'file':
            return redirect(insert_files(manager.form, origin))
        return redirect(save(manager))
    populate_insert_form(manager.form, class_, origin)
    place_info = get_place_info_for_insert(g.classes[class_].view, origin)
    return render_template(
        'entity/insert.html',
        form=manager.form,
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
    if entity.check_too_many_single_type_links():
        abort(422)
    place_info = get_place_info_for_update(entity)
    manager = get_entity_form(entity=entity)
    if manager.form.validate_on_submit():
        if isinstance(entity, Type) and not check_type(entity, manager.form):
            return redirect(url_for('view', id_=entity.id))
        if was_modified(manager.form, entity):  # pragma: no cover
            del manager.form.save
            flash(_('error modified'), 'error')
            return render_template(
                'entity/update.html',
                form=manager.form,
                entity=entity,
                modifier=link(logger.get_log_info(entity.id)['modifier']))
        return redirect(save(manager))
    manager.populate_update()
    if entity.class_.view in ['artifact', 'place']:
        entity.set_image_for_places()
    return render_template(
        'entity/update.html',
        form=manager.form,
        entity=entity,
        gis_data=place_info['gis_data'],
        overlays=place_info['overlays'],
        geonames_module=check_geonames_module(entity.class_.name),
        title=entity.name,
        crumbs=add_crumbs(entity.class_.name, entity, place_info['structure']))


def add_crumbs(
        class_: str,
        origin: Union[Entity, None],
        structure: Optional[dict[str, Any]],
        insert_: Optional[bool] = False) -> list[Any]:
    view = g.classes[class_].view
    label = origin.class_.name if origin else view
    if label in g.class_view_mapping:
        label = g.class_view_mapping[label]
    label = _(label.replace('_', ' '))
    crumbs: list[Any] = [
        [label, url_for('index', view=origin.class_.view if origin else view)],
        origin]
    if class_ == 'source_translation' and origin and not insert_:
        crumbs = [
            [_('source'), url_for('index', view='source')],
            origin.get_linked_entity('P73', True),
            origin]
    if structure:
        crumbs = [
            [_('place'), url_for('index', view='place')],
            structure['place']
            if origin and origin.class_.name != 'place' else '',
            structure['feature'],
            structure['stratigraphic_unit'],
            origin]
    if view == 'type':
        crumbs = [[_('types'), url_for('type_index')]]
        if isinstance(origin, Type) and origin.root:
            crumbs += [g.types[type_id] for type_id in origin.root]
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
    return class_ == 'place' \
           and bool(ReferenceSystem.get_by_name('GeoNames').classes)


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
        origin: Optional[Entity]) -> dict[str, Any]:
    if class_view not in ['artifact', 'place']:
        return {'structure': None, 'gis_data': None, 'overlays': None}
    structure = get_structure(super_=origin)
    return {
        'structure': structure,
        'gis_data': Gis.get_all([origin] if origin else None, structure),
        'overlays': Overlay.get_by_object(origin)
        if origin and origin.class_.view == 'place' else None}


def get_place_info_for_update(entity: Entity) -> dict[str, Any]:
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
    # Todo: adapt new forms
    filenames = []
    url = url_for('index', view=g.classes['file'].view)
    try:
        Transaction.begin()
        entity_name = form.name.data.strip()
        for count, file in enumerate(form.file.data):
            entity = Entity.insert('file', file.filename)
            url = get_redirect_url(form)
            # Add 'a' to prevent emtpy temporary filename, has no side effects
            filename = secure_filename(f'a{file.filename}')
            new_name = f"{entity.id}.{filename.rsplit('.', 1)[1].lower()}"
            file.save(str(app.config['UPLOAD_DIR'] / new_name))
            filenames.append(new_name)
            if g.settings['image_processing']:
                resize_image(new_name)
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


def save(form_manager: Any) -> Union[str, Response]:
    Transaction.begin()
    action = 'update' if form_manager.entity else 'insert'
    try:
        if not form_manager.entity:
            form_manager.entity = insert_entity(form_manager)
        form_manager.process_form_data()
        form_manager.entity.update(form_manager.data, new=(action == 'insert'))
        logger.log_user(form_manager.entity.id, action)
        Transaction.commit()
        url = get_redirect_url(form_manager)
        flash(
            _('entity created') if action == 'insert' else _('info update'),
            'info')
    except InvalidGeomException as e:  # pragma: no cover
        Transaction.rollback()
        logger.log('error', 'database', 'invalid geom', e)
        flash(_('Invalid geom entered'), 'error')
        url = url_for('index', view=g.classes[form_manager.class_.name].view)
        if action == 'update' and form_manager.entity:
            url = url_for(
                'update',
                id_=form_manager.entity.id,
                origin_id=form_manager.origin.id
                if form_manager.origin else None)
    except Exception as e:  # pragma: no cover
        Transaction.rollback()
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        if action == 'update' and form_manager.entity:
            url = url_for(
                'update',
                id_=form_manager.entity.id,
                origin_id=form_manager.origin.id
                if form_manager.origin else None)
        else:
            url = url_for(
                'index',
                view=g.classes[form_manager.class_.name].view)
            if form_manager.class_.name in ['administrative_unit', 'type']:
                url = url_for('type_index')
    return url


def insert_entity(form_manager: Any) -> Union[Entity, ReferenceSystem, Type]:
    if form_manager.class_.name == 'reference_system':
        return ReferenceSystem.insert_system({
            'name': form_manager.form.name.data,
            'description': form_manager.form.description.data,
            'website_url': form_manager.form.website_url.data,
            'resolver_url': form_manager.form.resolver_url.data})
    entity = Entity.insert(
        form_manager.class_.name,
        form_manager.form.name.data)
    if form_manager.class_.name == 'artifact' \
            or g.classes[form_manager.class_.name].view == 'place':
        entity.link(
            'P53',
            Entity.insert(
                'object_location',
                f'Location of {form_manager.form.name.data}'))
    return entity


def get_redirect_url(manager: base_manager.BaseManager) -> str:
    # if redirect_link_id and origin:
    #    return url_for(
    #        'link_update',
    #        id_=redirect_link_id,
    #        origin_id=origin.id)
    url = url_for('view', id_=manager.entity.id)
    if manager.origin and manager.entity.class_.name not in \
            ('administrative_unit', 'source_translation', 'type'):
        url = \
            f"{url_for('view', id_=manager.origin.id)}" \
            f"#tab-{manager.entity.class_.view}"
        if manager.entity.class_.name == 'file':
            url = f"{url_for('view', id_=manager.origin.id)}#tab-file"
        elif manager.origin.class_.view \
                in ['place', 'feature', 'stratigraphic_unit'] \
                and manager.entity.class_.view != 'actor':
            url = url_for('view', id_=manager.entity.id)
    if hasattr(manager.form, 'continue_') \
            and manager.form.continue_.data == 'yes':
        url = url_for(
            'insert',
            class_=manager.entity.class_.name,
            origin_id=manager.origin.id if manager.origin else None)
        if manager.entity.class_.name in ('administrative_unit', 'type') \
                and manager.origin:
            root_id = manager.origin.root[0] \
                if isinstance(manager.origin, Type) and manager.origin.root \
                else manager.origin.id
            super_id = getattr(manager.form, str(root_id)).data
            url = url_for(
                'insert',
                class_=manager.entity.class_.name,
                origin_id=str(super_id) if super_id else root_id)
    elif hasattr(manager.form, 'continue_') \
            and manager.form.continue_.data in ['sub', 'human_remains']:
        class_ = manager.form.continue_.data
        if class_ == 'sub':
            if manager.entity.class_.name == 'place':
                class_ = 'feature'
            elif manager.entity.class_.name == 'feature':
                class_ = 'stratigraphic_unit'
            elif manager.entity.class_.name == 'stratigraphic_unit':
                class_ = 'artifact'
        url = url_for('insert', class_=class_, origin_id=manager.entity.id)
    return url
