import os
from pathlib import Path
from typing import Any, Union

from flask import flash, g, render_template, send_from_directory, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import SubmitField

from openatlas import app
from openatlas.models.export import sql_export
from openatlas.util.table import Table
from openatlas.util.util import (
    convert_size, delete_link, is_authorized, link, required_group, uc_first)


class ExportSqlForm(FlaskForm):
    save = SubmitField(uc_first(_('export SQL')))


@app.route('/download/sql/<filename>')
@required_group('manager')
def download_sql(filename: str) -> Response:
    return send_from_directory(
        app.config['EXPORT_DIR'] / 'sql',
        filename,
        as_attachment=True)


@app.route('/export/sql', methods=['POST', 'GET'])
@required_group('manager')
def export_sql() -> Union[str, Response]:
    path = app.config['EXPORT_DIR'] / 'sql'
    writable = os.access(path, os.W_OK)
    form = ExportSqlForm()
    if form.validate_on_submit() and writable:
        if sql_export():
            g.logger.log('info', 'database', 'SQL export')
            flash(_('data was exported as SQL'), 'info')
        else:  # pragma: no cover
            g.logger.log('error', 'database', 'SQL export failed')
            flash(_('SQL export failed'), 'error')
        return redirect(url_for('export_sql'))
    return render_template(
        'export.html',
        form=form,
        table=get_table('sql', path, writable),
        writable=writable,
        title=_('export SQL'),
        crumbs=[
            [_('admin'),
             f"{url_for('admin_index')}#tab-data"], _('export SQL')])


def get_table(type_: str, path: Path, writable: bool) -> Table:
    table = Table(['name', 'size'], order=[[0, 'desc']])
    for file in [
            f for f in path.iterdir()
            if (path / f).is_file() and f.name != '.gitignore']:
        data = [
            file.name,
            convert_size(file.stat().st_size),
            link(
                _('download'),
                url_for(f'download_{type_}', filename=file.name))]
        if is_authorized('admin') and writable:
            data.append(
                delete_link(
                    file.name,
                    url_for('delete_export', type_=type_, filename=file.name)))
        table.rows.append(data)
    return table


@app.route('/delete_export/<type_>/<filename>')
@required_group('admin')
def delete_export(type_: str, filename: str) -> Response:
    try:
        (app.config['EXPORT_DIR'] / type_ / filename).unlink()
        g.logger.log('info', 'file', f'{type_} file deleted')
        flash(_('file deleted'), 'info')
    except Exception as e:
        g.logger.log('error', 'file', f'{type_} file deletion failed', e)
        flash(_('error file delete'), 'error')
    return redirect(url_for(f'export_{type_}'))
