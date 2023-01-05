from typing import Union

from flask import abort, flash, g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.table import Table
from openatlas.forms.form import get_manager
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.util.util import (
    display_form, get_entities_linked_to_type_recursive, link, required_group,
    sanitize, uc_first)


@app.route('/hierarchy/insert/<category>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_insert(category: str) -> Union[str, Response]:
    manager = get_manager(f'hierarchy_{category}')
    if manager.form.validate_on_submit():
        try:
            Transaction.begin()
            manager.insert_entity()
            Type.insert_hierarchy(
                manager.entity,
                category,
                manager.form.classes.data,
                bool(
                    category == 'value' or
                    (hasattr(manager.form, 'multiple')
                     and manager.form.multiple.data)))
            manager.process_form()
            manager.entity.update(manager.data, new=True)
            Transaction.commit()
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
            abort(418)
        flash(_('entity created'), 'info')
        return redirect(f"{url_for('type_index')}#menu-tab-{category}")
    return render_template(
        'content.html',
        content=display_form(manager.form, manual_page='entity/type'),
        title=_('types'),
        crumbs=[
            [_('types'), url_for('type_index')],
            f'+ {uc_first(_(category))}'])


@app.route('/hierarchy/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_update(id_: int) -> Union[str, Response]:
    hierarchy = g.types[id_]
    if hierarchy.category in ('standard', 'system'):
        abort(403)
    manager = get_manager(f'hierarchy_{hierarchy.category}', entity=hierarchy)
    linked_entities = set()
    has_multiple_links = False
    for entity in get_entities_linked_to_type_recursive(id_, []):
        if entity.id in linked_entities:
            has_multiple_links = True
            break
        linked_entities.add(entity.id)
    if manager.form.validate_on_submit():
        Transaction.begin()
        try:
            hierarchy.update_hierarchy(
                sanitize(manager.form.name.data, 'text'),
                manager.form.classes.data,
                multiple=(
                    hierarchy.category == 'value'
                    or (hasattr(manager.form, 'multiple')
                        and manager.form.multiple.data)
                    or has_multiple_links))
            manager.process_form()
            manager.entity.update(manager.data)
            Transaction.commit()
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
            abort(418)
        flash(_('info update'), 'info')
        tab = 'value' if g.types[id_].category == 'value' else 'custom'
        return redirect(
            f"{url_for('type_index')}#menu-tab-{tab}_collapse-{hierarchy.id}")
    if not manager.form.errors:
        manager.populate_update()
    if hasattr(manager.form, 'multiple') and has_multiple_links:
        manager.form.multiple.render_kw = {'disabled': 'disabled'}
    table = Table(paging=False)
    for name in hierarchy.classes:
        count = hierarchy.get_count_by_class(name)
        table.rows.append([
            g.classes[name].label,
            format_number(count) if count else link(
                _('remove'),
                url_for('remove_class', id_=hierarchy.id, name=name))])
    return render_template(
        'content.html',
        content=display_form(manager.form, manual_page='entity/type')
        + table.display(),
        title=_('types'),
        crumbs=[[_('types'), url_for('type_index')], hierarchy, _('edit')])


@app.route('/hierarchy/remove_class/<int:id_>/<name>')
@required_group('manager')
def remove_class(id_: int, name: str) -> Response:
    if g.types[id_].get_count_by_class(name):
        abort(403)
    try:
        g.types[id_].remove_class(name)
        flash(_('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.logger.log('error', 'database', 'remove hierarchy class failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('hierarchy_update', id_=id_))


@app.route('/hierarchy/delete/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_delete(id_: int) -> Response:
    type_ = g.types[id_]
    if type_.category in ('standard', 'system', 'place'):
        abort(403)
    if type_.subs:
        return redirect(url_for('type_delete_recursive', id_=id_))
    type_.delete()
    flash(_('entity deleted'), 'info')
    return redirect(url_for('type_index'))


@app.route('/hierarchy/required_risk/<int:id_>')
@required_group('manager')
def required_risk(id_: int) -> str:
    entity = Entity.get_by_id(id_)
    return render_template(
        'type/required.html',
        id_=id_,
        entity=entity,
        untyped_count=format_number(len(g.types[id_].get_untyped())),
        crumbs=[[_('types'), url_for('type_index')], entity, _('required')])


@app.route('/hierarchy/required_add/<int:id_>')
@required_group('manager')
def required_add(id_: int) -> Response:
    g.types[id_].set_required()
    g.logger.log('info', 'types', f'Setting hierarchy {id_} to required')
    flash(_('info update'), 'info')
    return redirect(url_for('view', id_=id_))


@app.route('/hierarchy/required_remove/<int:id_>')
@required_group('manager')
def required_remove(id_: int) -> Response:
    g.types[id_].unset_required()
    g.logger.log('info', 'types', f'Setting hierarchy {id_} to not required')
    flash(_('info update'), 'info')
    return redirect(url_for('view', id_=id_))
