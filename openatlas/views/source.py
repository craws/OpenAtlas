# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict

from flask import render_template, url_for, flash, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import build_custom_form
from openatlas.models.entity import EntityMapper
from openatlas.util.util import uc_first, link, truncate_string, required_group


class SourceForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('content')))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/source')
@required_group('readonly')
def source_index():
    tables = {'source': {
        'name': 'source',
        'header': ['name', 'info'],
        'data': []}}
    for source in EntityMapper.get_by_codes('E33'):
        tables['source']['data'].append([
            link(source),
            truncate_string(source.description)])
    return render_template('source/index.html', tables=tables)


@app.route('/source/insert', methods=['POST', 'GET'])
@required_group('editor')
def source_insert():
    form = build_custom_form(SourceForm, 'Source')
    if form.validate_on_submit():
        source = save(form)
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('source_insert'))
        return redirect(url_for('source_view', id_=source.id))
    return render_template('source/insert.html', form=form)


@app.route('/source/view/<int:id_>')
@required_group('readonly')
def source_view(id_):
    source = EntityMapper.get_by_id(id_)
    data = {'info': [(_('name'), source.name)]}
    type_data = OrderedDict()
    for node in source.nodes:
        if not node.root:
            continue
        root = openatlas.nodes[node.root[-1]]
        if not root.extendable:
            continue
        if root.name not in type_data:
            type_data[root.name] = []
        type_data[root.name].append(node.name)
    for root_name, nodes in type_data.items():
        data['info'].append((root_name, '<br />'.join(nodes)))
    return render_template('source/view.html', source=source, data=data)


@app.route('/source/delete/<int:id_>')
@required_group('editor')
def source_delete(id_):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(id_)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('source_index'))


@app.route('/source/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def source_update(id_):
    source = EntityMapper.get_by_id(id_)
    form = build_custom_form(SourceForm, 'Source', source if request.method == 'GET' else None)
    if form.validate_on_submit():
        save(form, source)
        flash(_('info update'), 'info')
        return redirect(url_for('source_view', id_=id_))
    return render_template('source/update.html', form=form, source=source)


def save(form, source=None):
    openatlas.get_cursor().execute('BEGIN')
    if source:
        pass
    else:
        source = EntityMapper.insert('E33', form.name.data)
    source.name = form.name.data
    source.description = form.description.data
    source.update()
    source.save_nodes(form)
    from openatlas import NodeMapper
    for node_id in NodeMapper.get_nodes('Linguistic object classification'):
        if openatlas.nodes[node_id].name == 'Source Content':
            source.link('P2', node_id)
            break
    openatlas.get_cursor().execute('COMMIT')
    return source
