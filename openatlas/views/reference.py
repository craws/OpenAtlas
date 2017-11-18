# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import build_form, TableField
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import (uc_first, truncate_string, required_group, append_node_data,
                                 build_delete_link, build_remove_link, get_base_table_data)


class ReferenceForm(Form):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


class AddSourceForm(Form):
    source = TableField(_('source'))
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


class AddReferenceForm(Form):
    reference = TableField(_('reference'))
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


@app.route('/reference/add/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def reference_add(origin_id):
    """Link an entity to reference coming from the entity."""
    origin = EntityMapper.get_by_id(origin_id)
    class_name = app.config['CODE_CLASS'][origin.class_.code]
    form = AddReferenceForm()
    if form.validate_on_submit():
        reference = EntityMapper.get_by_id(form.reference.data)
        reference.link('P67', origin.id, form.page.data)
        return redirect(url_for(class_name + '_view', id_=origin.id) + '#tab-reference')
    return render_template('reference/add.html', origin=origin, form=form, class_name=class_name)


@app.route('/reference/add2/<int:reference_id>', methods=['POST', 'GET'])
@required_group('editor')
def reference_add2(reference_id):
    """Link an entity to reference coming from the reference."""
    reference = EntityMapper.get_by_id(reference_id)
    form = AddSourceForm()
    if form.validate_on_submit():
        reference.link('P67', form.source.data, form.page.data)
        return redirect(url_for('reference_view', id_=reference.id) + '#tab-source')
    return render_template(
        'reference/add.html', origin=reference, form=form, class_name='reference')


@app.route('/reference/link-update/<int:link_id>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def reference_link_update(link_id, origin_id):
    link_ = LinkMapper.get_by_id(link_id)
    origin = EntityMapper.get_by_id(origin_id)
    class_name = app.config['CODE_CLASS'][origin.class_.code]
    form = AddReferenceForm()
    form.save.label.text = _('save')
    del form.reference
    if form.validate_on_submit():
        link_.description = form.page.data
        link_.update()
        flash(_('info update'), 'info')
        tab = '#tab-reference'
        if class_name == 'reference':
            tab = '#tab-' + app.config['CODE_CLASS'][link_.range.class_.code]
        return redirect(url_for(class_name + '_view', id_=origin.id) + tab)
    form.page.data = link_.description
    return render_template(
        'reference/link-update.html',
        origin=origin,
        linked_object=link_.domain if link_.domain.id != origin.id else link_.range,
        form=form,
        class_name=class_name)


@app.route('/reference/view/<int:id_>')
@app.route('/reference/view/<int:id_>/<int:unlink_id>')
@required_group('readonly')
def reference_view(id_, unlink_id=None):
    reference = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
    tables = {'info': []}
    append_node_data(tables['info'], reference)
    for name in ['source', 'event', 'actor', 'place']:
        header = app.config['TABLE_HEADERS'][name] + ['page', '', '']
        tables[name] = {'name': name, 'header': header, 'data': []}
    for link_ in reference.get_links('P67'):
        name = app.config['CODE_CLASS'][link_.range.class_.code]
        update_url = url_for('reference_link_update', link_id=link_.id, origin_id=reference.id)
        unlink_url = url_for(
            'reference_view', id_=reference.id, unlink_id=link_.id) + '#tab-' + name
        data = get_base_table_data(link_.range)
        data.append(truncate_string(link_.description))
        data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        data.append(build_remove_link(unlink_url, link_.range.name))
        tables[name]['data'].append(data)
    delete_link = build_delete_link(url_for('reference_delete', id_=reference.id), reference.name)
    return render_template(
        'reference/view.html',
        reference=reference,
        tables=tables,
        delete_link=delete_link)


@app.route('/reference')
@required_group('readonly')
def reference_index():
    header = app.config['TABLE_HEADERS']['reference'] + ['description']
    table = {'name': 'reference', 'header': header, 'data': []}
    for reference in EntityMapper.get_by_codes('reference'):
        data = get_base_table_data(reference)
        data.append(truncate_string(reference.description))
        table['data'].append(data)
    return render_template('reference/index.html', table=table)


@app.route('/reference/insert/<code>', methods=['POST', 'GET'])
@app.route('/reference/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def reference_insert(code, origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form_code = 'Information Carrier' if code == 'carrier' else uc_first(code)
    form = build_form(ReferenceForm, uc_first(form_code))
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        result = save(form, None, code, origin)
        flash(_('entity created'), 'info')
        if origin:
            return redirect(url_for('reference_link_update', link_id=result, origin_id=origin_id))
        if form.continue_.data == 'yes':
            return redirect(url_for('reference_insert', code=code, origin_id=origin_id))
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-reference')
        return redirect(url_for('reference_view', id_=result.id))
    return render_template('reference/insert.html', form=form, code=code, origin=origin)


@app.route('/reference/delete/<int:id_>')
@required_group('editor')
def reference_delete(id_):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(id_)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('reference_index'))


@app.route('/reference/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def reference_update(id_):
    reference = EntityMapper.get_by_id(id_)
    form = build_form(ReferenceForm, reference.system_type.title(), reference, request)
    if form.validate_on_submit():
        save(form, reference)
        flash(_('info update'), 'info')
        return redirect(url_for('reference_view', id_=id_))
    return render_template('reference/update.html', form=form, reference=reference)


def save(form, entity, code=None, origin=None):
    openatlas.get_cursor().execute('BEGIN')
    if not entity:
        class_code = 'E31'
        system_type = code
        if code == 'carrier':
            class_code = 'E84'
            system_type = 'information carrier'
        entity = EntityMapper.insert(class_code, form.name.data, system_type)
    entity.name = form.name.data
    entity.description = form.description.data
    entity.update()
    entity.save_nodes(form)
    link_ = entity.link('P67', origin, '') if origin else None
    openatlas.get_cursor().execute('COMMIT')
    return link_ if link_ else entity
