# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import build_form
from openatlas.models.entity import EntityMapper, Entity
from openatlas.models.link import LinkMapper
from openatlas.util.util import (link, truncate_string, required_group, append_node_data,
                                 build_table_form, build_remove_link, build_delete_link, uc_first,
                                 get_base_table_data)


class SourceForm(Form):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/source')
@required_group('readonly')
def source_index():
    header = app.config['TABLE_HEADERS']['source'] + ['description']
    table = {'name': 'source', 'header': header, 'data': []}
    for source in EntityMapper.get_by_codes('source'):
        data = get_base_table_data(source)
        data.append(truncate_string(source.description))
        table['data'].append(data)
    return render_template('source/index.html', table=table)


@app.route('/source/insert/<int:origin_id>', methods=['POST', 'GET'])
@app.route('/source/insert', methods=['POST', 'GET'])
@required_group('editor')
def source_insert(origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = build_form(SourceForm, 'Source')
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        result = save(form, None, origin)
        flash(_('entity created'), 'info')
        if not isinstance(result, Entity):
            return redirect(url_for('reference_link_update', link_id=result, origin_id=origin_id))
        if form.continue_.data == 'yes':
            return redirect(url_for('source_insert', origin_id=origin_id))
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-source')
        return redirect(url_for('source_view', id_=result.id))
    return render_template('source/insert.html', form=form, origin=origin)


@app.route('/source/view/<int:id_>/<int:unlink_id>')
@app.route('/source/view/<int:id_>')
@required_group('readonly')
def source_view(id_, unlink_id=None):
    source = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
    tables = {'info': []}
    append_node_data(tables['info'], source)
    tables['translation'] = {
        'name': 'translation',
        'header': ['translations', 'type', 'text'],
        'data': []}
    for translation in source.get_linked_entities('P73'):
        tables['translation']['data'].append([
            link(translation),
            translation.nodes[0].name if translation.nodes else '',
            truncate_string(translation.description)])
    for name in ['event', 'place', 'actor']:
        header = app.config['TABLE_HEADERS'][name] + ['']
        tables[name] = {'name': name, 'header': header, 'data': []}
    for link_ in source.get_links('P67'):
        data = get_base_table_data(link_.range)
        name = app.config['CODE_CLASS'][link_.range.class_.code]
        unlink_url = url_for('source_view', id_=source.id, unlink_id=link_.id) + '#tab-' + name
        data.append(build_remove_link(unlink_url, link_.range.name))
        tables[name]['data'].append(data)
    header = app.config['TABLE_HEADERS']['reference'] + ['page', '', '']
    tables['reference'] = {'name': 'source', 'header': header, 'data': []}
    for link_ in source.get_links('P67', True):
        unlink_url = url_for('source_view', id_=source.id, unlink_id=link_.id) + '#tab-reference'
        update_url = url_for('reference_link_update', link_id=link_.id, origin_id=source.id)
        data = get_base_table_data(link_.domain)
        data.append(link_.description)
        data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        data.append(build_remove_link(unlink_url, link_.domain.name))
        tables['reference']['data'].append(data)
    del_link = build_delete_link(url_for('source_delete', id_=source.id), source.name)
    return render_template('source/view.html', source=source, tables=tables, delete_link=del_link)


@app.route('/source/add/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def source_add(origin_id):
    """Link an entity to source coming from the entity."""
    origin = EntityMapper.get_by_id(origin_id)
    if request.method == 'POST':
        openatlas.get_cursor().execute('BEGIN')
        for value in request.form.getlist('values'):
            LinkMapper.insert(int(value), 'P67', origin.id)
        openatlas.get_cursor().execute('COMMIT')
        view_name = app.config['CODE_CLASS'][origin.class_.code]
        return redirect(url_for(view_name + '_view', id_=origin.id) + '#tab-source')
    form = build_table_form('source', origin.get_linked_entities('P67', True))
    return render_template('source/add.html', origin=origin, form=form)


@app.route('/source/add2/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('editor')
def source_add2(id_, class_name):
    """Link an entity to source coming from the source."""
    source = EntityMapper.get_by_id(id_)
    if request.method == 'POST':
        for value in request.form.getlist('values'):
            source.link('P67', int(value))
        return redirect(url_for('source_view', id_=source.id) + '#tab-' + class_name)
    form = build_table_form(class_name, source.get_linked_entities('P67'))
    return render_template('source/add2.html', source=source, class_name=class_name, form=form)


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
    form = build_form(SourceForm, 'Source', source, request)
    if form.validate_on_submit():
        save(form, source)
        flash(_('info update'), 'info')
        return redirect(url_for('source_view', id_=id_))
    return render_template('source/update.html', form=form, source=source)


def save(form, entity=None, origin=None):
    openatlas.get_cursor().execute('BEGIN')
    entity = entity if entity else EntityMapper.insert('E33', form.name.data, 'source content')
    entity.name = form.name.data
    entity.description = form.description.data
    entity.update()
    entity.save_nodes(form)
    link_ = None
    if origin:
        if origin.class_.code in app.config['CLASS_CODES']['reference']:
            link_ = origin.link('P67', entity)
        else:
            entity.link('P67', origin)
    openatlas.get_cursor().execute('COMMIT')
    return link_ if link_ else entity
