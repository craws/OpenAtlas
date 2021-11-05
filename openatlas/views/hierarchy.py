from typing import Optional, Union

from flask import abort, flash, g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.database.connect import Transaction
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.models.node import Node
from openatlas.util.table import Table
from openatlas.util.util import link, required_group, sanitize, uc_first


@app.route('/hierarchy/insert/<param>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_insert(param: str) -> Union[str, Response]:
    form = build_form('hierarchy', code=param)
    form.classes.choices = Node.get_class_choices()
    if form.validate_on_submit():
        if Node.check_hierarchy_exists(form.name.data):
            flash(_('error name exists'), 'error')
            return render_template('display_form.html', form=form)
        save(form, param=param)
        flash(_('entity created'), 'info')
        return redirect(f"{url_for('node_index')}#menu-tab-{param}")
    return render_template(
        'display_form.html',
        form=form,
        manual_page='entity/type',
        title=_('types'),
        crumbs=[[_('types'), url_for('node_index')], f'+ {uc_first(_(param))}'])


@app.route('/hierarchy/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_update(id_: int) -> Union[str, Response]:
    hierarchy = g.nodes[id_]
    if hierarchy.category in ('standard', 'system'):
        abort(403)
    form = build_form('hierarchy', hierarchy)
    form.classes.choices = Node.get_class_choices(hierarchy)
    if hasattr(form, 'multiple') and form.multiple.data:
        form.multiple.render_kw = {'disabled': 'disabled'}
    if form.validate_on_submit():
        if form.name.data != hierarchy.name and Node.get_nodes(form.name.data):
            flash(_('error name exists'), 'error')
        else:
            save(form, hierarchy)
            flash(_('info update'), 'info')
        tab = 'value' if g.nodes[id_].category == 'value' else 'custom'
        return redirect(
            f"{url_for('node_index')}#menu-tab-{tab}_collapse-{hierarchy.id}")
    form.multiple = hierarchy.multiple
    table = Table(paging=False)
    for class_name in hierarchy.classes:
        count = Node.get_form_count(hierarchy, class_name)
        table.rows.append([
            g.classes[class_name].label,
            format_number(count) if count else link(
                _('remove'),
                url_for(
                    'remove_class',
                    id_=hierarchy.id,
                    class_name=class_name))])
    return render_template(
        'display_form.html',
        form=form,
        table=table,
        manual_page='entity/type',
        title=_('types'),
        crumbs=[[_('types'), url_for('node_index')], hierarchy, _('edit')])


@app.route('/hierarchy/remove_class/<int:id_>/<class_name>')
@required_group('manager')
def remove_class(id_: int, class_name: str) -> Response:
    root = g.nodes[id_]
    if Node.get_form_count(root, class_name):
        abort(403)  # pragma: no cover
    try:
        Node.remove_class_from_hierarchy(class_name, root.id)
        flash(_('info update'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'database', 'remove class from hierarchy failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('hierarchy_update', id_=id_))


@app.route('/hierarchy/delete/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_delete(id_: int) -> Response:
    node = g.nodes[id_]
    if node.category in ('standard', 'system') or node.subs or node.count:
        abort(403)
    node.delete()
    flash(_('entity deleted'), 'info')
    return redirect(url_for('node_index'))


def save(
        form: FlaskForm,
        node: Optional[Node] = None,
        param: Optional[str] = None) -> Optional[Node]:
    Transaction.begin()
    try:
        if node:
            Node.update_hierarchy(node, form)
        else:
            node = Entity.insert('type', sanitize(form.name.data))
            Node.insert_hierarchy(node, form, param)
        node.update(form)
        Transaction.commit()
    except Exception as e:  # pragma: no cover
        Transaction.rollback()
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        abort(418)
    return node
