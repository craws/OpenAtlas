import os

from flask import flash, g, render_template, send_from_directory, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import button, display_info, link, required_group
from openatlas.display.util2 import convert_size, is_authorized, manual
from openatlas.models.export import arche_export, rdf_export, sql_export


@app.route('/download/export/<filename>')
@required_group('manager')
def download_export(filename: str) -> Response:
    return send_from_directory(
        app.config['EXPORT_PATH'],
        filename,
        as_attachment=True)


@app.route('/download/export/arche/<filename>')
@required_group('manager')
def download_arche_export(filename: str) -> Response:
    return send_from_directory(
        app.config['ARCHE_PATH'],
        filename,
        as_attachment=True)


@app.route('/delete_export/<view>/<filename>')
@required_group('admin')
def delete_export(view: str, filename: str) -> Response:
    path = app.config['EXPORT_PATH']
    if view == 'export_arche':
        path = app.config['ARCHE_PATH']
    if view == 'export_rdf':
        path = app.config['RDF_PATH']
    try:
        (path / filename).unlink()
        g.logger.log('info', 'file', 'SQL file deleted')
        flash(_('file deleted'), 'info')
    except Exception as e:
        g.logger.log('error', 'file', 'SQL file deletion failed', e)
        flash(_('error file delete'), 'error')
    return redirect(url_for(view, _anchor='tab-export'))


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
                url_for('download_export', filename=file.name))]
        if is_authorized('admin') \
                and os.access(app.config['EXPORT_PATH'], os.W_OK):
            confirm = _('Delete %(name)s?', name=file.name.replace("'", ''))
            data.append(
                link(
                    _('delete'),
                    url_for(
                        'delete_export',
                        view='export_sql',
                        filename=file.name),
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


@app.route('/export/arche')
@required_group('manager')
def export_arche() -> str:
    path = app.config['ARCHE_PATH']
    table = Table(['name', 'size'], order=[[0, 'desc']])
    for file in path.iterdir():
        if (not file.is_file()
                or file.name == '.gitignore'
                or 'export' in file.name):
            continue
        data = [
            file.name,
            convert_size(file.stat().st_size),
            link(
                _('download'),
                url_for('download_arche_export', filename=file.name))]
        if is_authorized('admin') and os.access(path, os.W_OK):
            confirm = _('Delete %(name)s?', name=file.name.replace("'", ''))
            data.append(
                link(
                    _('delete'),
                    url_for(
                        'delete_export',
                        view='export_arche',
                        filename=file.name),
                    js=f"return confirm('{confirm}')"))
        table.rows.append(data)
    metadata = app.config['ARCHE_METADATA']
    info_content = {
        'topCollection': metadata.get('topCollection'),
        'language': metadata.get('language'),
        'depositor': ', '.join(metadata.get('depositor', [])),
        'acceptedDate': metadata.get('acceptedDate'),
        'curator': ', '.join(metadata.get('curator', [])),
        'principalInvestigator':
            ', '.join(metadata.get('principalInvestigator', [])),
        'hasMetadataCreator':
            ', '.join(metadata.get('hasMetadataCreator', [])),
        'relatedDiscipline': ', '.join(
            metadata.get('relatedDiscipline', [])),
        'excludeReferenceSystems':
            ', '.join(metadata.get('excludeReferenceSystems', [])),
        'typeIds':
            ', '.join(
                [link(str(type_id), url_for('view', id_=type_id))
                 for type_id in metadata.get('typeIds', [])])}
    return render_template(
        'tabs.html',
        tabs={
            'info': Tab(
                'info',
                content=display_info(info_content),
                buttons=[manual('admin/export'),
                         button(
                             'ARCHE ' + _('file checker'),
                             url_for('check_files', arche='arche'))]),
            'export': Tab(
                'export',
                _('export'),
                content=table.display(),
                buttons=[
                    manual('admin/export'),
                    button(
                        _('export') + ' ARCHE',
                        url_for('arche_execute'))
                ])},
        title=_('export') + ' ARCHE',
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('export') + ' ARCHE'])


@app.route('/export/arche/execute')
@required_group('admin')
def arche_execute() -> Response:
    if os.access(app.config['ARCHE_PATH'], os.W_OK):
        if arche_export():
            g.logger.log('info', 'database', 'ARCHE export')
            flash(_('data was exported'), 'info')
        else:  # pragma: no cover
            g.logger.log('error', 'database', 'ARCHE export failed')
            flash(_('export failed'), 'error')
    return redirect(url_for('export_arche', _anchor='tab-export'))


@app.route('/export/rdf')
@required_group('manager')
def export_rdf() -> str:
    path = app.config['RDF_PATH']
    table = Table(['name', 'size'], order=[[0, 'desc']])
    for file in path.iterdir():
        if (not file.is_file()
                or file.name == '.gitignore'
                or 'export' in file.name):
            continue
        data = [
            file.name,
            convert_size(file.stat().st_size),
            link(
                _('download'),
                url_for('download_rdf_export', filename=file.name))]
        if is_authorized('admin') and os.access(path, os.W_OK):
            confirm = _('Delete %(name)s?', name=file.name.replace("'", ''))
            data.append(
                link(
                    _('delete'),
                    url_for(
                        'delete_export',
                        view='export_rdf',
                        filename=file.name),
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
                        _('export') + ' turtle',
                        url_for('rdf_execute', format_='turtle'))
                ])},
        title=_('export') + ' RDF',
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('export') + ' RDF'])


@app.route('/export/rdf/execute/<format_>')
@required_group('admin')
def rdf_execute(format_: str) -> Response:
    if format_ not in app.config['RDF_FORMATS']:
        g.logger.log('error', 'export', 'Wrong RDF format for export')
        flash(_('export failed'), 'error')
        return redirect(url_for('export_arche', _anchor='tab-export'))
    if os.access(app.config['RDF_PATH'], os.W_OK):
        if rdf_export(format_):
            g.logger.log('info', 'database', 'RDF export')
            flash(_('data was exported'), 'info')
        else:  # pragma: no cover
            g.logger.log('error', 'database', 'RDF export failed')
            flash(_('export failed'), 'error')
    return redirect(url_for('export_arche', _anchor='tab-export'))
