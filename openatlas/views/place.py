# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for, flash, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.forms import DateForm, build_form
from openatlas.models.entity import EntityMapper
from openatlas.util.util import (link, truncate_string, required_group, append_node_data,
                                 print_base_type)


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
        'header': [_('name'), _('site'), _('first'), _('last'), _('info')],
        'data': []}}
    for place in EntityMapper.get_by_codes('place'):
        tables['place']['data'].append([
            link(place),
            print_base_type(place, 'Site'),
            format(place.first),
            format(place.last),
            truncate_string(place.description)])
    return render_template('place/index.html', tables=tables)


@app.route('/place/insert', methods=['POST', 'GET'])
@required_group('editor')
def place_insert():
    form = build_form(PlaceForm, 'Place')
    if form.validate_on_submit():
        object_ = save(form)
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('place_insert', code='E18'))
        return redirect(url_for('place_view', id_=object_.id))
    return render_template('place/insert.html', form=form)


@app.route('/place/view/<int:id_>')
@required_group('readonly')
def place_view(id_):
    object_ = EntityMapper.get_by_id(id_)
    object_.set_dates()
    location = object_.get_linked_entity('P53')
    data = {'info': []}
    append_node_data(data['info'], object_, location)
    return render_template('place/view.html', object_=object_, data=data)


@app.route('/place/delete/<int:id_>')
@required_group('editor')
def place_delete(id_):
    place = EntityMapper.get_by_id(id_)
    openatlas.get_cursor().execute('BEGIN')
    EntityMapper.delete(place.get_linked_entity('P53'))
    EntityMapper.delete(id_)
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('place_index'))


@app.route('/place/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def place_update(id_):
    object_ = EntityMapper.get_by_id(id_)
    object_.set_dates()
    location = object_.get_linked_entity('P53')
    form = build_form(PlaceForm, 'Place', object_, request, location)
    if form.validate_on_submit():
        save(form, object_, location)
        flash(_('info update'), 'info')
        return redirect(url_for('place_view', id_=id_))
    return render_template('place/update.html', form=form, object_=object_)


def save(form, object_=None, location=None):
    openatlas.get_cursor().execute('BEGIN')
    if not object_:
        object_ = EntityMapper.insert('E18', form.name.data)
        location = EntityMapper.insert('E53', 'Location of ' + form.name.data, 'place location')
        object_.link('P53', location)
    object_.name = form.name.data
    object_.description = form.description.data
    object_.update()
    object_.save_dates(form)
    object_.save_nodes(form)
    location.name = 'Location of ' + form.name.data
    location.update()
    location.save_nodes(form)
    openatlas.get_cursor().execute('COMMIT')
    return object_
