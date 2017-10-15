# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_custom_form
from openatlas.models.entity import EntityMapper
from openatlas.util.util import link, truncate_string, required_group, append_node_data


class PlaceForm(DateForm):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/place')
@required_group('readonly')
def place_index():
    tables = {'place': {
        'name': 'place',
        'header': ['name', _('first'), _('last'), 'info'],
        'data': []}}
    for place in EntityMapper.get_by_codes('E18'):
        tables['place']['data'].append([
            link(place),
            format(place.first),
            format(place.last),
            truncate_string(place.description)])
    return render_template('place/index.html', tables=tables)


@app.route('/place/insert', methods=['POST', 'GET'])
@required_group('editor')
def place_insert():
    form = build_custom_form(PlaceForm, 'Place')
    if form.validate_on_submit():
        object = save(form, EntityMapper.insert('E18', form.name.data))
        place = save(form, EntityMapper.insert('E18', form.name.data))
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('place_insert', code='E18'))
        return redirect(url_for('place_view', id_=place.id))
    return render_template('place/insert.html', form=form)


@app.route('/place/view/<int:id_>')
@required_group('readonly')
def place_view(id_):
    place = EntityMapper.get_by_id(id_)
    place.set_dates()
    data = {'info': []}
    append_node_data(data['info'], place)
    return render_template('place/view.html', place=place, data=data)


@app.route('/place/delete/<int:id_>')
@required_group('editor')
def place_delete(id_):
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(id_)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('place_index'))


@app.route('/place/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def place_update(id_):
    place = EntityMapper.get_by_id(id_)
    place.set_dates()
    form = build_custom_form(PlaceForm, 'Place', place, request)
    if form.validate_on_submit():
        save(form, place)
        flash(_('info update'), 'info')
        return redirect(url_for('place_view', id_=id_))
    return render_template('place/update.html', form=form, place=place)


def save(form, entity):
    openatlas.get_cursor().execute('BEGIN')
    entity.name = form.name.data
    entity.description = form.description.data
    entity.update()
    entity.save_dates(form)
    # entity.save_nodes(form)
    openatlas.get_cursor().execute('COMMIT')
    return entity
