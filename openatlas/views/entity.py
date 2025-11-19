import os
from datetime import datetime
from typing import Any, Optional

from flask import flash, g, render_template, request, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.display import Display
from openatlas.display.table import entity_table
from openatlas.display.util import (
    button, check_iiif_file_exist, get_chart_data, get_file_path,
    get_iiif_file_path, hierarchy_crumbs, link, reference_systems,
    required_group)
from openatlas.display.util2 import is_authorized, manual, sanitize
from openatlas.forms.entity_form import (
    get_entity_form, process_files, process_form_data)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis, InvalidGeomException
from openatlas.models.openatlas_class import Relation
from openatlas.models.overlay import Overlay


@app.route('/entity/<int:id_>')
@required_group('readonly')
def view(id_: int) -> str | Response:
    entity = Entity.get_by_id(id_, types=True, aliases=True)
    if not entity.class_.group:
        flash(_("This entity can't be viewed directly."), 'error')
        abort(400)
    match entity.class_.group.get('name'):
        case 'type' if not entity.root:
            return redirect(
                f"{url_for('index', group='type')}"
                f"#menu-tab-{entity.category}_collapse-{id_}")
        case 'reference_system':
            entity.class_.relations = {}
            for name in entity.classes:
                entity.class_.relations[name] = Relation(name, {
                    'name': name,
                    'label': _(name.replace('_', ' ')),
                    'classes': [name],
                    'property': 'P67',
                    'multiple': True,
                    'tab': {
                        'buttons': ['remove_reference_system_class'],
                        'columns': [
                            'name',
                            'external_reference_match',
                            'precision']}})
    display = Display(entity)
    return render_template(
        'tabs.html',
        tabs=display.tabs,
        entity=entity,
        gis_data=display.gis_data,
        crumbs=hierarchy_crumbs(entity) + [entity.name])


