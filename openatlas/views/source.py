# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.util.util import uc_first, link, truncate_string


class SourceForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('content')))


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
        # flash('Entity created', 'success')
        return redirect(url_for('source_view', source_id=source.id))
    return render_template('source/insert.html', form=form)


@app.route('/source/view/<int:source_id>')
def source_view(source_id):
    source = EntityMapper.get_by_id(source_id)
    return render_template('source/view.html', source=source)


@app.route('/source/delete/<int:source_id>')
def source_delete(source_id):
    pass


@app.route('/source/update/<int:source_id>')
def source_update(source_id):
    pass
