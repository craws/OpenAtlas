from datetime import datetime
from typing import Any, Optional

from flask import (
    abort, flash, g, render_template, request, send_from_directory, url_for)
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    button, check_iiif_activation, check_iiif_file_exist,
    convert_image_to_iiif, delete_iiif_image, display_info, link,
    required_group)
from openatlas.display.util2 import format_date, is_authorized, manual
from openatlas.forms.form import get_table_form
from openatlas.forms.setting import FileForm, IiifForm
from openatlas.forms.util import get_form_settings
from openatlas.models.entity import Entity
from openatlas.models.settings import Settings
from openatlas.views.admin import (
    count_files_to_convert, count_files_to_delete, get_disk_space_info)


@app.route('/file')
@required_group('readonly')
def file_index() -> str:
    tabs = {
        'settings': Tab(
            'settings',
            content=render_template(
                'file.html',
                info=get_form_settings(FileForm()),
                disk_space_info=get_disk_space_info()),
            buttons=[
                manual('entity/file'),
                button(_('edit'), url_for('settings', category='file'))
                if is_authorized('manager') else '',
                button(_('list'), url_for('index', view='file')),
                button(_('file'), url_for('insert', class_='file'))
                if is_authorized('contributor') else ''])}
    if is_authorized('admin'):
        tabs['IIIF'] = Tab(
            'IIIF',
            content=display_info(get_form_settings(IiifForm())),
            buttons=[
                manual('admin/iiif'),
                button(_('edit'), url_for('settings', category='iiif')),
                button(
                    _('convert all files') + f' ({count_files_to_convert()})',
                    url_for('convert_iiif_files')),
                button(
                    _('delete all IIIF files') +
                    f' ({count_files_to_delete()})',
                    url_for('delete_iiif_files'))])
    return render_template(
        'tabs.html',
        title=_('file'),
        tabs=tabs,
        crumbs=[_('file')])


@app.route('/download/<path:filename>')
@required_group('readonly')
def download(filename: str) -> Any:
    return send_from_directory(
        app.config['UPLOAD_PATH'],
        filename,
        as_attachment=True)


@app.route('/display/<path:filename>')
@required_group('readonly')
def display_file(filename: str) -> Any:
    if request.args.get('size'):
        return send_from_directory(
            app.config['RESIZED_IMAGES'] / request.args.get('size'),
            filename)
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/display_logo/<path:filename>')
def display_logo(filename: str) -> Any:
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/set_profile_image/<int:id_>/<int:origin_id>')
@required_group('contributor')
def set_profile_image(id_: int, origin_id: int) -> Response:
    Entity.set_profile_image(id_, origin_id)
    return redirect(url_for('view', id_=origin_id))


@app.route('/remove_profile_image/<int:entity_id>')
@required_group('contributor')
def remove_profile_image(entity_id: int) -> Response:
    entity = Entity.get_by_id(entity_id)
    entity.remove_profile_image()
    return redirect(url_for('view', id_=entity.id))


@app.route('/file/add/<int:id_>/<view>', methods=['GET', 'POST'])
@required_group('contributor')
def file_add(id_: int, view: str) -> str | Response:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string('P67', request.form['checkbox_values'])
        return redirect(f"{url_for('view', id_=entity.id)}#tab-{view}")
    return render_template(
        'content.html',
        content=get_table_form(
            g.class_groups[view]['classes'],
            [e.id for e in entity.get_linked_entities('P67')]),
        title=entity.name,
        crumbs=[link(entity, index=True), entity, f"{_('link')} {_(view)}"])


@app.route('/file/convert_iiif/<int:id_>')
@required_group('contributor')
def make_iiif_available(id_: int) -> Response:
    if convert_image_to_iiif(id_):
        flash(_('IIIF converted'), 'info')
    else:
        flash(_('failed to convert image'), 'error')  # pragma: no cover
    return redirect(url_for('view', id_=id_))


@app.route('/view_iiif/<int:id_>')
@required_group('readonly')
def view_iiif(id_: int) -> str:
    entity = Entity.get_by_id(id_)
    manifests = []
    if entity.class_.group['name'] == 'file' and check_iiif_file_exist(id_):
        manifests.append(get_manifest_url(id_))
    else:
        for file_ in entity.get_linked_entities('P67', inverse=True):
            if file_.class_.group['name'] == 'file' and check_iiif_file_exist(file_.id):
                manifests.append(get_manifest_url(file_.id))
    return render_template('iiif.html', manifests=manifests)


def get_manifest_url(id_: int) -> str:
    return url_for(
        'api.iiif_manifest',
        id_=id_,
        version=g.settings['iiif_version'],
        _external=True)


@app.route('/convert_iiif_files')
@required_group('admin')
def convert_iiif_files() -> Response:
    convert()
    return redirect(url_for('file_index') + '#tab-IIIF')


def convert() -> None:
    if not check_iiif_activation():  # pragma: no cover
        flash(_('please activate IIIF'), 'info')
        return
    if not g.settings['iiif_conversion']:  # pragma: no cover
        flash(_('please activate IIIF conversion'), 'info')
        return
    existing_files = [entity.id for entity in Entity.get_by_class('file')]
    for id_, file_path in g.files.items():
        if check_iiif_file_exist(id_):
            continue
        if id_ in existing_files and file_path.suffix in g.display_file_ext:
            convert_image_to_iiif(id_)
    flash(_('all image files are converted'), 'info')


@app.route('/delete_iiif_file/<int:id_>')
@required_group('admin')
def delete_iiif_file(id_: int) -> Response:
    delete_iiif_image(id_)
    flash(_('IIIF file deleted'), 'info')
    return redirect(url_for('view', id_=id_))


@app.route('/delete_iiif_files')
@required_group('admin')
def delete_iiif_files() -> Response:
    delete_all_iiif_files()
    return redirect(url_for('file_index') + '#tab-IIIF')


def delete_all_iiif_files() -> None:
    if app.config['UPLOAD_PATH'].match(
            g.settings['iiif_path']):  # pragma: no cover
        flash(_('cannot delete images in upload directory'), 'warning')
        return
    for id_ in g.files:
        if check_iiif_file_exist(id_):
            delete_iiif_image(id_)
    flash(_('all IIIF files are deleted'), 'info')


@app.route('/logo/')
@app.route('/logo/<int:id_>')
@required_group('manager')
def logo(id_: Optional[int] = None) -> str | Response:
    if g.settings['logo_file_id']:
        abort(418)  # pragma: no cover - logo already set
    if id_:
        Settings.set_logo(id_)
        return redirect(url_for('file_index'))
    entities = Entity.get_display_files()
    table = Table(
        [''] + entities[0].class_.group['table_columns']
        if entities else [] + ['date'])
    for entity in Entity.get_display_files():
        date = 'N/A'
        if entity.id in g.files:
            date = format_date(
                datetime.fromtimestamp(g.files[entity.id].stat().st_ctime))
        table.rows.append([
            link(_('set'), url_for('logo', id_=entity.id)),
            entity.name,
            link(entity.standard_type),
            _('yes') if entity.public else None,
            entity.creator,
            entity.license_holder,
            entity.get_file_size(),
            entity.get_file_ext(),
            entity.description,
            date])
    return render_template(
        'tabs.html',
        tabs={'logo': Tab('logo', table=table)},
        title=_('logo'),
        crumbs=[[_('file'), url_for('file_index')], _('logo')])


@app.route('/logo/remove')
@required_group('manager')
def logo_remove() -> Response:
    Settings.set_logo()
    return redirect(url_for('file_index'))
