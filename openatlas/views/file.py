# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast
import os

from flask import render_template, request, flash, url_for, g
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import secure_filename, redirect
from wtforms import FileField, TextAreaField, SubmitField, StringField
from wtforms.validators import InputRequired, DataRequired

import openatlas
from openatlas import app, EntityMapper
from openatlas.forms.forms import TableMultiField
from openatlas.util.util import (required_group, get_base_table_data, truncate_string, link,
                                 uc_first, format_date, print_file_size, get_entity_data)


class FileForm(Form):
    file = FileField(_('name'), [InputRequired()])
    name = StringField(_('name'), [DataRequired()])
    source = TableMultiField(_('source'))
    event = TableMultiField(_('event'))
    actor = TableMultiField(_('actor'))
    place = TableMultiField(_('place'))
    reference = TableMultiField(_('reference'))
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))


def allowed_file(name):
    return '.' in name and name.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/file/index')
@required_group('readonly')
def file_index():
    headers = ['date', 'name', 'license', 'size', 'description']
    table = {'id': 'files', 'header': headers, 'data': []}
    for file in EntityMapper.get_by_system_type('file'):
        table['data'].append([
            format_date(file.created),
            link(file),
            uc_first(_('license')),
            print_file_size(file),
            truncate_string(file.description)])
    return render_template('file/index.html', table=table)


@app.route('/file/add/<int:origin_id>', methods=['GET', 'POST'])
@required_group('editor')
def file_add(origin_id):
    return render_template('file/add.html')


@app.route('/file/view/<int:id_>')
@required_group('readonly')
def file_view(id_):
    entity = EntityMapper.get_by_id(id_)
    tables = {'info': get_entity_data(entity)}
    for name in ['source', 'event', 'actor', 'place', 'reference']:
        header = app.config['TABLE_HEADERS'][name] + ['page']
        tables[name] = {'id': name, 'header': header, 'data': []}
    for link_ in entity.get_links('P67'):
        name = app.config['CODE_CLASS'][link_.range.class_.code]
        data = get_base_table_data(link_.range)
        data.append(truncate_string(link_.description))
        tables[name]['data'].append(data)
    return render_template('file/view.html', entity=entity, tables=tables)


@app.route('/file/update/<int:id_>', methods=['GET', 'POST'])
@required_group('readonly')
def file_update(id_):
    form = FileForm()
    return render_template('file/update.html', form=form)


@app.route('/file/insert/<int:origin_id>', methods=['GET', 'POST'])
@required_group('editor')
def file_insert(origin_id):
    origin = EntityMapper.get_by_id(origin_id) if origin_id and origin_id != 0 else None
    form = FileForm()
    if form.validate_on_submit():
        entity = save(form)
        if origin:
            view = app.config['CODE_CLASS'][origin.class_.code]
            return redirect(url_for(view + '_view', id_=origin.id) + '#tab-file')
        return redirect(url_for('file_view', id_=entity.id))
    if origin_id:
        getattr(form, app.config['CODE_CLASS'][origin.class_.code]).data = [origin.id]
    return render_template('file/insert.html', form=form)


def save(form, entity=None):
    g.cursor.execute('BEGIN')
    try:
        if not entity:
            file_ = request.files['file']
            if file_ and allowed_file(file_.filename):
                entity = EntityMapper.insert('E31', form.name.data, 'file')
                filename = secure_filename(file_.filename)
                new_name = str(entity.id) + '.' + filename.rsplit('.', 1)[1].lower()
                full_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
                file_.save(full_path)
            else:
                return 1 / 0
        else:
            entity.delete_links('P67')
        entity.name = form.name.data
        entity.description = form.description.data
        entity.update()
        link_data = []
        for name in ['source', 'event', 'actor', 'place', 'reference']:
            data = getattr(form, name).data
            if data:
                link_data = link_data + ast.literal_eval(data)
        if link_data:
            entity.link('P67', link_data)
            g.cursor.execute('COMMIT')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        openatlas.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        return
    return entity
