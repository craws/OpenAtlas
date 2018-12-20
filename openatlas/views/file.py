# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os

import datetime
import math
from flask import flash, g, render_template, request, send_from_directory, session, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect, secure_filename
from wtforms import FileField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app, logger
from openatlas.forms.forms import build_form
from openatlas.models.entity import EntityMapper
from openatlas.util.util import (build_table_form, convert_size, display_remove_link, format_date,
                                 get_base_table_data, get_entity_data, get_file_path, is_authorized,
                                 link, required_group, truncate_string, uc_first, was_modified)


class FileForm(Form):
    file = FileField(_('file'), [InputRequired()])
    name = StringField(_('name'), [InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    opened = HiddenField()

    def validate(self, extra_validators=None):
        valid = Form.validate(self)
        if request.files:
            file_ = request.files['file']
            ext = session['settings']['file_upload_allowed_extension'].split()
            if not file_:  # pragma: no cover
                self.file.errors.append(_('no file to upload'))
                valid = False
            elif not ('.' in file_.filename and file_.filename.rsplit('.', 1)[1].lower() in ext):
                self.file.errors.append(_('file type not allowed'))
                valid = False
        return valid


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


@app.route('/display_logo/<path:filename>')
def display_logo(filename):  # File display function for public
    return send_from_directory(app.config['UPLOAD_FOLDER_PATH'], filename)


@app.route('/file/set_as_profile_image/<int:id_>/<int:origin_id>')
def file_set_as_profile_image(id_, origin_id):
    EntityMapper.set_profile_image(id_, origin_id)
    origin = EntityMapper.get_by_id(origin_id)
    return redirect(url_for(app.config['CODE_CLASS'][origin.class_.code] + '_view', id_=origin.id))


@app.route('/file/set_as_profile_image/<int:entity_id>')
def file_remove_profile_image(entity_id):
    entity = EntityMapper.get_by_id(entity_id)
    entity.remove_profile_image()
    return redirect(url_for(app.config['CODE_CLASS'][entity.class_.code] + '_view', id_=entity.id))


@app.route('/file/index')
@required_group('readonly')
def file_index():
    table = {'id': 'files', 'header': ['date'] + app.config['TABLE_HEADERS']['file'], 'data': []}
    path = app.config['UPLOAD_FOLDER_PATH']
    files_in_dir = {}
    # Build a dict with file ids and stats from existing files in directory
    # It's much faster to do this in one call instead for every file

    # When python3.6 change to:
    # with os.scandir(app.config['UPLOAD_FOLDER_PATH']) as it:
    #     for file in it:
    for file in os.scandir(app.config['UPLOAD_FOLDER_PATH']):
        split_name = os.path.splitext(file.name)
        if len(split_name) > 1 and split_name[0].isdigit():
            files_in_dir[int(split_name[0])] = {
                'ext': split_name[1],
                'size': file.stat().st_size,
                'date': file.stat().st_ctime}
    for entity in EntityMapper.get_by_system_type('file'):
        date = 'N/A'
        if entity.id in files_in_dir:
            date = format_date(datetime.datetime.utcfromtimestamp(files_in_dir[entity.id]['date']))
        table['data'].append([
            date,
            link(entity),
            entity.print_base_type(),
            convert_size(files_in_dir[entity.id]['size']) if entity.id in files_in_dir else 'N/A',
            files_in_dir[entity.id]['ext'] if entity.id in files_in_dir else 'N/A',
            truncate_string(entity.description)])

    statvfs = os.statvfs(path)
    disk_space = statvfs.f_frsize * statvfs.f_blocks
    free_space = statvfs.f_frsize * statvfs.f_bavail  # Available space without reserved blocks
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
        origin.link('P67', request.form.getlist('values'), inverse=True)
        return redirect(url_for(origin.view_name + '_view', id_=origin.id) + '#tab-file')
    form = build_table_form('file', origin.get_linked_entities('P67', True))
    return render_template('file/add.html', origin=origin, form=form)


@app.route('/file/add2/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('editor')
def file_add2(id_, class_name):
    """ Link an entity to file coming from the file"""
    file = EntityMapper.get_by_id(id_)
    if request.method == 'POST':
        file.link('P67', request.form.getlist('values'))
        return redirect(url_for('file_view', id_=file.id) + '#tab-' + class_name)
    form = build_table_form(class_name, file.get_linked_entities('P67'))
    return render_template('file/add2.html', entity=file, class_name=class_name, form=form)


@app.route('/file/view/<int:id_>')
@required_group('readonly')
def file_view(id_):
    file = EntityMapper.get_by_id(id_)
    path = get_file_path(file.id)
    tables = {'info': get_entity_data(file)}
    for name in ['source', 'event', 'actor', 'place', 'feature', 'stratigraphic-unit', 'find',
                 'reference']:
        header = app.config['TABLE_HEADERS'][name] + (['page'] if name == 'reference' else [])
        tables[name] = {'id': name, 'data': [], 'header': header}
    for link_ in file.get_links('P67'):
        range_ = link_.range
        data = get_base_table_data(range_)
        view_name = range_.view_name
        view_name = view_name if view_name != 'place' else range_.system_type.replace(' ', '-')
        if is_authorized('editor'):
            url = url_for('link_delete', id_=link_.id, origin_id=file.id)
            data.append(display_remove_link(url + '#tab-' + view_name, range_.name))
        tables[view_name]['data'].append(data)
    for link_ in file.get_links('P67', True):
        data = get_base_table_data(link_.domain)
        data.append(link_.description)
        if is_authorized('editor'):
            update_url = url_for('reference_link_update', link_id=link_.id, origin_id=file.id)
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=file.id)
            data.append(display_remove_link(unlink_url + '#tab-reference', link_.domain.name))
        tables['reference']['data'].append(data)
    return render_template('file/view.html', missing_file=False if path else True, entity=file,
                           tables=tables, preview=True if path and preview_file(path) else False,
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
        return redirect(save(form, origin=origin))
    return render_template('file/insert.html', form=form, origin=origin)


@app.route('/file/delete/<int:id_>')
@required_group('editor')
def file_delete(id_=None):
    try:
        EntityMapper.delete(id_)
        logger.log_user(id_, 'delete')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'database', 'Deletion failed', e)
        flash(_('error database'), 'error')
    try:
        path = get_file_path(id_)
        if path:
            os.remove(path)
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
                link_id = origin.link('P67', file)
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            else:
                file.link('P67', origin)
                url = url_for(origin.view_name + '_view', id_=origin.id) + '#tab-file'
        g.cursor.execute('COMMIT')
        logger.log_user(file.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        openatlas.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('file_index', origin_id=origin.id if origin else None)
    return url
