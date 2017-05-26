# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template, url_for, flash
from flask_babel import gettext, lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.util.util import uc_first, link, truncate_string


class SourceForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('content')))
    continue_ = HiddenField()


@app.route('/source')
def source_index():
    tables = {'source': {
        'name': 'source',
        # 'sort': 'sortList: [[3, 1]]',
        'header': ['name', 'info'],
        'data': []}}
    for source in EntityMapper.get_by_codes('E33'):
        tables['source']['data'].append([
            link(source),
            truncate_string(source.description)
        ])
    return render_template('source/index.html', tables=tables)


@app.route('/source/insert/<code>', methods=['POST', 'GET'])
def source_insert(code):
    form = SourceForm()
    if form.validate_on_submit():
        source = EntityMapper.insert(code, form.name.data, form.description.data)
        flash(gettext('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('source_insert', code='E33'))
        return redirect(url_for('source_view', source_id=source.id))
    return render_template('source/insert.html', form=form)


@app.route('/source/view/<int:source_id>')
def source_view(source_id):
    source = EntityMapper.get_by_id(source_id)
    return render_template('source/view.html', source=source)


@app.route('/source/delete/<int:source_id>')
def source_delete(source_id):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(source_id)
    openatlas.get_cursor().execute('COMMIT')
    flash(gettext('entity deleted'), 'info')
    return redirect(url_for('source_index'))


@app.route('/source/update/<int:source_id>', methods=['POST', 'GET'])
def source_update(source_id):
    source = EntityMapper.get_by_id(source_id)
    form = SourceForm()
    if form.validate_on_submit():
        source.name = form.name.data
        source.description = form.description.data
        source.update()
        flash(gettext('entity updated'), 'info')
        return redirect(url_for('source_view', source_id=source.id))
    form.name.data = source.name
    form.description.data = source.description
    return render_template('source/update.html', form=form, source=source)
