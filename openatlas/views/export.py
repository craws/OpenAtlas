import os
from pathlib import Path

from flask import flash, g, render_template, send_from_directory, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import button, link, required_group
from openatlas.display.util2 import convert_size, is_authorized, manual
from openatlas.models.export import arche_export, sql_export


@app.route('/download/sql/<filename>')
@required_group('manager')
def download_sql(filename: str) -> Response:
    return send_from_directory(
        app.config['EXPORT_PATH'],
        filename,
        as_attachment=True)


@app.route('/export/execute/<format_>')
@required_group('manager')
def export_execute(format_: str) -> Response:
    if os.access(app.config['EXPORT_PATH'], os.W_OK):
        if sql_export(format_):
            g.logger.log('info', 'database', 'SQL export')
            flash(_('data was exported'), 'info')
        else:  # pragma: no cover
            g.logger.log('error', 'database', 'SQL export failed')
            flash(_('export failed'), 'error')
    return redirect(url_for('export_sql'))


@app.route('/export/sql')
@required_group('manager')
def export_sql() -> str:
    path = app.config['EXPORT_PATH']
    table = Table(['name', 'size'], order=[[0, 'desc']])
    for file in [
            f for f in path.iterdir()
            if (path / f).is_file() and f.name != '.gitignore']:
        data = [
            file.name,
            convert_size(file.stat().st_size),
            link(
                _('download'),
                url_for('download_sql', filename=file.name))]
        if is_authorized('admin') \
                and os.access(app.config['EXPORT_PATH'], os.W_OK):
            confirm = _('Delete %(name)s?', name=file.name.replace("'", ''))
            data.append(
                link(
                    _('delete'),
                    url_for('delete_export', filename=file.name),
                    js=f"return confirm('{confirm}')"))
        table.rows.append(data)
    return render_template(
        'tabs.html',
        tabs={
            'export': Tab(
                'export',
                _('export'),
                content=table.display(),
                buttons=[
                    manual('admin/export'),
                    button(
                        _('export SQL'),
                        url_for('export_execute', format_='sql')),
                    button(
                        _('export database dump'),
                        url_for('export_execute', format_='dump'))])},
        title=_('export SQL'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('export SQL')])


@app.route('/delete_export/<filename>')
@required_group('admin')
def delete_export(filename: str) -> Response:
    try:
        (app.config['EXPORT_PATH'] / filename).unlink()
        g.logger.log('info', 'file', 'SQL file deleted')
        flash(_('file deleted'), 'info')
    except Exception as e:
        g.logger.log('error', 'file', 'SQL file deletion failed', e)
        flash(_('error file delete'), 'error')
    return redirect(url_for('export_sql'))



@app.route('/export/arche')
@required_group('manager')
def export_arche() -> str:
    path = app.config['EXPORT_PATH']
    table = Table(['name', 'size'], order=[[0, 'desc']])
    for file in [
            f for f in path.iterdir()
            if (path / f).is_file() and f.name != '.gitignore']:
        if 'export' in file.name:
            continue
        data = [
            file.name,
            convert_size(file.stat().st_size),
            link(
                _('download'),
                url_for('download_sql', filename=file.name))]
        if is_authorized('admin') \
                and os.access(app.config['EXPORT_PATH'], os.W_OK):
            confirm = _('Delete %(name)s?', name=file.name.replace("'", ''))
            data.append(
                link(
                    _('delete'),
                    url_for('delete_export', filename=file.name),
                    js=f"return confirm('{confirm}')"))
        table.rows.append(data)
    return render_template(
        'tabs.html',
        tabs={
            'export': Tab(
                'export',
                _('export'),
                content=table.display(),
                buttons=[
                    manual('admin/export'),
                    button(
                         _('export') + ' ARCHE',
                        url_for('arche_execute')),
                    ])},
        title=_('export') + ' ARCHE',
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
             _('export') + ' ARCHE'])


@app.route('/export/arche/execute')
@required_group('admin')
def arche_execute() -> Response:
    if os.access(app.config['EXPORT_PATH'], os.W_OK):
        if sql_export('sql'):
            g.logger.log('info', 'database', 'SQL export')
            flash(_('data was exported'), 'info')
        else:  # pragma: no cover
            g.logger.log('error', 'database', 'SQL export failed')
            flash(_('export failed'), 'error')


    sql = get_latest_file(app.config['EXPORT_PATH'])
    arche_export(sql)

    return redirect(url_for('export_sql'))


def get_latest_file(directory: str) -> Path | None:
    path = Path(directory)
    files = [f for f in path.iterdir() if f.is_file()]
    return max(files, key=lambda f: f.stat().st_mtime, default=None)
