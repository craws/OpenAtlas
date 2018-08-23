# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os
from os.path import basename

from flask import flash, render_template, url_for, send_from_directory
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import BooleanField, SubmitField

from openatlas import app, logger
from openatlas.models.export import Export
from openatlas.util.util import (convert_size, required_group, uc_first, is_authorized)


class ExportSqlForm(Form):
    save = SubmitField(uc_first(_('export SQL')))


class ExportCsvForm(Form):
    model_class = BooleanField('model.class', default=True)
    model_class_inheritance = BooleanField('model.class_inheritance', default=True)
    model_entity = BooleanField('model.entity', default=True)
    model_link = BooleanField('model.link', default=True)
    model_link_property = BooleanField('model.link_property', default=True)
    model_property = BooleanField('model.property', default=True)
    model_property_inheritance = BooleanField('model.property_inheritance', default=True)
    gis_point = BooleanField('gis.point', default=True)
    gis_polygon = BooleanField('gis.polygon', default=True)
    save = SubmitField(uc_first(_('export CSV')))


@app.route('/admin/export/sql', methods=['POST', 'GET'])
@required_group('manager')
def admin_export_sql():
    table = {'id': 'sql', 'header': ['name', 'size'], 'data': [],
             'sort': 'sortList: [[0, 1]],headers: {0: { sorter: "text" }}'}
    path = app.config['EXPORT_FOLDER_PATH'] + '/sql'
    writeable = True if os.access(path, os.W_OK) else False
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        name = basename(file)
        file_path = path + '/' + name
        if name == '.gitignore':
            continue
        data = [
            name, convert_size(os.path.getsize(file_path)),
            '<a href="' + url_for('download_sql', filename=name) + '">' + uc_first(
                _('download')) + '</a>']
        if is_authorized('admin') and writeable:
            confirm = ' onclick="return confirm(\'' + _('Delete %(name)s?', name=name) + '\')"'
            delete = '<a href="' + url_for('delete_sql',
                                           filename=name) + '" ' + confirm + '>Delete</a>'
            data.append(delete)
        table['data'].append(data)
    form = ExportSqlForm()
    if form.validate_on_submit() and writeable:
        if Export.export_sql():
            logger.log('info', 'database', 'SQL export')
            flash(_('data was exported as SQL'), 'info')
        else:
            logger.log('error', 'database', 'SQL export failed')
            flash(_('SQL export failed'), 'error')
        return redirect(url_for('admin_export_sql'))
    return render_template('export/export_sql.html', form=form, table=table, writeable=writeable)


@app.route('/download/sql/<filename>')
@required_group('manager')
def download_sql(filename):
    path = app.config['EXPORT_FOLDER_PATH'] + '/sql/'
    return send_from_directory(path, filename, as_attachment=True)


@app.route('/delete/sql/<filename>')
@required_group('admin')
def delete_sql(filename):
    try:
        os.remove(app.config['EXPORT_FOLDER_PATH'] + '/sql/' + filename)
        logger.log('info', 'file', 'SQL file deleted')
        flash(_('file deleted'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'file', 'SQL file deletion failed', e)
        flash(_('error file delete'), 'error')
    return redirect(url_for('admin_export_sql'))


@app.route('/download/csv/<filename>')
@required_group('manager')
def download_csv(filename):
    path = app.config['EXPORT_FOLDER_PATH'] + '/csv/'
    return send_from_directory(path, filename, as_attachment=True)


@app.route('/admin/export/csv', methods=['POST', 'GET'])
@required_group('manager')
def admin_export_csv():
    table = {'id': 'sql', 'header': ['name', 'size'], 'data': [],
             'sort': 'sortList: [[0, 1]],headers: {0: { sorter: "text" }}'}
    path = app.config['EXPORT_FOLDER_PATH'] + '/csv'
    writeable = True if os.access(path, os.W_OK) else False
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        name = basename(file)
        file_path = path + '/' + name
        if name == '.gitignore':
            continue
        data = [
            name, convert_size(os.path.getsize(file_path)),
            '<a href="' + url_for('download_csv', filename=name) + '">' + uc_first(
                _('download')) + '</a>']
        if is_authorized('admin') and writeable:
            confirm = ' onclick="return confirm(\'' + _('Delete %(name)s?', name=name) + '\')"'
            delete = '<a href="' + url_for('delete_csv',
                                           filename=name) + '" ' + confirm + '>Delete</a>'
            data.append(delete)
        table['data'].append(data)
    form = ExportCsvForm()
    if form.validate_on_submit() and writeable:
        Export.export_csv(form)
        logger.log('info', 'database', 'CSV export')
        flash(_('data was exported as CSV'), 'info')
        return redirect(url_for('admin_export_csv'))
    return render_template('export/export_csv.html', form=form, table=table, writeable=writeable)


@app.route('/delete/csv/<filename>')
@required_group('admin')
def delete_csv(filename):
    try:
        os.remove(app.config['EXPORT_FOLDER_PATH'] + '/csv/' + filename)
        logger.log('info', 'file', 'CSV file deleted')
        flash(_('file deleted'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'file', 'CSV deletion failed', e)
        flash(_('error file delete'), 'error')
    return redirect(url_for('admin_export_csv'))
