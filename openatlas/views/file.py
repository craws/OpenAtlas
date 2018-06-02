# Created by Alexander Watzinger and others. Please see README.md for licensing information
import math
import os

from flask import flash, g, render_template, request, send_from_directory, session, url_for
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
from openatlas.util.util import (build_table_form, convert_size, display_remove_link,
                                 get_base_table_data, get_entity_data, get_file_path,
                                 get_view_name, link, required_group, was_modified)


class FileForm(Form):
    file = FileField(_('file'), [InputRequired()])
    name = StringField(_('name'), [DataRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    opened = HiddenField()


def allowed_file(name):
    allowed_extensions = session['settings']['file_upload_allowed_extension'].split()
    return '.' in name and name.rsplit('.', 1)[1].lower() in allowed_extensions


def preview_file(name):
    return name.rsplit('.', 1)[1].lower() in app.config['DISPLAY_FILE_EXTENSIONS']


@app.route('/download/<path:filename>')
@required_group('readonly')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_PATH'], filename, as_attachment=True)


@app.route('/display/<path:filename>')
@required_group('readonly')
def display_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_PATH'], filename)


@app.route('/file/index')
@required_group('readonly')
def file_index():
    table = {'id': 'files', 'header': app.config['TABLE_HEADERS']['file'], 'data': []}
    for file in EntityMapper.get_by_system_type('file'):
        table['data'].append(get_base_table_data(file))
    statvfs = os.statvfs('/')
    disk_space = statvfs.f_frsize * statvfs.f_blocks
    free_space = statvfs.f_frsize * statvfs.f_bavail  # available space without reserved blocks
    disk_space_values = {
        'total': convert_size(statvfs.f_frsize * statvfs.f_blocks),
        'free': convert_size(statvfs.f_frsize * statvfs.f_bavail),
        'percent': 100 - math.ceil(free_space / (disk_space / 100))}
    return render_template('file/index.html', table=table, disk_space_values=disk_space_values)


@app.route('/file/add/<int:origin_id>', methods=['GET', 'POST'])
@required_group('editor')
def file_add(origin_id):
    """ Link an entity to file coming from the entity."""
    origin = EntityMapper.get_by_id(origin_id)
    if request.method == 'POST':
        g.cursor.execute('BEGIN')
        try:
            for value in request.form.getlist('values'):
                if origin.system_type in ['edition', 'bibliography']:
                    LinkMapper.insert(origin.id, 'P67', int(value))
                else:
                    LinkMapper.insert(int(value), 'P67', origin.id)
            g.cursor.execute('COMMIT')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for(get_view_name(origin) + '_view', id_=origin.id) + '#tab-file')
    form = build_table_form('file', origin.get_linked_entities('P67', True))
    return render_template('file/add.html', origin=origin, form=form)


@app.route('/file/add2/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('editor')
def file_add2(id_, class_name):
    """ Link an entity to file coming from the file"""
    file = EntityMapper.get_by_id(id_)
    if request.method == 'POST':
        for value in request.form.getlist('values'):
            if class_name == 'reference':
                LinkMapper.insert(int(value), 'P67', file)
            else:
                file.link('P67', int(value))
        return redirect(url_for('file_view', id_=file.id) + '#tab-' + class_name)
    form = build_table_form(class_name, file.get_linked_entities('P67'))
    return render_template('file/add2.html', entity=file, class_name=class_name, form=form)


@app.route('/file/view/<int:id_>')
@app.route('/file/view/<int:id_>/<int:unlink_id>')
@required_group('readonly')
def file_view(id_, unlink_id=None):
    file = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
        flash(_('link removed'), 'info')
    path = get_file_path(file.id)
    tables = {'info': get_entity_data(file)}
    for name in ['source', 'event', 'actor', 'place', 'reference']:
        tables[name] = {'id': name, 'header': app.config['TABLE_HEADERS'][name], 'data': []}
    for link_ in file.get_links('P67'):
        view_name = get_view_name(link_.range)
        data = get_base_table_data(link_.range)
        unlink_url = url_for('file_view', id_=file.id, unlink_id=link_.id) + '#tab-' + view_name
        data.append(display_remove_link(unlink_url, link_.range.name))
        tables[view_name]['data'].append(data)
    for link_ in file.get_links('P67', True):
        data = get_base_table_data(link_.domain)
        unlink_url = url_for('file_view', id_=file.id, unlink_id=link_.id) + '#tab-reference'
        data.append(display_remove_link(unlink_url, link_.domain.name))
        tables['reference']['data'].append(data)
    return render_template(
        'file/view.html',
        missing_file=False if path else True,
        entity=file,
        tables=tables,
        preview=True if path and preview_file(path) else False,
        filename=os.path.basename(path) if path else False)


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
        save(form, file)
        return redirect(url_for('file_view', id_=id_))
    return render_template('file/update.html', form=form, file=file)


@app.route('/file/insert', methods=['GET', 'POST'])
@app.route('/file/insert/<int:origin_id>', methods=['GET', 'POST'])
@required_group('editor')
def file_insert(origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = build_form(FileForm, 'File')
    if form.validate_on_submit():
        file_ = request.files['file']
        if not file_:  # pragma: no cover
            flash(_('no file to upload'), 'error')
        elif not allowed_file(file_.filename):
            flash(_('file type not allowed'), 'error')
        else:
            return redirect(save(form, origin=origin))
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


def save(form, file=None, origin=None):
    g.cursor.execute('BEGIN')
    try:
        log_action = 'update'
        if not file:
            log_action = 'insert'
            file_ = request.files['file']
            file = EntityMapper.insert('E31', form.name.data, 'file')
            filename = secure_filename(file_.filename)
            new_name = str(file.id) + '.' + filename.rsplit('.', 1)[1].lower()
            full_path = os.path.join(app.config['UPLOAD_FOLDER_PATH'], new_name)
            file_.save(full_path)
        file.name = form.name.data
        file.description = form.description.data
        file.update()
        file.save_nodes(form)
        url = url_for('file_view', id_=file.id)
        if origin:
            if origin.system_type in ['edition', 'bibliography']:
                origin.link('P67', file)
            else:
                file.link('P67', origin)
            url = url_for(get_view_name(origin) + '_view', id_=origin.id) + '#tab-file'
        g.cursor.execute('COMMIT')
        logger.log_user(file.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        openatlas.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('file_index', origin_id=origin.id if origin else None)
    return url
