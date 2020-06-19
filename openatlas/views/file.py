import datetime
import os
from typing import Any, Optional, Union

from flask import flash, g, render_template, request, send_from_directory, session, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import Response
from wtforms import FileField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app, logger
from openatlas.forms.forms import build_form, build_table_form
from openatlas.models.entity import Entity
from openatlas.util.tab import Tab
from openatlas.util.table import Table
from openatlas.util.util import (button, convert_size, display_remove_link, format_date,
                                 get_base_table_data, get_entity_data, get_file_path,
                                 get_file_stats, is_authorized, link,
                                 required_group, uc_first, was_modified)


class FileForm(FlaskForm):  # type: ignore
    file = FileField(_('file'), [InputRequired()])
    name = StringField(_('name'), [InputRequired()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    opened = HiddenField()

    def validate(self) -> bool:
        valid = FlaskForm.validate(self)
        if request.files:
            file_ = request.files['file']
            ext = session['settings']['file_upload_allowed_extension']
            if not file_:  # pragma: no cover
                self.file.errors.append(_('no file to upload'))
                valid = False
            elif not ('.' in file_.filename and file_.filename.rsplit('.', 1)[1].lower() in ext):
                self.file.errors.append(_('file type not allowed'))
                valid = False
        return valid


def preview_file(name: str) -> bool:
    return name.rsplit('.', 1)[1].lower() in app.config['DISPLAY_FILE_EXTENSIONS']


@app.route('/download/<path:filename>')
@required_group('readonly')
def download_file(filename: str) -> Any:
    return send_from_directory(app.config['UPLOAD_FOLDER_PATH'], filename, as_attachment=True)


@app.route('/display/<path:filename>')
@required_group('readonly')
def display_file(filename: str) -> Any:
    return send_from_directory(app.config['UPLOAD_FOLDER_PATH'], filename)


@app.route('/display_logo/<path:filename>')
def display_logo(filename: str) -> Any:  # File display function for public
    return send_from_directory(app.config['UPLOAD_FOLDER_PATH'], filename)


@app.route('/file/set_as_profile_image/<int:id_>/<int:origin_id>')
def file_set_as_profile_image(id_: int, origin_id: int) -> Response:
    Entity.set_profile_image(id_, origin_id)
    return redirect(url_for('entity_view', id_=origin_id))


@app.route('/file/set_as_profile_image/<int:entity_id>')
def file_remove_profile_image(entity_id: int) -> Response:
    entity = Entity.get_by_id(entity_id)
    entity.remove_profile_image()
    return redirect(url_for('entity_view', id_=entity.id))


@app.route('/file/index')
@app.route('/file/<action>/<int:id_>')
@required_group('readonly')
def file_index(action: Optional[str] = None, id_: Optional[int] = None) -> str:
    if id_ and action == 'delete':
        try:
            Entity.delete_(id_)
            logger.log_user(id_, 'delete')
            flash(_('entity deleted'), 'info')
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
    table = Table(['date'] + Table.HEADERS['file'])
    file_stats = get_file_stats()
    for entity in Entity.get_by_system_type('file', nodes=True):
        date = 'N/A'
        if entity.id in file_stats:
            date = format_date(datetime.datetime.utcfromtimestamp(file_stats[entity.id]['date']))
        table.rows.append([
            date,
            link(entity),
            entity.print_base_type(),
            convert_size(file_stats[entity.id]['size']) if entity.id in file_stats else 'N/A',
            file_stats[entity.id]['ext'] if entity.id in file_stats else 'N/A',
            entity.description])
    return render_template('file/index.html', table=table)


@app.route('/file/add/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('contributor')
def file_add(id_: int, class_name: str) -> Union[str, Response]:
    file = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            file.link_string('P67', request.form['checkbox_values'])
        return redirect(url_for('entity_view', id_=file.id) + '#tab-' + class_name)
    form = build_table_form(class_name, file.get_linked_entities('P67'))
    return render_template('file/add.html', entity=file, class_name=class_name, form=form)


@app.route('/file/update/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def file_update(id_: int) -> Union[str, Response]:
    file_ = Entity.get_by_id(id_, nodes=True)
    form = build_form(FileForm, 'File', file_, request)
    del form.file
    if form.validate_on_submit():
        if was_modified(form, file_):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(file_.id)['modifier'])
            return render_template('file/update.html', form=form, file=file_, modifier=modifier)
        save(form, file_)
        return redirect(url_for('entity_view', id_=id_))
    return render_template('file/update.html', form=form, file=file_)


@app.route('/file/insert', methods=['GET', 'POST'])
@app.route('/file/insert/<int:origin_id>', methods=['GET', 'POST'])
@required_group('contributor')
def file_insert(origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    form = build_form(FileForm, 'File')
    if form.validate_on_submit():
        return redirect(save(form, origin=origin))
    writeable = True if os.access(app.config['UPLOAD_FOLDER_PATH'], os.W_OK) else False
    return render_template('file/insert.html', form=form, origin=origin, writeable=writeable)


def file_view(file: Entity) -> str:
    path = get_file_path(file.id)
    tabs = {'info': Tab('info')}
    for name in ['source', 'event', 'actor', 'place', 'feature', 'stratigraphic_unit', 'find',
                 'human_remains', 'reference']:
        tabs[name] = Tab(name, table=Table(
            Table.HEADERS[name] + (['page'] if name == 'reference' else [])))
    tabs['node'] = Tab('types', table=Table(Table.HEADERS['node']))
    tabs['event'].buttons = [button(_('add'), url_for('file_add', id_=file.id, class_name='event'))]
    for code in app.config['CLASS_CODES']['event']:
        tabs['event'].buttons.append(button(g.classes[code].name,
                                            url_for('event_insert', code=code, origin_id=file.id)))
    tabs['actor'].buttons = [
        button(_('add'), url_for('file_add', id_=file.id, class_name='actor'))]
    for code in app.config['CLASS_CODES']['actor']:
        tabs['actor'].buttons.append(
            button(g.classes[code].name, url_for('actor_insert', code=code, origin_id=file.id)))
    tabs['place'].buttons = [
        button(_('add'), url_for('file_add', id_=file.id, class_name='place')),
        button(_('place'), url_for('place_insert', origin_id=file.id))]
    tabs['reference'].buttons = [
        button(_('add'), url_for('entity_add_reference', id_=file.id)),
        button(_('bibliography'), url_for('reference_insert',
                                          code='bibliography', origin_id=file.id)),
        button(_('edition'), url_for('reference_insert', code='edition', origin_id=file.id)),
        button(_('external reference'), url_for('reference_insert',
                                                code='external_reference', origin_id=file.id))]
    for link_ in file.get_links('P67'):
        range_ = link_.range
        data = get_base_table_data(range_)
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=file.id)
            data.append(display_remove_link(url + '#tab-' + range_.table_name, range_.name))
        tabs[range_.table_name].table.rows.append(data)
    for link_ in file.get_links('P67', True):
        data = get_base_table_data(link_.domain)
        data.append(link_.description)
        if is_authorized('contributor'):
            update_url = url_for('reference_link_update', link_id=link_.id, origin_id=file.id)
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=file.id)
            data.append(display_remove_link(unlink_url + '#tab-reference', link_.domain.name))
        tabs['reference'].table.rows.append(data)
    return render_template('file/view.html',
                           missing_file=False if path else True,
                           entity=file,
                           info=get_entity_data(file),
                           tabs=tabs,
                           preview=True if path and preview_file(path) else False,
                           filename=os.path.basename(path) if path else False)


def save(form: FileForm, file: Optional[Entity] = None, origin: Optional[Entity] = None) -> str:
    g.cursor.execute('BEGIN')
    try:
        log_action = 'update'
        if not file:
            log_action = 'insert'
            file_ = request.files['file']
            file = Entity.insert('E31', form.name.data, 'file')
            # Add an 'a' to prevent emtpy filename
            filename = secure_filename('a' + file_.filename)  # type: ignore
            new_name = str(file.id) + '.' + filename.rsplit('.', 1)[1].lower()
            full_path = os.path.join(app.config['UPLOAD_FOLDER_PATH'], new_name)
            file_.save(full_path)
        file.update(form)
        url = url_for('entity_view', id_=file.id)
        if origin:
            if origin.system_type in ['edition', 'bibliography']:
                link_id = origin.link('P67', file)[0]
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            else:
                file.link('P67', origin)
                url = url_for('entity_view', id_=origin.id) + '#tab-file'
        g.cursor.execute('COMMIT')
        logger.log_user(file.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        openatlas.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('file_index', origin_id=origin.id if origin else None)
    return url
