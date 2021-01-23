import os
from typing import Any, Optional, Union

from flask import flash, g, render_template, request, send_from_directory, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import Response

import openatlas
from openatlas import app, logger
from openatlas.forms.form import build_form, build_table_form
from openatlas.models.entity import Entity
from openatlas.util.display import link
from openatlas.util.util import required_group, was_modified


@app.route('/download/<path:filename>')
@required_group('readonly')
def download_file(filename: str) -> Any:
    return send_from_directory(app.config['UPLOAD_DIR'], filename, as_attachment=True)


@app.route('/display/<path:filename>')
@required_group('readonly')
def display_file(filename: str) -> Any:
    return send_from_directory(app.config['UPLOAD_DIR'], filename)


@app.route('/display_logo/<path:filename>')
def display_logo(filename: str) -> Any:  # File display function for public
    return send_from_directory(app.config['UPLOAD_DIR'], filename)


@app.route('/file/set_as_profile_image/<int:id_>/<int:origin_id>')
def set_profile_image(id_: int, origin_id: int) -> Response:
    Entity.set_profile_image(id_, origin_id)
    return redirect(url_for('entity_view', id_=origin_id))


@app.route('/file/set_as_profile_image/<int:entity_id>')
def file_remove_profile_image(entity_id: int) -> Response:
    entity = Entity.get_by_id(entity_id)
    entity.remove_profile_image()
    return redirect(url_for('entity_view', id_=entity.id))


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
    form = build_form('file', file_)
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
    form = build_form('file')
    if form.validate_on_submit():
        return redirect(save(form, origin=origin))
    writeable = True if os.access(app.config['UPLOAD_DIR'], os.W_OK) else False
    return render_template('file/insert.html', form=form, origin=origin, writeable=writeable)


def save(form: FlaskForm, file: Optional[Entity] = None, origin: Optional[Entity] = None) -> str:
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
            file_.save(str(app.config['UPLOAD_DIR'] / new_name))
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
