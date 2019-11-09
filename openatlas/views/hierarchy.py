# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Optional, Union

from flask import abort, flash, g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import (BooleanField, SelectMultipleField, StringField, SubmitField, TextAreaField,
                     widgets)
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import build_form
from openatlas.models.node import NodeMapper
from openatlas.util.table import Table
from openatlas.util.util import required_group, sanitize, uc_first


class HierarchyForm(FlaskForm):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    multiple = BooleanField(_('multiple'), description=_('tooltip hierarchy multiple'))
    forms = SelectMultipleField(_('forms'),
                                render_kw={'disabled': True},
                                description=_('tooltip hierarchy forms'),
                                choices=[],
                                option_widget=widgets.CheckboxInput(),
                                widget=widgets.ListWidget(prefix_label=False),
                                coerce=int)
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))


@app.route('/hierarchy/insert/<param>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_insert(param: str) -> Union[str, Response]:
    form = build_form(HierarchyForm, 'hierarchy')
    form.forms.choices = NodeMapper.get_form_choices()
    if param == 'value':
        del form.multiple
    if form.validate_on_submit():
        if NodeMapper.get_nodes(form.name.data):
            flash(_('error name exists'), 'error')
            return render_template('hierarchy/insert.html', form=form)
        node = save(form, value_type=True if param == 'value' else False)
        flash(_('entity created'), 'info')
        return redirect(url_for('node_index') + '#tab-' + str(node.id))
    return render_template('hierarchy/insert.html', form=form, param=param)


@app.route('/hierarchy/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_update(id_: int) -> Union[str, Response]:
    root = g.nodes[id_]
    if root.system:
        abort(403)
    form = build_form(HierarchyForm, 'hierarchy', root)
    form.forms.choices = NodeMapper.get_form_choices(root)
    if root.value_type:
        del form.multiple
    elif root.multiple:
        form.multiple.render_kw = {'disabled': 'disabled'}
    if form.validate_on_submit():
        if form.name.data != root.name and NodeMapper.get_nodes(form.name.data):
            flash(_('error name exists'), 'error')
            return redirect(url_for('node_index') + '#tab-' + str(root.id))
        save(form, root)
        flash(_('info update'), 'info')
        return redirect(url_for('node_index') + '#tab-' + str(root.id))
    form.multiple = root.multiple
    table = Table(['form', 'count'], paging=False)
    for form_id, form_ in root.forms.items():
        url = url_for('hierarchy_remove_form', id_=root.id, remove_id=form_id)
        link = '<a href="' + url + '">' + uc_first(_('remove')) + '</a>'
        count = NodeMapper.get_form_count(root, form_id)
        table.rows.append([form_['name'], format_number(count) if count else link])
    return render_template('hierarchy/update.html', node=root, form=form, table=table,
                           forms=[form.id for form in form.forms])


@app.route('/hierarchy/remove_form/<int:id_>/<int:remove_id>')
@required_group('manager')
def hierarchy_remove_form(id_: int, remove_id: int) -> Response:
    root = g.nodes[id_]
    if NodeMapper.get_form_count(root, remove_id):
        abort(403)  # pragma: no cover
    try:
        NodeMapper.remove_form_from_hierarchy(root, remove_id)
        flash(_('info update'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'database', 'remove form from hierarchy failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('hierarchy_update', id_=id_))


@app.route('/hierarchy/delete/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_delete(id_: int) -> Response:
    node = g.nodes[id_]
    if node.system or node.subs or node.count:
        abort(403)
    node.delete()
    flash(_('entity deleted'), 'info')
    return redirect(url_for('node_index'))


def save(form, node=None, value_type=None):
    g.cursor.execute('BEGIN')
    try:
        if not node:
            node = NodeMapper.insert('E55', sanitize(form.name.data, 'node'))
            NodeMapper.insert_hierarchy(node, form, value_type)
        else:
            node = g.nodes[node.id]
            NodeMapper.update_hierarchy(node, form)
        node.name = sanitize(form.name.data, 'node')
        node.description = form.description.data
        node.update()
        g.cursor.execute('COMMIT')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    return node
