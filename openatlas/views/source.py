# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
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
from openatlas.models.link import LinkMapper
from openatlas.util.util import (uc_first, link, truncate_string, required_group, append_node_data,
                                 print_base_type)


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
        'header': ['name', 'type', 'info'],
        'data': []}}
    for source in EntityMapper.get_by_codes('E33', 'source content'):
        tables['source']['data'].append([
            link(source),
            print_base_type(source, 'Source'),
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
    data = {'info': []}
    append_node_data(data['info'], source)
    tables = {'translation': {
        'name': 'translation',
        'header': ['translations', 'type', 'text'],
        'data': []}}
    for translation in source.get_linked_entities('P73'):
        tables['translation']['data'].append([
            link(translation),
            translation.nodes[0].name if translation.nodes else '',
            truncate_string(translation.description)])
    return render_template('source/view.html', source=source, data=data, tables=tables)


@app.route('/source/delete/<int:id_>')
@required_group('editor')
def source_delete(id_):
    source = EntityMapper.get_by_id(id_)
    openatlas.get_cursor().execute('BEGIN')
    for translation in source.get_linked_entities('P73'):
        EntityMapper.delete(translation.id)
    EntityMapper.delete(source.id)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('source_index'))


@app.route('/source/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def source_update(id_):
    source = EntityMapper.get_by_id(id_)
    form = build_custom_form(SourceForm, 'Source', source, request)
    if form.validate_on_submit():
        save(form, source)
        flash(_('info update'), 'info')
        return redirect(url_for('source_view', id_=id_))
    return render_template('source/update.html', form=form, source=source)


def save(form, entity=None):
    openatlas.get_cursor().execute('BEGIN')
    if not entity:
        entity = EntityMapper.insert('E33', form.name.data, 'source content')
    entity.name = form.name.data
    entity.description = form.description.data
    entity.update()
    entity.save_nodes(form)
    openatlas.get_cursor().execute('COMMIT')
    return entity
