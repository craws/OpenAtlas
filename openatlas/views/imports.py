# Created by Alexander Watzinger and others. Please see README.md for licensing information
import collections
import os
from typing import Union, Optional

import pandas as pd
from flask import flash, g, render_template, request, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import Response
from wtforms import BooleanField, FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.models.entity import EntityMapper
from openatlas.models.imports import ImportMapper, Project
from openatlas.util.table import Table
from openatlas.util.util import format_date, is_float, link, required_group, truncate_string


class ProjectForm(FlaskForm):
    project_id: Optional[int] = None
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))

    def validate(self) -> bool:
        valid = FlaskForm.validate(self)
        project = ImportMapper.get_project_by_id(self.project_id) if self.project_id else Project()
        if project.name != self.name.data and ImportMapper.get_project_by_name(self.name.data):
            self.name.errors.append(_('error name exists'))
            valid = False
        return valid


@app.route('/import/index')
@required_group('contributor')
def import_index() -> str:
    table = Table([_('project'), _('entities'), _('description')])
    for project in ImportMapper.get_all_projects():
        table.rows.append([link(project),
                           format_number(project.count),
                           truncate_string(project.description)])
    return render_template('import/index.html', table=table)


@app.route('/import/project/insert', methods=['POST', 'GET'])
@required_group('manager')
def import_project_insert() -> Union[str, Response]:
    form = ProjectForm()
    if form.validate_on_submit():
        id_ = ImportMapper.insert_project(form.name.data, form.description.data)
        flash(_('project inserted'), 'info')
        return redirect(url_for('import_project_view', id_=id_))
    return render_template('import/project_insert.html', form=form)


@app.route('/import/project/view/<int:id_>')
@required_group('contributor')
def import_project_view(id_: int) -> str:
    table = Table([_('name'), _('class'), _('description'), 'origin ID', _('date')])
    for entity in EntityMapper.get_by_project_id(id_):
        table.rows.append([link(entity),
                           entity.class_.name,
                           truncate_string(entity.description),
                           entity.origin_id,
                           format_date(entity.created)])
    project = ImportMapper.get_project_by_id(id_)
    return render_template('import/project_view.html', project=project, table=table)


@app.route('/import/project/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def import_project_update(id_: int) -> Union[str, Response]:
    project = ImportMapper.get_project_by_id(id_)
    form = ProjectForm(obj=project)
    form.project_id = id_
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        ImportMapper.update_project(project)
        flash(_('project updated'), 'info')
        return redirect(url_for('import_project_view', id_=project.id))
    return render_template('import/project_update.html', project=project, form=form)


@app.route('/import/project/delete/<int:id_>')
@required_group('manager')
def import_project_delete(id_: int) -> Response:
    ImportMapper.delete_project(id_)
    flash(_('project deleted'), 'info')
    return redirect(url_for('import_index'))


class ImportForm(FlaskForm):
    file = FileField(_('file'), [InputRequired()])
    preview = BooleanField(_('preview only'), default=True)
    duplicate = BooleanField(_('check for duplicates'), default=True)
    save = SubmitField(_('import'))

    def validate(self) -> bool:
        valid = FlaskForm.validate(self)
        file_ = request.files['file']
        extensions = app.config['IMPORT_FILE_EXTENSIONS']
        if not file_:  # pragma: no cover
            self.file.errors.append(_('no file to upload'))
            valid = False
        elif not ('.' in file_.filename and file_.filename.rsplit('.', 1)[1].lower() in extensions):
            self.file.errors.append(_('file type not allowed'))
            valid = False
        return valid


@app.route('/import/data/<int:project_id>/<class_code>', methods=['POST', 'GET'])
@required_group('manager')
def import_data(project_id: int, class_code: str) -> str:
    project = ImportMapper.get_project_by_id(project_id)
    form = ImportForm()
    table = None
    imported = False
    messages: dict = {'error': [], 'warn': []}
    if form.validate_on_submit():
        file_ = request.files['file']
        # TODO fix windows separator
        separator = '/' if os.name == "posix" else '\\'
        file_path = app.config['IMPORT_FOLDER_PATH'] + separator + secure_filename(file_.filename)
        columns: dict = {'allowed': ['name', 'id', 'description'], 'valid': [], 'invalid': []}
        if class_code == 'E18':
            columns['allowed'] += ['easting', 'northing']
        try:
            file_.save(file_path)
            if file_path.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']:
                df = pd.read_excel(file_path, keep_default_na=False)
            else:
                df = pd.read_csv(file_path, keep_default_na=False)
            headers = list(df.columns.values)
            if 'name' not in headers:  # pragma: no cover
                messages['error'].append(_('missing name column'))
                raise Exception()
            for item in headers:  # pragma: no cover
                if item not in columns['allowed']:
                    columns['invalid'].append(item)
                    del df[item]
            if columns['invalid']:  # pragma: no cover
                messages['warn'].append(_('invalid columns') + ': ' + ','.join(columns['invalid']))
            headers = list(df.columns.values)  # Read cleaned headers again
            table_data = []
            checked_data = []
            origin_ids = []
            names = []
            missing_name_count = 0
            for index, row in df.iterrows():
                if not row['name']:  # pragma: no cover
                    missing_name_count += 1
                    continue
                table_row = []
                checked_row = {}
                for item in headers:
                    value = row[item]
                    if item in ['northing', 'easting'] and not is_float(row[item]):
                        value = '<span class="error">' + row[item] + '</span>'  # pragma: no cover
                    table_row.append(value)
                    checked_row[item] = row[item]
                    if item == 'name' and form.duplicate.data:
                        names.append(row['name'].lower())
                    if item == 'id' and row[item]:
                        origin_ids.append(str(row['id']))
                table_data.append(table_row)
                checked_data.append(checked_row)
            table = Table(headers, rows=table_data)

            # Checking for data inconsistency
            if missing_name_count:  # pragma: no cover
                messages['warn'].append(_('empty names') + ': ' + str(missing_name_count))
            doubles = [item for item, count in collections.Counter(origin_ids).items() if count > 1]
            if doubles:  # pragma: no cover
                messages['error'].append(_('double IDs in import') + ': ' + ', '.join(doubles))
            existing = ImportMapper.check_origin_ids(project, origin_ids) if origin_ids else None
            if existing:
                messages['error'].append(_('IDs already in database') + ': ' + ', '.join(existing))
            if form.duplicate.data:  # Check for possible duplicates
                duplicates = ImportMapper.check_duplicates(class_code, names)
                if duplicates:  # pragma: no cover
                    messages['warn'].append(_('possible duplicates') + ': ' + ', '.join(duplicates))
            if messages['error']:
                raise Exception()
        except Exception as e:  # pragma: no cover
            flash(_('error at import'), 'error')
            return render_template('import/import_data.html', project=project, form=form,
                                   class_code=class_code, messages=messages)

        if not form.preview.data and checked_data:
            g.cursor.execute('BEGIN')
            try:
                ImportMapper.import_data(project, class_code, checked_data)
                g.cursor.execute('COMMIT')
                logger.log('info', 'import', 'import: ' + str(len(checked_data)))
                flash(_('import of') + ': ' + str(len(checked_data)), 'info')
                imported = True
            except Exception as e:  # pragma: no cover
                g.cursor.execute('ROLLBACK')
                logger.log('error', 'import', 'import failed', e)
                flash(_('error transaction'), 'error')
    return render_template('import/import_data.html', project=project, form=form,
                           class_code=class_code, table=table, imported=imported, messages=messages)
