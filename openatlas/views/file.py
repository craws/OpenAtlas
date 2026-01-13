from pathlib import Path
from typing import Any, Optional

from flask import (
    abort, flash, g, render_template, request, send_from_directory, url_for)
from flask_babel import gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import entity_table
from openatlas.display.util import (
    check_iiif_activation, check_iiif_file_exist, convert_image_to_iiif,
    delete_iiif_image, required_group)
from openatlas.display.util2 import is_authorized
from openatlas.models.entity import Entity
from openatlas.models.settings import set_logo


@app.route('/download/<path:name>')
@required_group('readonly')
def download(name: str) -> Any:
    return send_from_directory(
        app.config['UPLOAD_PATH'],
        name,
        as_attachment=True)


@app.route('/display/<path:name>')
@required_group('readonly')
def display_file(name: str) -> Any:
    if size := request.args.get('size'):
        if not size.isdigit() or size not in app.config['IMAGE_SIZE'].values():
            abort(400)
        return send_from_directory(app.config['RESIZED_IMAGES'] / size, name)
    return send_from_directory(app.config['UPLOAD_PATH'], name)


@app.route('/display/custom_logo/<ext>')
def display_custom_logo(ext: str) -> Any:
    return send_from_directory(
        app.config['UPLOAD_PATH'],
        g.settings['logo_file_id'] + ext)


@app.route('/set_profile_image/<int:id_>/<int:origin_id>')
@required_group('contributor')
def set_profile_image(id_: int, origin_id: int) -> Response:
    Entity.set_profile_image(id_, origin_id)
    return redirect(url_for('view', id_=origin_id))


@app.route('/file/convert_iiif/<int:id_>')
@required_group('contributor')
def make_iiif_available(id_: int) -> Response:
    if convert_image_to_iiif(id_):
        flash(_('IIIF converted'))
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
            if file_.class_.group['name'] == 'file' \
                    and check_iiif_file_exist(file_.id):
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
    return redirect(f"{url_for('admin_index')}#tab-iiif")


def convert() -> None:
    if not check_iiif_activation():  # pragma: no cover
        flash(_('please activate IIIF'))
        return
    if not g.settings['iiif_conversion']:  # pragma: no cover
        flash(_('please activate IIIF conversion'))
        return
    existing_files = [entity.id for entity in Entity.get_by_class('file')]
    for id_, file_path in g.files.items():
        if check_iiif_file_exist(id_):
            continue
        if id_ in existing_files and file_path.suffix in g.display_file_ext:
            convert_image_to_iiif(id_)
    flash(_('all image files are converted'))


@app.route('/delete_iiif_file/<int:id_>')
@required_group('admin')
def delete_iiif_file(id_: int) -> Response:
    delete_iiif_image(id_)
    flash(_('IIIF file deleted'))
    return redirect(url_for('view', id_=id_))


@app.route('/delete_iiif_files')
@required_group('admin')
def delete_iiif_files() -> Response:
    delete_all_iiif_files()
    return redirect(f"{url_for('admin_index')}#tab-iiif")


def delete_all_iiif_files() -> None:
    if app.config['UPLOAD_PATH'].match(
            g.settings['iiif_path']):  # pragma: no cover
        flash(_('cannot delete images in upload directory'), 'warning')
        return
    for id_ in g.files:
        if check_iiif_file_exist(id_):
            delete_iiif_image(id_)
    flash(_('all IIIF files are deleted'))


@app.route('/logo/')
@app.route('/logo/<int:id_>')
@required_group('manager')
def logo(id_: Optional[int] = None) -> str | Response:
    if g.settings['logo_file_id']:
        abort(418)
    if id_:
        set_logo(id_)
        return redirect(f"{url_for('admin_index')}#tab-file")
    table = entity_table(
        Entity.get_display_files(),
        columns=['set_logo'] + g.class_groups['file']['table_columns'],
        forms={'mode': 'logo'})
    return render_template(
        'tabs.html',
        tabs={'logo': Tab('logo', table=table)},
        title=_('logo'),
        crumbs=[[_('admin'), f'{url_for('admin_index')}#tab-file'], _('logo')])


@app.route('/logo/remove')
@required_group('manager')
def logo_remove() -> Response:
    set_logo()
    return redirect(f"{url_for('admin_index')}#tab-file")


@app.route('/file/delete/<name>')
@required_group('editor')
def file_delete(name: str) -> Response:
    if name != 'all':  # Delete one file
        try:
            (app.config['UPLOAD_PATH'] / name).unlink()
            flash(f'{name} {_('was deleted')}')
        except Exception as e:
            g.logger.log('error', 'file', f'deletion of {name} failed', e)
            flash(_('error file delete'), 'error')
        return redirect(f'{url_for('check_files')}#tab-orphaned-files')

    # Delete all files with no corresponding entity
    if is_authorized('admin'):  # pragma: no cover - don't test, ever
        entity_file_ids = [entity.id for entity in Entity.get_by_class('file')]
        for f in app.config['UPLOAD_PATH'].iterdir():
            if f.name != '.gitignore' and int(f.stem) not in entity_file_ids:
                (app.config['UPLOAD_PATH'] / f.name).unlink()
    return redirect(
        f'{url_for('check_files')}#tab-orphaned-files')  # pragma: no cover


@app.route('/file/iiif/delete/<filename>')
@required_group('editor')
def file_iiif_delete(filename: str) -> Response:
    try:
        (Path(g.settings['iiif_path']) / filename).unlink()
        flash(f"{filename} {_('was deleted')}")
    except Exception as e:
        g.logger.log('error', 'file', f'deletion of IIIF {filename} failed', e)
        flash(_('error file delete'), 'error')
    return redirect(f"{url_for('check_files')}#tab-orphaned-iiif-files")
