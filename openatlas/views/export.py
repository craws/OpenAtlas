# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os
from os.path import basename
from typing import Union

from flask import flash, render_template, send_from_directory, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import BooleanField, SelectField, SubmitField

from openatlas import app, logger
from openatlas.models.export import Export
from openatlas.util.table import Table
from openatlas.util.util import convert_size, is_authorized, required_group, uc_first


class ExportSqlForm(FlaskForm):
    save = SubmitField(uc_first(_('export SQL')))


class ExportCsvForm(FlaskForm):
    zip = BooleanField(_('export as ZIP and add info file'), default=True)
    timestamps = BooleanField('created and modified dates', default=False)
    gis_format = SelectField(_('GIS format'), choices=[
        ('coordinates', _('coordinates')), ('wkt', 'WKT'), ('postgis', 'PostGIS Geometry')])
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


@app.route('/export/sql', methods=['POST', 'GET'])
@required_group('manager')
def export_sql() -> Union[str, Response]:
    path = app.config['EXPORT_FOLDER_PATH'] + '/sql'
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
    table = Table(['name', 'size'], order='[[0, "desc"]]')
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        name = basename(file)
        if name == '.gitignore':
            continue
        url = url_for('download_sql', filename=name)
        data = [name, convert_size(os.path.getsize(path + '/' + name)),
                '<a href="' + url + '">' + uc_first(_('download')) + '</a>']
        if is_authorized('admin') and writeable:
            confirm = ' onclick="return confirm(\'' + _('Delete %(name)s?', name=name) + '\')"'
            delete = '<a href="' + url_for('delete_sql', filename=name)
            delete += '" ' + confirm + '>' + uc_first(_('delete')) + '</a>'
            data.append(delete)
        table.rows.append(data)
    return render_template('export/export_sql.html', form=form, table=table, writeable=writeable)


@app.route('/download/sql/<filename>')
@required_group('manager')
def download_sql(filename: str):
    path = app.config['EXPORT_FOLDER_PATH'] + '/sql/'
    return send_from_directory(path, filename, as_attachment=True)


@app.route('/delete/sql/<filename>')
@required_group('admin')
def delete_sql(filename: str) -> Response:
    try:
        os.remove(app.config['EXPORT_FOLDER_PATH'] + '/sql/' + filename)
        logger.log('info', 'file', 'SQL file deleted')
        flash(_('file deleted'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'file', 'SQL file deletion failed', e)
        flash(_('error file delete'), 'error')
    return redirect(url_for('export_sql'))


@app.route('/download/csv/<filename>')
@required_group('manager')
def download_csv(filename: str):
    path = app.config['EXPORT_FOLDER_PATH'] + '/csv/'
    return send_from_directory(path, filename, as_attachment=True)


@app.route('/export/csv', methods=['POST', 'GET'])
@required_group('manager')
def export_csv() -> Union[str, Response]:
    path = app.config['EXPORT_FOLDER_PATH'] + '/csv'
    writeable = True if os.access(path, os.W_OK) else False
    form = ExportCsvForm()
    if form.validate_on_submit() and writeable:
        Export.export_csv(form)
        logger.log('info', 'database', 'CSV export')
        flash(_('data was exported as CSV'), 'info')
        return redirect(url_for('export_csv'))
    table = Table(['name', 'size'], order='[[0, "desc"]]')
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        name = basename(file)
        if name == '.gitignore':
            continue
        link = '<a href="{url}">{label}</a>'.format(url=url_for('download_csv', filename=name),
                                                    label=uc_first(_('download')))
        data = [name, convert_size(os.path.getsize(path + '/' + name)), link]
        if is_authorized('admin') and writeable:
            confirm = ' onclick="return confirm(\'' + _('Delete %(name)s?', name=name) + '\')"'
            delete = '<a href="' + url_for('delete_csv', filename=name)
            delete += '" ' + confirm + '>' + uc_first(_('delete')) + '</a>'
            data.append(delete)
        table.rows.append(data)
    return render_template('export/export_csv.html', form=form, table=table, writeable=writeable)


@app.route('/delete/csv/<filename>')
@required_group('admin')
def delete_csv(filename: str) -> Response:
    try:
        os.remove(app.config['EXPORT_FOLDER_PATH'] + '/csv/' + filename)
        logger.log('info', 'file', 'CSV file deleted')
        flash(_('file deleted'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'file', 'CSV deletion failed', e)
        flash(_('error file delete'), 'error')
    return redirect(url_for('export_csv'))
