from typing import Union

from flask import abort, flash, g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.database.connect import Transaction
from openatlas.forms.form import build_form
from openatlas.forms.util import process_form_data
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.util.table import Table
from openatlas.util.util import link, required_group, sanitize, uc_first


@app.route('/hierarchy/insert/<category>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_insert(category: str) -> Union[str, Response]:
    form = build_form('hierarchy', code=category)
    form.classes.choices = Type.get_class_choices()
    if form.validate_on_submit():
        if Type.check_hierarchy_exists(form.name.data):
            flash(_('error name exists'), 'error')
            return render_template('display_form.html', form=form)
        try:
            Transaction.begin()
            type_ = Entity.insert('type', sanitize(form.name.data))
            Type.insert_hierarchy(
                type_,  # type: ignore
                category,
                form.classes.data,
                is_multiple(form, category))
            type_.update(process_form_data(form, type_))
            Transaction.commit()
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
            abort(418)
        flash(_('entity created'), 'info')
        return redirect(f"{url_for('type_index')}#menu-tab-{category}")
    return render_template(
        'display_form.html',
        form=form,
        manual_page='entity/type',
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
    form = build_form('hierarchy', hierarchy)
    form.classes.choices = Type.get_class_choices(hierarchy)
    if hasattr(form, 'multiple') and form.multiple.data:
        form.multiple.render_kw = {'disabled': 'disabled'}
    if form.validate_on_submit():
        if form.name.data != hierarchy.name and Type.get_types(form.name.data):
            flash(_('error name exists'), 'error')
        else:
            Transaction.begin()
            try:
                Type.update_hierarchy(
                    hierarchy,
                    sanitize(form.name.data),
                    form.classes.data,
                    is_multiple(form, hierarchy.category))
                hierarchy.update(process_form_data(form, hierarchy))
                Transaction.commit()
            except Exception as e:  # pragma: no cover
                Transaction.rollback()
                logger.log('error', 'database', 'transaction failed', e)
                flash(_('error transaction'), 'error')
                abort(418)
            flash(_('info update'), 'info')
        tab = 'value' if g.types[id_].category == 'value' else 'custom'
        return redirect(
            f"{url_for('type_index')}#menu-tab-{tab}_collapse-{hierarchy.id}")
    form.multiple = hierarchy.multiple
    table = Table(paging=False)
    for class_name in hierarchy.classes:
        count = Type.get_form_count(hierarchy, class_name)
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
        crumbs=[[_('types'), url_for('type_index')], hierarchy, _('edit')])


@app.route('/hierarchy/remove_class/<int:id_>/<class_name>')
@required_group('manager')
def remove_class(id_: int, class_name: str) -> Response:
    root = g.types[id_]
    if Type.get_form_count(root, class_name):
        abort(403)  # pragma: no cover
    try:
        Type.remove_class_from_hierarchy(class_name, root.id)
        flash(_('info update'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'database', 'remove class from hierarchy failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('hierarchy_update', id_=id_))


@app.route('/hierarchy/delete/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_delete(id_: int) -> Response:
    type_ = g.types[id_]
    if type_.category in ('standard', 'system') or type_.subs or type_.count:
        abort(403)
    type_.delete()
    flash(_('entity deleted'), 'info')
    return redirect(url_for('type_index'))


def is_multiple(form: FlaskForm, category: str) -> bool:
    if category == 'value' or (
            hasattr(form, 'multiple') and form.multiple and form.multiple.data):
        return True
    return False  # pragma: no cover
