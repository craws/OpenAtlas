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
from openatlas.util.util import uc_first, link, truncate_string, required_group


class PlaceForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('content')))
    continue_ = HiddenField()


@app.route('/place')
@required_group('readonly')
def place_index():
    tables = {'place': {
        'name': 'place',
        # 'sort': 'sortList: [[3, 1]]',
        'header': ['name', 'info'],
        'data': []}}
    for place in EntityMapper.get_by_codes('E18'):
        tables['place']['data'].append([
            link(place),
            truncate_string(place.description)
        ])
    return render_template('place/index.html', tables=tables)


@app.route('/place/insert/<code>', methods=['POST', 'GET'])
@required_group('editor')
def place_insert(code):
    form = PlaceForm()
    if form.validate_on_submit():
        place = EntityMapper.insert(code, form.name.data, form.description.data)
        flash(gettext('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('place_insert', code='E18'))
        return redirect(url_for('place_view', place_id=place.id))
    return render_template('place/insert.html', form=form)


@app.route('/place/view/<int:place_id>')
@required_group('readonly')
def place_view(place_id):
    place = EntityMapper.get_by_id(place_id)
    return render_template('place/view.html', place=place)


@app.route('/place/delete/<int:place_id>')
@required_group('editor')
def place_delete(place_id):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(place_id)
    openatlas.get_cursor().execute('COMMIT')
    flash(gettext('entity deleted'), 'info')
    return redirect(url_for('place_index'))


@app.route('/place/update/<int:place_id>', methods=['POST', 'GET'])
@required_group('editor')
def place_update(place_id):
    place = EntityMapper.get_by_id(place_id)
    form = PlaceForm()
    if form.validate_on_submit():
        place.name = form.name.data
        place.description = form.description.data
        place.update()
        flash(gettext('entity updated'), 'info')
        return redirect(url_for('place_view', place_id=place.id))
    form.name.data = place.name
    form.description.data = place.description
    return render_template('place/update.html', form=form, place=place)
