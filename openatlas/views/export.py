import os
from pathlib import Path
from typing import Any, Union

from flask import flash, render_template, send_from_directory, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import BooleanField, SelectField, SubmitField

from openatlas import app, logger
from openatlas.models.export import Export
from openatlas.util.table import Table
from openatlas.util.util import (
    convert_size, delete_link, is_authorized, link, required_group, uc_first)


class ExportSqlForm(FlaskForm):  # type: ignore
    save = SubmitField(uc_first(_('export SQL')))


class ExportCsvForm(FlaskForm):  # type: ignore
    zip = BooleanField(_('export as ZIP and add info file'), default=True)
    timestamps = BooleanField('created and modified dates', default=False)
    gis_format = SelectField(
        _('GIS format'),
        choices=[
            ('coordinates', _('coordinates')),
            ('wkt', 'WKT'),
            ('postgis', 'PostGIS Geometry')])
    model_class = BooleanField('model.class', default=True)
    model_class_inheritance = BooleanField('model.class_inheritance', default=True)
    model_entity = BooleanField('model.entity', default=True)
    model_link = BooleanField('model.link', default=True)
    model_property = BooleanField('model.property', default=True)
    model_property_inheritance = BooleanField('model.property_inheritance', default=True)
    gis_point = BooleanField('gis.point', default=True)
    gis_linestring = BooleanField('gis.linestring', default=True)
    gis_polygon = BooleanField('gis.polygon', default=True)
    save = SubmitField(uc_first(_('export CSV')))


@app.route('/download/sql/<filename>')
@required_group('manager')
def download_sql(filename: str) -> Response:
    return send_from_directory(app.config['EXPORT_DIR'] / 'sql', filename, as_attachment=True)


@app.route('/download/csv/<filename>')
@required_group('manager')
def download_csv(filename: str) -> Any:
    return send_from_directory(app.config['EXPORT_DIR'] / 'csv', filename, as_attachment=True)


@app.route('/export/sql', methods=['POST', 'GET'])
@required_group('manager')
def export_sql() -> Union[str, Response]:
    path = app.config['EXPORT_DIR'] / 'sql'
    writeable = True if os.access(path, os.W_OK) else False
    form = ExportSqlForm()
    if form.validate_on_submit() and writeable:
        if Export.export_sql():
            logger.log('info', 'database', 'SQL export')
            flash(_('data was exported as SQL'), 'info')
        else:  # pragma: no cover
            logger.log('error', 'database', 'SQL export failed')
            flash(_('SQL export failed'), 'error')
        return redirect(url_for('export_sql'))
    return render_template(
        'export.html',
        form=form,
        table=get_table('sql', path, writeable),
        writeable=writeable,
        title=_('export SQL'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-data"], _('export SQL')])


@app.route('/export/csv', methods=['POST', 'GET'])
@required_group('manager')
def export_csv() -> Union[str, Response]:
    path = app.config['EXPORT_DIR'] / 'csv'
    writeable = True if os.access(path, os.W_OK) else False
    form = ExportCsvForm()
    if form.validate_on_submit() and writeable:
        Export.export_csv(form)
        logger.log('info', 'database', 'CSV export')
        flash(_('data was exported as CSV'), 'info')
        return redirect(url_for('export_csv'))
    return render_template(
        'export.html',
        form=form,
        table=get_table('csv', path, writeable),
        writeable=writeable,
        title=_('export CSV'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-data"], _('export CSV')])


def get_table(type_: str, path: Path, writeable: bool) -> Table:
    table = Table(['name', 'size'], order=[[0, 'desc']])
    for file in [f for f in path.iterdir() if (path / f).is_file() and f.name != '.gitignore']:
        data = [
            file.name,
            convert_size(file.stat().st_size),
            link(_('download'), url_for(f'download_{type_}', filename=file.name))]
        if is_authorized('admin') and writeable:
            data.append(
                delete_link(file.name, url_for('delete_export', type_=type_, filename=file.name)))
        table.rows.append(data)
    return table


@app.route('/delete_export/<type_>/<filename>')
@required_group('admin')
def delete_export(type_: str, filename: str) -> Response:
    try:
        (app.config['EXPORT_DIR'] / type_ / filename).unlink()
        logger.log('info', 'file', f'{type_} file deleted')
        flash(_('file deleted'), 'info')
    except Exception as e:
        logger.log('error', 'file', f'{type_} file deletion failed', e)
        flash(_('error file delete'), 'error')
    return redirect(url_for(f'export_{type_}'))
