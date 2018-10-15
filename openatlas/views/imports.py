# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.models.imports import ImportMapper, Project
from openatlas.util.util import link, required_group, truncate_string


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
    table = {'id': 'project', 'header': ['project', 'description'], 'data': []}
    for project in ImportMapper.get_all_projects():
        table['data'].append([
            link(project),
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
    return render_template('import/project_view.html', project=project)


@app.route('/import/project/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def import_project_update(id_):
    project = ImportMapper.get_project_by_id(id_)
    form = ProjectForm(obj=project)
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
