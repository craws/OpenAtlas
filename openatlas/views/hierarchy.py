# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, flash, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectMultipleField
from wtforms import widgets
from wtforms.validators import InputRequired

import openatlas
from openatlas import app, NodeMapper, EntityMapper
from openatlas.forms import build_form
from openatlas.util.util import required_group, sanitize, uc_first


class HierarchyForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    multiple = BooleanField(uc_first(_('multiple')), uc_first(_('active')))
    forms = SelectMultipleField(
        uc_first(_('forms')),
        description=_('tooltip multiple hierarchies'),
        choices=NodeMapper.get_forms(),
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
    description = TextAreaField(uc_first(_('description')))
    save = SubmitField(_('insert'))


@app.route('/hierarchy/insert', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_insert():
    form = build_form(HierarchyForm, 'hierarchy')
    if form.validate_on_submit():
        node = save(form)
        flash(_('entity created'), 'info')
        return redirect(url_for('node_index') + '#tab-' + str(node.id))
    return render_template('hierarchy/insert.html', form=form)


@app.route('/hierarchy/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_update(id_):
    node = openatlas.nodes[id_]
    if node.system:
        flash(_('error forbidden'), 'error')
        return redirect(url_for('node_view', id_=id_))
    form = build_form(HierarchyForm, 'hierarchy', node)
    if form.validate_on_submit():
        if save(form, node):
            flash(_('info update'), 'info')
            return redirect(url_for('node_index') + '#tab-' + str(node.id))
        return render_template('hierarchy/update.html', node=node, form=form)
    return render_template('hierarchy/update.html', node=node, form=form)


@app.route('/hierarchy/delete/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def hierarchy_delete(id_):
    node = openatlas.nodes[id_]
    if node.system or node.subs or node.count:
        flash(_('error forbidden'), 'error')
        return redirect(url_for('node_view', id_=id_))
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(node.id)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('node_index'))


def save(form, node=None):
    openatlas.get_cursor().execute('BEGIN')
    if not node:
        node = NodeMapper.insert('E55', form.name.data)
    else:
        node = openatlas.nodes[node.id]
    node.name = sanitize(form.name.data, 'node')
    node.description = form.description.data
    openatlas.get_cursor().execute('COMMIT')
    return node
