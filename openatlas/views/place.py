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
from openatlas.models.link import LinkMapper
from openatlas.util.util import (truncate_string, required_group, append_node_data,
                                 build_delete_link, build_remove_link, get_base_table_data)


class PlaceForm(DateForm):
    name = StringField(_('name'), validators=[InputRequired()])
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/place')
@required_group('readonly')
def place_index():
    table = {'name': 'place', 'header': app.config['TABLE_HEADERS']['place'], 'data': []}
    for place in EntityMapper.get_by_codes('place'):
        table['data'].append(get_base_table_data(place))
    return render_template('place/index.html', table=table)


@app.route('/place/insert', methods=['POST', 'GET'])
@app.route('/place/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def place_insert(origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = build_form(PlaceForm, 'Place')
    if form.validate_on_submit():
        object_ = save(form, None, None, origin)
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('place_insert', origin_id=origin_id))
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-place')
        return redirect(url_for('place_view', id_=object_.id))
    return render_template('place/insert.html', form=form, origin=origin)


@app.route('/place/view/<int:id_>')
@app.route('/place/view/<int:id_>/<int:unlink_id>')
@required_group('readonly')
def place_view(id_, unlink_id=None):
    object_ = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
    object_.set_dates()
    location = object_.get_linked_entity('P53')
    tables = {'info': []}
    append_node_data(tables['info'], object_, location)
    header = app.config['TABLE_HEADERS']['source'] + ['description', '']
    tables['source'] = {'name': 'source', 'header': header, 'data': []}
    for link_ in object_.get_links('P67', True):
        unlink_url = url_for('place_view', id_=object_.id, unlink_id=link_.id) + '#tab-source'
        data = get_base_table_data(link_.domain)
        data.append(truncate_string(link_.domain.description))
        data.append(build_remove_link(unlink_url, link_.domain.name))
        tables['source']['data'].append(data)
    del_link = build_delete_link(url_for('place_delete', id_=object_.id), object_.name)
    return render_template('place/view.html', object_=object_, tables=tables, delete_link=del_link)


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


def save(form, object_=None, location=None, origin=None):
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
    if origin:
        origin.link('P67', object_)
    openatlas.get_cursor().execute('COMMIT')
    return object_
