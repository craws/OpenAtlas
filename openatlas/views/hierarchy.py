from flask import abort, flash, g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.table import Table
from openatlas.display.util import (
    get_entities_linked_to_type_recursive, link, required_group)
from openatlas.display.util2 import uc_first
from openatlas.forms.display import display_form
from openatlas.forms.entity_form import get_entity_form, process_form
from openatlas.models.entity import Entity


@app.route('/hierarchy/insert/<category>', methods=['GET', 'POST'])
@required_group('manager')
def hierarchy_insert(category: str) -> str | Response:
    hierarchy = Entity({'openatlas_class_name': 'type'})
    hierarchy.category = category
    form = get_entity_form(hierarchy)
    if form.validate_on_submit():
        if Entity.check_hierarchy_exists(form.name.data):
            form.name.errors.append(_('error name exists'))
        else:
            try:
                Transaction.begin()
                hierarchy = process_form(hierarchy, form)
                Entity.insert_hierarchy(
                    hierarchy,
                    category,
                    form.classes.data,
                    bool(
                        category == 'value' or (
                            hasattr(form, 'multiple')
                            and form.multiple.data)))
                g.logger.log_user(hierarchy.id, 'insert')
                Transaction.commit()
            except Exception as e:  # pragma: no cover
                Transaction.rollback()
                g.logger.log('error', 'database', 'transaction failed', e)
                flash(_('error transaction'), 'error')
                abort(418)
            flash(_('entity created'))
            return redirect(
                f"{url_for('index', group='type')}#menu-tab-{category}")
    return render_template(
        'content.html',
        content=display_form(form, manual_page='entity/type'),
        title=_('type'),
        crumbs=[
            [_('type'), url_for('index', group='type')],
            '+ ' + uc_first(_(category))])


@app.route('/hierarchy/update/<int:id_>', methods=['GET', 'POST'])
@required_group('manager')
def hierarchy_update(id_: int) -> str | Response:
    hierarchy = g.types[id_]
    if hierarchy.category in ('standard', 'system'):
        abort(403)
    form = get_entity_form(hierarchy)
    linked_entities = set()
    has_multiple_links = False
    for entity in get_entities_linked_to_type_recursive(id_, []):
        if entity.id in linked_entities:
            has_multiple_links = True
            break
        linked_entities.add(entity.id)
    if form.validate_on_submit():
        if form.name.data != hierarchy.name \
                and Entity.check_hierarchy_exists(form.name.data):
            form.name.errors.append(_('error name exists'))
        else:
            Transaction.begin()
            try:
                hierarchy.update_hierarchy(
                    form.name.data,
                    form.classes.data,
                    multiple=(
                        hierarchy.category == 'value'
                        or (hasattr(form, 'multiple') and form.multiple.data)
                        or has_multiple_links))
                process_form(hierarchy, form)
                g.logger.log_user(hierarchy.id, 'update')
                Transaction.commit()
            except Exception as e:  # pragma: no cover
                Transaction.rollback()
                g.logger.log('error', 'database', 'transaction failed', e)
                flash(_('error transaction'), 'error')
                abort(418)
            flash(_('info update'))
            tab = 'value' if g.types[id_].category == 'value' else 'custom'
            return redirect(
                f"{url_for('index', group='type')}"
                f"#menu-tab-{tab}_collapse-{hierarchy.id}")
    if hasattr(form, 'multiple') and has_multiple_links and hierarchy.multiple:
        form.multiple.render_kw = {'disabled': 'disabled'}
    table = Table(['class', 'count'], paging=False)
    for name in hierarchy.classes:
        count = hierarchy.get_count_by_class(name)
        table.rows.append([
            g.classes[name].label,
            format_number(count) if count else link(
                _('remove'),
                url_for('remove_class', id_=hierarchy.id, name=name))])
    return render_template(
        'content.html',
        content=f'''
            <div class="row">
              <div class="col-12 col-sm-6">
                {display_form(form, manual_page='entity/type')}
              </div>
              <div class="col-12 col-sm-6">{table.display()}</div>
            </div>''',
        title=_('type'),
        crumbs=[
            [_('type'), url_for('index', group='type')],
            hierarchy,
            _('edit')])


@app.route('/hierarchy/remove_class/<int:id_>/<name>')
@required_group('manager')
def remove_class(id_: int, name: str) -> Response:
    if g.types[id_].get_count_by_class(name):
        abort(403)
    try:
        g.types[id_].remove_class(name)
        flash(_('info update'))
    except Exception as e:  # pragma: no cover
        g.logger.log('error', 'database', 'remove hierarchy class failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('hierarchy_update', id_=id_))


@app.route('/hierarchy/delete/<int:id_>', methods=['GET', 'POST'])
@required_group('manager')
def hierarchy_delete(id_: int) -> Response:
    type_ = g.types[id_]
    if type_.category in ('standard', 'system', 'place'):
        abort(403)
    if type_.subs:
        return redirect(url_for('type_delete_recursive', id_=id_))
    type_.delete()
    flash(_('entity deleted'))
    return redirect(
        f"{url_for('index', group='type')}#menu-tab-{type_.category}")


@app.route('/hierarchy/required_risk/<int:id_>')
@required_group('manager')
def required_risk(id_: int) -> str:
    entity = Entity.get_by_id(id_)
    return render_template(
        'type/required.html',
        id_=id_,
        entity=entity,
        untyped_count=format_number(len(g.types[id_].get_untyped())),
        crumbs=[
            [_('type'), url_for('index', group='type')],
            entity,
            _('required')])


@app.route('/hierarchy/required_add/<int:id_>')
@required_group('manager')
def required_add(id_: int) -> Response:
    g.types[id_].set_required()
    g.logger.log('info', 'types', f'Setting hierarchy {id_} to required')
    flash(_('info update'))
    return redirect(url_for('view', id_=id_))


@app.route('/hierarchy/required_remove/<int:id_>')
@required_group('manager')
def required_remove(id_: int) -> Response:
    g.types[id_].unset_required()
    g.logger.log('info', 'types', f'Setting hierarchy {id_} to not required')
    flash(_('info update'))
    return redirect(url_for('view', id_=id_))
