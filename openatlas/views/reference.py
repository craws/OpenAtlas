# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash
from flask_babel import gettext, lazy_gettext as _
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


@app.route('/reference/view/<int:reference_id>')
@required_group('readonly')
def reference_view(reference_id):
    reference = EntityMapper.get_by_id(reference_id)
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
        flash(gettext('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('reference_insert', code=code))
        return redirect(url_for('reference_view', reference_id=reference.id))
    return render_template('reference/insert.html', form=form, code=code)


@app.route('/reference/delete/<int:reference_id>')
@required_group('editor')
def reference_delete(reference_id):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(reference_id)
    openatlas.get_cursor().execute('COMMIT')
    flash(gettext('entity deleted'), 'info')
    return redirect(url_for('reference_index'))


@app.route('/reference/update/<int:reference_id>', methods=['POST', 'GET'])
@required_group('editor')
def reference_update(reference_id):
    reference = EntityMapper.get_by_id(reference_id)
    form = ReferenceForm()
    if form.validate_on_submit():
        reference.name = form.name.data
        reference.description = form.description.data
        reference.update()
        flash(gettext('entity updated'), 'info')
        return redirect(url_for('reference_view', reference_id=reference.id))
    form.name.data = reference.name
    form.description.data = reference.description
    return render_template('reference/update.html', form=form, reference=reference)
