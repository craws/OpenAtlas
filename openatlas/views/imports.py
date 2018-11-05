# Created by Alexander Watzinger and others. Please see README.md for licensing information

import collections
import pandas as pd
from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect, secure_filename
from wtforms import BooleanField, FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.models.entity import EntityMapper
from openatlas.models.imports import ImportMapper, Project
from openatlas.util.util import format_date, link, required_group, truncate_string


class ProjectForm(Form):
    project_id = None
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))

    def validate(self, extra_validators=None):
        valid = Form.validate(self)
        project = ImportMapper.get_project_by_id(self.project_id) if self.project_id else Project()
        if project.name != self.name.data and ImportMapper.get_project_by_name(self.name.data):
            self.name.errors.append(str(_('error name exists')))
            valid = False
        return valid


@app.route('/import/index')
@required_group('editor')
def import_index():
    table = {'id': 'project', 'header': [_('project'), _('entities'), _('description')], 'data': []}
    for project in ImportMapper.get_all_projects():
        table['data'].append([
            link(project),
            project.count,
            truncate_string(project.description)])
    return render_template('import/index.html', table=table)


@app.route('/import/project/insert', methods=['POST', 'GET'])
@required_group('manager')
def import_project_insert():
    form = ProjectForm()
    if form.validate_on_submit():
        id_ = ImportMapper.insert_project(form.name.data, form.description.data)
        flash(_('project inserted'), 'info')
        return redirect(url_for('import_project_view', id_=id_))
    return render_template('import/project_insert.html', form=form)


@app.route('/import/project/view/<int:id_>')
@required_group('editor')
def import_project_view(id_):
    project = ImportMapper.get_project_by_id(id_)
    table = {'id': 'entities', 'data': [],
             'header': [_('name'), _('class'), _('description'), _('origin id'), _('date')]}
    for entity in EntityMapper.get_by_project_id(id_):
        table['data'].append([
            link(entity),
            entity.class_.name,
            truncate_string(entity.description),
            entity.origin_id,
            format_date(entity.created)])
    return render_template('import/project_view.html', project=project, table=table)


@app.route('/import/project/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def import_project_update(id_):
    project = ImportMapper.get_project_by_id(id_)
    form = ProjectForm(obj=project)
    form.project_id = id_
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        ImportMapper.update_project(project)
        flash(_('Project updated'), 'info')
        return redirect(url_for('import_project_view', id_=project.id))
    return render_template('import/project_update.html', project=project, form=form)


@app.route('/import/project/delete/<int:id_>')
@required_group('manager')
def import_project_delete(id_):
    ImportMapper.delete_project(id_)
    flash(_('Project deleted'), 'info')
    return redirect(url_for('import_index'))


class ImportForm(Form):
    file = FileField(_('file'), [InputRequired()])
    preview = BooleanField(_('preview only'), default=True)
    save = SubmitField(_('import'))


@app.route('/import/data/<int:project_id>/<class_code>', methods=['POST', 'GET'])
@required_group('manager')
def import_data(project_id, class_code):
    project = ImportMapper.get_project_by_id(project_id)
    form = ImportForm()
    imported = None
    table = None
    columns = {'allowed': ['name', 'id', 'description'], 'valid': [], 'invalid': []}
    if form.validate_on_submit():
        file_ = request.files['file']
        extensions = ['csv', 'xls', 'xlsx']
        if not file_:  # pragma: no cover
            flash(_('no file to upload'), 'error')
        elif not ('.' in file_.filename and file_.filename.rsplit('.', 1)[1].lower() in extensions):
            flash(_('file type not allowed'), 'error')
        else:
            filename = secure_filename(file_.filename)
            file_path = app.config['IMPORT_FOLDER_PATH'] + '/' + filename
            try:
                file_.save(file_path)
                if filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']:
                    df = pd.read_excel(file_path, keep_default_na=False)
                else:
                    df = pd.read_csv(file_path, keep_default_na=False)
                headers = list(df.columns.values)
                if 'name' not in headers:
                    flash(_('missing name column'), 'error')
                    raise Exception()
                for item in headers:
                    if item not in columns['allowed']:
                        columns['invalid'].append(item)
                        del df[item]
                headers = list(df.columns.values)  # Read cleaned headers again
                table = {'id': 'import', 'header': headers, 'data': []}
                table_data = []
                checked_data = []
                origin_ids = []
                for index, row in df.iterrows():
                    table_row = []
                    checked_row = {}
                    for item in headers:
                        table_row.append(row[item])
                        checked_row[item] = row[item]
                        if item == 'id' and row[item]:
                            origin_ids.append(str(row[item]))
                    table_data.append(table_row)
                    checked_data.append(checked_row)
                table['data'] = table_data

                # Check origin ids for doubles and already existing
                if origin_ids:
                    doubles = [
                        item for item,
                        count in collections.Counter(origin_ids).items() if count > 1]
                    existing = ImportMapper.check_origin_ids(project, set(origin_ids))
                    if doubles or existing:
                        if doubles:
                            flash(_('Double ids in import: ') + ', '.join(doubles), 'error')
                        if existing:
                            flash(_('ids already in database: ') + ', '.join(existing), 'error')
                        raise Exception()

            except Exception as e:  # pragma: no cover
                flash(_('error at import'), 'error')
                return render_template('import/import_data.html', project=project, form=form,
                                       class_code=class_code, columns=columns)

            if not form.preview.data and checked_data:
                g.cursor.execute('BEGIN')
                try:
                    ImportMapper.import_data(project, class_code, checked_data)
                    g.cursor.execute('COMMIT')
                    logger.log('info', 'import', 'import: ' + str(len(checked_data)))
                    flash(_('Import of') + ': ' + str(len(checked_data)), 'info')
                    imported = True
                except Exception as e:  # pragma: no cover
                    g.cursor.execute('ROLLBACK')
                    logger.log('error', 'import', 'import failed', e)
                    flash(_('error transaction'), 'error')
    return render_template('import/import_data.html', project=project, form=form,
                           class_code=class_code, table=table, columns=columns, imported=imported)
