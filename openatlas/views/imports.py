import collections
from pathlib import Path
from typing import Any, Optional

import numpy
import pandas as pd
from flask import flash, g, render_template, request, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import Response
from wtforms import (
    BooleanField, FileField, StringField, TextAreaField, validators)

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    button, button_bar, description, link, required_group)
from openatlas.display.util2 import (
    datetime64_to_timestamp, format_date, get_backup_file_data, is_authorized,
    manual, uc_first)
from openatlas.forms.display import display_form
from openatlas.forms.field import SubmitField
from openatlas.models.entity import Entity
from openatlas.models.imports import Import, is_float


class ProjectForm(FlaskForm):
    project_id: Optional[int] = None
    name: Any = StringField(
        _('name'),
        [validators.InputRequired()],
        render_kw={'autofocus': True})
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))

    def validate(self, extra_validators: validators = None) -> bool:
        valid = FlaskForm.validate(self)
        name = Import.get_project_by_id(self.project_id).name \
            if self.project_id else ''
        if name != self.name.data \
                and Import.get_project_by_name(self.name.data):
            self.name.errors.append(_('error name exists'))
            valid = False
        return valid


@app.route('/import/index')
@required_group('contributor')
def import_index() -> str:
    table = Table([_('project'), _('entities'), _('description')])
    for project in Import.get_all_projects():
        table.rows.append([
            link(project),
            format_number(project.count),
            project.description])
    buttons = [manual('admin/import')]
    if is_authorized('admin'):
        buttons.append(button(_('project'), url_for('import_project_insert')))
    return render_template(
        'content.html',
        content=table.display(),
        buttons=buttons,
        title=_('import'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('import')])


@app.route('/import/project/insert', methods=['GET', 'POST'])
@required_group('manager')
def import_project_insert() -> str | Response:
    form = ProjectForm()
    if form.validate_on_submit():
        id_ = Import.insert_project(form.name.data, form.description.data)
        flash(_('project inserted'), 'info')
        return redirect(url_for('import_project_view', id_=id_))
    return render_template(
        'content.html',
        content=display_form(form, manual_page='admin/import'),
        title=_('import'),
        crumbs=[
            [_('admin'), url_for('admin_index') + '#tab-data'],
            [_('import'), url_for('import_index')],
            '+ <span class="uc-first">' + _('project') + '</span>'])


@app.route('/import/project/view/<int:id_>')
@required_group('contributor')
def import_project_view(id_: int) -> str:
    project = Import.get_project_by_id(id_)
    content = ''
    if is_authorized('manager'):
        content = button_bar([
            manual('admin/import'),
            button(
                _('edit'),
                url_for('import_project_update', id_=project.id)),
            button(
                _('delete'),
                url_for('import_project_delete', id_=project.id),
                onclick="return confirm('" +
                _('delete %(name)s?', name=project.name.replace("'", "")) +
                "')")])
        content += '<p>' + uc_first(_('new import')) + ':</p>'
        buttons = []
        for class_ in \
                ['source'] \
                + g.view_class_mapping['event'] \
                + g.view_class_mapping['actor'] \
                + ['place', 'bibliography', 'edition']:
            buttons.append(button(
                _(class_),
                url_for('import_data', project_id=project.id, class_=class_)))
        content += button_bar(buttons)
    content += description(project.description)
    tabs = {
        'info': Tab('info', content=content),
        'entities': Tab(
            'entities',
            table=Table(
                ['name', 'class', 'description', 'origin ID', 'date']))}
    for entity in Entity.get_by_project_id(id_):
        tabs['entities'].table.rows.append([
            link(entity),
            entity.class_.label,
            entity.description,
            entity.origin_id,
            format_date(entity.created)])
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=_('import'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            [_('import'), url_for('import_index')],
            project.name])


@app.route('/import/project/update/<int:id_>', methods=['GET', 'POST'])
@required_group('manager')
def import_project_update(id_: int) -> str | Response:
    project = Import.get_project_by_id(id_)
    form = ProjectForm(obj=project)
    form.project_id = id_
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        Import.update_project(project)
        flash(_('project updated'), 'info')
        return redirect(url_for('import_project_view', id_=project.id))
    return render_template(
        'content.html',
        content=display_form(form, manual_page='admin/import'),
        title=_('import'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            [_('import'), url_for('import_index')],
            project,
            _('edit')])


@app.route('/import/project/delete/<int:id_>')
@required_group('manager')
def import_project_delete(id_: int) -> Response:
    Import.delete_project(id_)
    flash(_('project deleted'), 'info')
    return redirect(url_for('import_index'))


class ImportForm(FlaskForm):
    file: Any = FileField(_('file'), [validators.InputRequired()])
    preview = BooleanField(_('preview only'), default=True)
    duplicate = BooleanField(_('check for duplicates'), default=True)
    save = SubmitField(_('import'))

    def validate(self, extra_validators: validators = None) -> bool:
        valid = FlaskForm.validate(self)
        if Path(str(request.files['file'].filename)) .suffix.lower() != '.csv':
            self.file.errors.append(_('file type not allowed'))
            valid = False
        return valid


