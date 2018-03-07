# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import os

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect, secure_filename
from wtforms import FileField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired

import openatlas
from openatlas import app, logger
from openatlas.forms.forms import build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import (build_table_form, get_base_table_data, get_entity_data,
                                 get_file_path, link, required_group, was_modified)


class FileForm(Form):
    file = FileField(_('file'), [InputRequired()])
    name = StringField(_('name'), [DataRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    opened = HiddenField()


def allowed_file(name):
    return '.' in name and name.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/file/index')
@required_group('readonly')
def file_index():
    headers = ['date', 'name', 'license', 'size', 'description']
    table = {'id': 'files', 'header': headers, 'data': []}
    for file in EntityMapper.get_by_system_type('file'):
        table['data'].append(get_base_table_data(file))
    return render_template('file/index.html', table=table)


@app.route('/file/add/<int:origin_id>', methods=['GET', 'POST'])
@required_group('editor')
def file_add(origin_id):
    """ Link an entity to file coming from the entity."""
    origin = EntityMapper.get_by_id(origin_id)
    if request.method == 'POST':
        g.cursor.execute('BEGIN')
        try:
            for value in request.form.getlist('values'):
                LinkMapper.insert(int(value), 'P67', origin.id)
            g.cursor.execute('COMMIT')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        view_name = app.config['CODE_CLASS'][origin.class_.code]
        return redirect(url_for(view_name + '_view', id_=origin.id) + '#tab-file')
    form = build_table_form('file', origin.get_linked_entities('P67', True))
    return render_template('file/add.html', origin=origin, form=form)


@app.route('/file/view/<int:id_>')
@required_group('readonly')
def file_view(id_):
    entity = EntityMapper.get_by_id(id_)
    tables = {'info': get_entity_data(entity)}
    for name in ['source', 'event', 'actor', 'place', 'reference']:
        header = app.config['TABLE_HEADERS'][name]
        tables[name] = {'id': name, 'header': header, 'data': []}
    for link_ in entity.get_links('P67'):
        name = app.config['CODE_CLASS'][link_.range.class_.code]
        data = get_base_table_data(link_.range)
        tables[name]['data'].append(data)
    return render_template('file/view.html', entity=entity, tables=tables)


@app.route('/file/update/<int:id_>', methods=['GET', 'POST'])
@required_group('editor')
def file_update(id_):
    file = EntityMapper.get_by_id(id_)
    form = build_form(FileForm, 'File', file, request)
    del form.file
    if form.validate_on_submit():
        if was_modified(form, file):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(file.id)['modifier'])
            return render_template('file/update.html', form=form, file=file, modifier=modifier)
        if save(form, file):
            flash(_('info update'), 'info')
        return redirect(url_for('file_view', id_=id_))
    return render_template('file/update.html', form=form, file=file)


@app.route('/file/insert/<int:origin_id>', methods=['GET', 'POST'])
@required_group('editor')
def file_insert(origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = build_form(FileForm, 'File')
    if form.validate_on_submit():
        return redirect(save(form, None, origin))
    return render_template('file/insert.html', form=form, origin=origin)


@app.route('/file/delete/<int:id_>')
@required_group('editor')
def file_delete(id_=None):
    g.cursor.execute('BEGIN')
    try:
        EntityMapper.delete(id_)
        logger.log_user(id_, 'delete')
        g.cursor.execute('COMMIT')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    try:
        path = get_file_path(id_)
        if path:
            os.remove(get_file_path(id_))
    except Exception as e:  # pragma: no cover
        logger.log('error', 'file', 'file deletion failed', e)
        flash(_('error file delete'), 'error')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('file_index'))


def save(form, entity=None, origin=None):
    g.cursor.execute('BEGIN')
    try:
        if entity:
            logger.log_user(entity.id, 'update')
        else:
            file_ = request.files['file']
            if file_ and allowed_file(file_.filename):
                entity = EntityMapper.insert('E31', form.name.data, 'file')
                filename = secure_filename(file_.filename)
                new_name = str(entity.id) + '.' + filename.rsplit('.', 1)[1].lower()
                full_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
                file_.save(full_path)
                logger.log_user(entity.id, 'insert')
            else:
                1/0  # Todo: give feedback if upload failed
        entity.name = form.name.data
        entity.description = form.description.data
        entity.update()
        entity.save_nodes(form)
        url = url_for('file_view', id_=entity.id)
        if origin:
            entity.link('P67', origin)
            view = app.config['CODE_CLASS'][origin.class_.code]
            url = url_for(view + '_view', id_=origin.id) + '#tab-file'
        g.cursor.execute('COMMIT')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        openatlas.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('file_insert', origin_id=origin.id if origin else None)
    return url
