# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm
from openatlas.models.entity import EntityMapper
from openatlas.util.util import link, truncate_string, required_group


class PlaceForm(DateForm):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/place')
@required_group('readonly')
def place_index():
    tables = {'place': {'name': 'place', 'header': ['name', _('first'), _('last'), 'info'], 'data': []}}
    for place in EntityMapper.get_by_codes('E18'):
        tables['place']['data'].append([
            link(place),
            format(place.first),
            format(place.last),
            truncate_string(place.description)
        ])
    return render_template('place/index.html', tables=tables)


@app.route('/place/insert/<code>', methods=['POST', 'GET'])
@required_group('editor')
def place_insert(code):
    form = PlaceForm()
    if form.validate_on_submit():
        openatlas.get_cursor().execute('BEGIN')
        place = EntityMapper.insert(code, form.name.data, form.description.data)
        place.save_dates(form)
        openatlas.get_cursor().execute('COMMIT')
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('place_insert', code='E18'))
        return redirect(url_for('place_view', place_id=place.id))
    return render_template('place/insert.html', form=form)


@app.route('/place/view/<int:place_id>')
@required_group('readonly')
def place_view(place_id):
    place = EntityMapper.get_by_id(place_id)
    place.set_dates()
    data = {'info': [
        (_('name'), place.name),
    ]}
    return render_template('place/view.html', place=place, data=data)


@app.route('/place/delete/<int:place_id>')
@required_group('editor')
def place_delete(place_id):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(place_id)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('place_index'))


@app.route('/place/update/<int:place_id>', methods=['POST', 'GET'])
@required_group('editor')
def place_update(place_id):
    place = EntityMapper.get_by_id(place_id)
    place.set_dates()
    form = PlaceForm()
    if form.validate_on_submit():
        place.name = form.name.data
        place.description = form.description.data
        openatlas.get_cursor().execute('BEGIN')
        place.update()
        place.delete_dates()
        place.save_dates(form)
        openatlas.get_cursor().execute('COMMIT')
        flash(_('info update'), 'info')
        return redirect(url_for('place_view', place_id=place.id))
    form.name.data = place.name
    form.description.data = place.description
    form.populate_dates(place)
    return render_template('place/update.html', form=form, place=place)