@app.route('/import/data/<int:project_id>/<class_>', methods=['GET', 'POST'])
@required_group('manager')
def import_data(project_id: int, class_: str) -> str:
    project = Import.get_project_by_id(project_id)
    form = ImportForm()
    table = None
    imported = False
    messages: dict[str, list[str]] = {'error': [], 'warn': []}
    file_data = get_backup_file_data()
    class_label = g.classes[class_].label
    if form.validate_on_submit():
        file_ = request.files['file']
        file_path = \
            app.config['TMP_PATH'] / secure_filename(str(file_.filename))
        columns: dict[str, list[str]] = {
            'allowed': ['name', 'id', 'description'],
            'valid': [],
            'invalid': []}
        if class_ not in g.view_class_mapping['reference']:
            columns['allowed'].extend([
                'begin_from', 'begin_to', 'begin_comment',
                'end_from', 'end_to', 'end_comment'])
        columns['allowed'].append('type_ids')
        if class_ == 'place':
            columns['allowed'] += ['easting', 'northing']
        try:
            file_.save(str(file_path))
            data_frame = pd.read_csv(file_path, keep_default_na=False)
            headers = list(data_frame.columns.values)
            if 'name' not in headers:
                messages['error'].append(_('missing name column'))
                raise ValueError()
            for item in headers:
                if item not in columns['allowed']:
                    columns['invalid'].append(item)
                    del data_frame[item]
            if columns['invalid']:
                messages['warn'].append(
                    f"{_('invalid columns')}: {','.join(columns['invalid'])}")
            headers = list(data_frame.columns.values)  # Get clean headers
            table_data = []
            checked_data = []
            origin_ids = []
            names = []
            missing_name_count = 0
            invalid_type_ids = False
            invalid_geoms = False
            for _index, row in data_frame.iterrows():
                if not row['name']:
                    missing_name_count += 1
                    continue
                table_row = []
                checked_row = {}
                for item in headers:
                    value = row[item]
                    if item == 'type_ids':
                        type_ids = []
                        for type_id in str(value).split():
                            if Import.check_type_id(type_id, class_):
                                type_ids.append(type_id)  # pragma: no cover
                            else:
                                type_ids.append(
                                    f'<span class="error">{type_id}</span>')
                                invalid_type_ids = True
                        value = ' '.join(type_ids)
                    if item in ['northing', 'easting'] \
                            and row[item] \
                            and not is_float(row[item]):
                        value = f'<span class="error">{value}</span>'
                        invalid_geoms = True
                    if item in [
                            'begin_from',
                            'begin_to',
                            'end_from',
                            'end_to']:
                        if not value:
                            value = ''
                        else:
                            try:
                                value = datetime64_to_timestamp(
                                    numpy.datetime64(value))
                                row[item] = value
                            except ValueError:
                                row[item] = ''
                                value = '' if str(value) == 'NaT' else \
                                    f'<span class="error">{value}</span>'
                    table_row.append(str(value))
                    checked_row[item] = row[item]
                    if item == 'name' and form.duplicate.data:
                        names.append(row['name'].lower())
                    if item == 'id' and row[item]:
                        origin_ids.append(str(row['id']))
                table_data.append(table_row)
                checked_data.append(checked_row)
            if invalid_type_ids:
                messages['warn'].append(_('invalid type ids'))
            if invalid_geoms:
                messages['warn'].append(_('invalid coordinates'))
            table = Table(headers, rows=table_data)
            if missing_name_count:
                messages['warn'].append(
                    f"{_('empty names')}: {missing_name_count}")
            doubles = [
                item for item, count in collections.Counter(origin_ids).items()
                if count > 1]
            if doubles:
                messages['error'].append(
                    f"{_('double IDs in import')}: {', '.join(doubles)}")
            existing = Import.get_origin_ids(project, origin_ids) \
                if origin_ids else None
            if existing:
                messages['error'].append(
                    f"{_('IDs already in database')}: {', '.join(existing)}")
            if form.duplicate.data:  # Check for possible duplicates
                duplicates = Import.check_duplicates(class_, names)
                if duplicates:
                    messages['warn'].append(
                        f"{_('possible duplicates')}: {', '.join(duplicates)}")
            if messages['error']:
                raise ValueError()
        except Exception as e:
            g.logger.log('error', 'import', 'import check failed', e)
            flash(_('error at import'), 'error')
            return render_template(
                'import_data.html',
                form=form,
                messages=messages,
                file_data=file_data,
                title=_('import'),
                crumbs=[
                    [_('admin'), f"{url_for('admin_index')}#tab-data"],
                    [_('import'), url_for('import_index')],
                    project,
                    class_label])

        if not form.preview.data and checked_data and (
                not file_data['backup_too_old'] or app.testing):
            Transaction.begin()
            try:
                Import.import_data(project, class_, checked_data)
                Transaction.commit()
                g.logger.log('info', 'import', f'import: {len(checked_data)}')
                flash(f"{_('import of')}: {len(checked_data)}", 'info')
                imported = True
            except Exception as e:  # pragma: no cover
                Transaction.rollback()
                g.logger.log('error', 'import', 'import failed', e)
                flash(_('error transaction'), 'error')
    return render_template(
        'import_data.html',
        form=form,
        file_data=file_data,
        table=table,
        imported=imported,
        messages=messages,
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            [_('import'), url_for('import_index')],
            project,
            class_label])
