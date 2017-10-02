# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.util.util import uc_first, link, truncate_string, required_group


class ReferenceForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('description')))
    continue_ = HiddenField()


@app.route('/reference/view/<int:id_>')
@required_group('readonly')
def reference_view(id_):
    reference = EntityMapper.get_by_id(id_)
    data = {'info': [
        (_('name'), reference.name),
    ]}
    return render_template('reference/view.html', reference=reference, data=data)


@app.route('/reference')
@required_group('readonly')
def reference_index():
    tables = {'reference': {
        'name': 'reference',
        # 'sort': 'sortList: [[3, 1]]',
        'header': ['name', 'class', 'info'],
        'data': []}}
    for reference in EntityMapper.get_by_codes(['E31', 'E84']):
        if openatlas.classes[reference.class_.id].code == 'E84':
            class_name = openatlas.classes[reference.class_.id].name
        else:
            class_name = 'Bibliography or Edition (to do)'
        tables['reference']['data'].append([
            link(reference),
            class_name,
            truncate_string(reference.description)
        ])
    return render_template('reference/index.html', tables=tables)


@app.route('/reference/insert/<code>', methods=['POST', 'GET'])
@required_group('editor')
def reference_insert(code):
    form = ReferenceForm()
    if form.validate_on_submit():
        reference = EntityMapper.insert('E84' if code == 'carrier' else 'E31', form.name.data, form.description.data)
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
    form = ReferenceForm()
    if form.validate_on_submit():
        reference.name = form.name.data
        reference.description = form.description.data
        reference.update()
        flash(_('info update'), 'info')
        return redirect(url_for('reference_view', id_=id_))
    form.name.data = reference.name
    form.description.data = reference.description
    return render_template('reference/update.html', form=form, reference=reference)