@app.route('/reference_system/remove_class/<int:system_id>/<name>')
@required_group('manager')
def reference_system_remove_class(system_id: int, name: str) -> Response:
    system = g.reference_systems[system_id]
    if system.get_links('P67', [name]):
        abort(403)  # Abort because there are linked entities
    try:
        system.remove_reference_system_class(name)
        flash(_('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.logger.log('error', 'database', 'remove class failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('view', id_=system_id))


@app.route('/insert/<class_>', methods=['GET', 'POST'])
@app.route(
    '/insert/<class_>/<int:origin_id>/<relation>',
    methods=['GET', 'POST'])
@required_group('contributor')
def insert(
        class_: str,
        origin_id: Optional[int] = None,
        relation: Optional[str] = None) -> str | Response:
    check_insert_access(class_)
    entity = Entity({'openatlas_class_name': class_})
    origin = Entity.get_by_id(origin_id) if origin_id else None
    form = get_entity_form(entity, origin, relation)
    if form.validate_on_submit():
        return redirect(save(entity, form, origin, relation))
    structure = None
    gis_data = None
    if entity.class_.attributes.get('location'):
        structure = origin.get_structure_for_insert() if origin else None
        gis_data = Gis.get_all(structure=structure)
    return render_template(
        'entity/insert.html',
        form=form,
        class_=entity.class_,
        gis_data=gis_data,
        writable=os.access(app.config['UPLOAD_PATH'], os.W_OK),
        overlays=get_overlays(origin) if origin else None,
        title=_(entity.class_.group['name']),
        crumbs=crumbs_for_insert(entity, origin, structure))


def crumbs_for_insert(
        entity: Entity,
        origin: Entity | None,
        structure: dict[str, Any] | None) -> list[Any]:
    crumbs = hierarchy_crumbs(origin or entity) + \
        [origin, f'+ {entity.class_.label}']
    if entity.class_.group['name'] == 'artifact' and origin and structure:
        if count := len([
            i for i in structure['siblings']
                if i.class_.name == entity.class_.name]):
            crumbs.append(f' ({count} {_("exists")})')
    return crumbs


def get_overlays(entity: Entity) -> dict[int, Overlay]:
    if entity.class_.group['name'] == 'place' \
            and current_user.settings['module_map_overlay']:
        return Overlay.get_by_object(entity)
    return {}


@app.route('/update/<int:id_>', methods=['GET', 'POST'])
@app.route('/update/<int:id_>/<copy>', methods=['GET', 'POST'])
@required_group('contributor')
def update(id_: int, copy: Optional[str] = None) -> str | Response:
    entity = Entity.get_by_id(id_, types=True, aliases=True)
    check_update_access(entity)
    form = get_entity_form(entity)
    if form.validate_on_submit():
        if copy:
            entity.id = 0
        elif template := was_modified_template(entity, form):
            return template
        return redirect(save(entity, form))
    gis_data = None
    entity.image_id = entity.get_profile_image_id()
    if entity.class_.attributes.get('location'):
        entity.location = entity.location \
            or entity.get_linked_entity_safe('P53')
        gis_data = Gis.get_all([entity], entity.get_structure())
    return render_template(
        'entity/update.html',
        form=form,
        entity=entity,
        gis_data=gis_data,
        overlays=get_overlays(entity),
        title=entity.name,
        crumbs=hierarchy_crumbs(entity) +
        [entity, _('copy') if copy else _('edit')])


def deletion_possible(entity: Entity) -> bool:
    if not is_authorized(entity.class_.write_access):
        return False
    if current_user.group == 'contributor':
        info = g.logger.get_log_info(entity.id)
        if not info['creator'] or info['creator'].id != current_user.id:
            return False
    if entity.class_.group['name'] == 'type':
        return True  # Type (recursive) deletion is taken care of at delete()
    for relation in entity.class_.relations.values():
        if relation.reverse_relation \
                and relation.reverse_relation.required \
                and entity.get_linked_entities(
                    relation.property,
                    relation.classes,
                    relation.inverse):
            return False
    match entity.class_.group['name']:
        case 'reference_system' if entity.system or entity.classes:
            return False
        case 'type' if entity.system:
            return False
    return True


@app.route('/delete/<int:id_>')
@required_group('contributor')
def delete(id_: int) -> Response:
    entity = Entity.get_by_id(id_)
    if not deletion_possible(entity):
        abort(403)
    url = url_for('index', group=entity.class_.group['name'])
    if entity.class_.group['name'] == 'type':
        if entity.subs or entity.count:
            return redirect(url_for('type_delete_recursive', id_=entity.id))
        root = g.types[entity.root[0]] if entity.root else None
        url = url_for('view', id_=root.id) if root \
            else url_for('index', group='type')
    elif entity.class_.group['name'] in ['artifact', 'place']:
        if entity.get_linked_entities('P46'):
            flash(_('Deletion not possible if subunits exists'), 'error')
            return redirect(url_for('view', id_=id_))
        if entity.class_.name != 'place' \
                and (parent := entity.get_linked_entity(
                    'P46',
                    g.class_groups['place']['classes'] +
                    g.class_groups['artifact']['classes'],
                    True)):
            url = \
                f"{url_for('view', id_=parent.id)}" \
                f"#tab-{entity.class_.name.replace('_', '-')}"
    elif entity.class_.name == 'source_translation':
        source = entity.get_linked_entity_safe('P73', inverse=True)
        url = f"{url_for('view', id_=source.id)}#tab-text"
    elif entity.class_.name == 'file':
        try:
            delete_files(id_)
        except Exception as e:  # pragma: no cover
            g.logger.log('error', 'file', 'file deletion failed', e)
            flash(_('error file delete'), 'error')
            return redirect(url_for('view', id_=id_))
    entity.delete()
    g.logger.log_user(id_, 'delete')
    flash(_('entity deleted'), 'info')
    return redirect(url)


def check_insert_access(class_: str) -> None:
    if class_ not in g.classes \
            or not g.classes[class_].group \
            or not is_authorized(g.classes[class_].write_access):
        abort(403)


def check_update_access(entity: Entity) -> None:
    check_insert_access(entity.class_.name)
    if entity.class_.group['name'] == 'type' and (
            entity.category == 'system'
            or entity.category == 'standard' and not entity.root):
        abort(403)
    if entity.check_too_many_single_type_links():
        abort(422)


def save(
        entity: Entity,
        form: Any,
        origin: Optional[Entity] = None,
        relation: Optional[str] = None) -> str:
    action = 'update' if entity.id else 'insert'
    url = url_for('index', group=entity.class_.group['name'])
    try:
        if hasattr(form, 'file'):
            entity = process_files(form, origin, relation)
        else:
            entity = process_form_data(entity, form, origin, relation)
        g.logger.log_user(entity.id, action)
        url = redirect_url_insert(entity, form, origin, relation)
        flash(
            _('entity created') if action == 'insert' else _('info update'),
            'info')
    except InvalidGeomException:
        flash(_('Invalid geom entered'), 'error')
        if action == 'update' and entity.id:
            url = url_for(
                'update',
                id_=entity.id,
                origin_id=origin.id if origin else None)
    except Exception:
        flash(_('error transaction'), 'error')
        if action == 'update' and entity.id:
            url = url_for(
                'update',
                id_=entity.id,
                origin_id=origin.id if origin else None)  # pragma: no cover
    return url


def redirect_url_insert(
        entity: Entity,
        form: Any,
        origin: Entity | None,
        relation_name: str | None) -> str:
    url = url_for('view', id_=entity.id)
    if hasattr(form, 'continue_') and form.continue_.data == 'yes':
        url = request.url
        if entity.class_.group['name'] == 'type' and origin:
            if not (super_id := getattr(form, 'super').data):
                super_id = origin.root[0] if origin.root else origin.id
            url = url_for(
                'insert',
                class_=entity.class_.name,
                origin_id=str(super_id),
                relation=relation_name)
    if entity.class_.group['name'] != 'type' and origin and relation_name:
        relation = origin.class_.relations[relation_name]
        if relation.additional_fields:
            url = url_for(
                'link_insert_detail',
                origin_id=origin.id,
                name=relation_name,
                selection_id=entity.id)
        elif not hasattr(form, 'continue_') or form.continue_.data != 'yes':
            url = url_for(
                'view',
                id_=origin.id) + f"#tab-{relation_name.replace('_', '-')}"
    if hasattr(form, 'continue_') \
            and form.continue_.data in ['sub', 'human_remains']:
        class_ = form.continue_.data
        if class_ == 'sub':
            match entity.class_.name:
                case 'place':
                    class_ = 'feature'
                case 'feature':
                    class_ = 'stratigraphic_unit'
                case 'stratigraphic_unit':
                    class_ = 'artifact'
        url = url_for(
            'insert',
            class_=class_,
            origin_id=entity.id,
            relation=class_.replace('human_remains', 'artifact'))
    return url


def delete_files(id_: int) -> None:
    if path := get_file_path(id_):  # Prevent missing file warning
        path.unlink()
    for resized_path in app.config['RESIZED_IMAGES'].glob(f'**/{id_}.*'):
        resized_path.unlink()
    if g.settings['iiif'] and check_iiif_file_exist(id_):
        if path := get_iiif_file_path(id_):
            path.unlink()


def was_modified_template(entity: Entity, form: Any) -> str | None:
    if not entity.modified \
            or not form.opened.data \
            or entity.modified < \
            datetime.fromtimestamp(float(form.opened.data)):
        return None
    del form.save
    g.logger.log('info', 'multi user', 'Overwrite denied')
    flash(
        _('error modified by %(username)s', username=link(
            g.logger.get_log_info(entity.id)['modifier'],
            external=True)) +
        button(_('reload'), url_for('update', id_=entity.id)),
        'error')
    return render_template('entity/update.html', form=form, entity=entity)


@app.route('/index/<group>')
@required_group('readonly')
def index(group: str) -> str | Response:
    if group == 'type':
        types: dict[str, dict[Entity, str]] = {
            'standard': {},
            'custom': {},
            'place': {},
            'value': {},
            'system': {}}
        for type_ in [type_ for type_ in g.types.values() if not type_.root]:
            if type_.category in types:
                type_.chart_data = get_chart_data(type_)
                types[type_.category][type_] = render_template(
                    'forms/tree_select_item.html',
                    name=sanitize(type_.name, 'ascii'),
                    data=walk_tree(type_.subs))
                type_.reference_systems_display = reference_systems(type_)
        return render_template(
            'type/index.html',
            buttons=[manual('entity/type')],
            types=types,
            title=_('type'),
            crumbs=[_('type')])

    classes = ['place'] if group == 'place' else \
        g.class_groups[group].get('classes', [group])
    if group == 'reference_system':
        entities = list(g.reference_systems.values())
        counts = Entity.reference_system_counts()
        for entity in entities:
            entity.count = counts[entity.id]
    else:
        entities = Entity.get_by_class(classes, types=True, aliases=True)
    buttons = [manual(f'entity/{group}')]
    for class_ in classes:
        if is_authorized(g.classes[class_].write_access):
            buttons.append(
                button(
                    g.classes[class_].label,
                    url_for('insert', class_=class_),
                    tooltip_text=g.classes[class_].display['tooltip']))
    return render_template(
        'entity/index.html',
        class_=group,
        table=entity_table(entities),
        buttons=buttons,
        gis_data=Gis.get_all() if group == 'place' else None,
        title=_(group.replace('_', ' ')),
        crumbs=[_(group).replace('_', ' ')])


def walk_tree(types: list[int]) -> list[dict[str, Any]]:
    items = []
    for id_ in types:
        item = g.types[id_]
        count_subs = f' ({format_number(item.count_subs)})' \
            if item.count_subs else ''
        name = item.name.replace("'", "&apos;")
        if item.selectable:
            text = f'{name} {format_number(item.count)}{count_subs}'
        else:
            text = f'<span class="text-muted">{name}{count_subs}</span>'
        items.append({
            'id': item.id,
            'href': url_for('view', id_=item.id),
            'a_attr': {'href': url_for('view', id_=item.id)},
            'text': text,
            'children': walk_tree(item.subs)})
    return items
