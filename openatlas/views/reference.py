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
from openatlas.models.entity import EntityMapper
from openatlas.util.util import uc_first, link, truncate_string, required_group, append_node_data


class ReferenceForm(Form):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/reference/view/<int:id_>')
@required_group('readonly')
def reference_view(id_):
    reference = EntityMapper.get_by_id(id_)
    data = {'info': []}
    append_node_data(data['info'], reference)
    return render_template('reference/view.html', reference=reference, data=data)


@app.route('/reference')
@required_group('readonly')
def reference_index():
    tables = {'reference': {
        'name': 'reference',
        'header': ['name', 'class', 'type', 'info'],
        'data': []}}
    for reference in EntityMapper.get_by_codes('reference'):
        class_name = _(reference.system_type).title()
        tables['reference']['data'].append([
            link(reference),
            class_name,
            reference.print_base_type(),
            truncate_string(reference.description)])
    return render_template('reference/index.html', tables=tables)


@app.route('/reference/insert/<code>', methods=['POST', 'GET'])
@required_group('editor')
def reference_insert(code):
    form_code = 'Information Carrier' if code == 'carrier' else uc_first(code)
    form = build_form(ReferenceForm, uc_first(form_code))
    if form.validate_on_submit():
        class_code = 'E31'
        system_type = code
        if code == 'carrier':
            class_code = 'E84'
            system_type = 'information carrier'
        reference = save(form, EntityMapper.insert(class_code, form.name.data, system_type))
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('reference_insert', code=code))
        return redirect(url_for('reference_view', id_=reference.id))
    return render_template('reference/insert.html', form=form, code=code)


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


def save(form, entity):
    openatlas.get_cursor().execute('BEGIN')
    entity.name = form.name.data
    entity.description = form.description.data
    entity.update()
    entity.save_nodes(form)
    openatlas.get_cursor().execute('COMMIT')
    return entity
