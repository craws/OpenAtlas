from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from flask import flash, g, render_template, request, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from pandas import DataFrame, Series
from shapely import wkt
from shapely.errors import WKTReadingError
from werkzeug.exceptions import ImATeapot
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import Response
from wtforms import (
    BooleanField, FileField, StringField, TextAreaField, validators)

from openatlas import app
from openatlas.api.import_scripts.util import (
    get_match_types, get_reference_system_by_name)
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.error import EntityDoesNotExistError
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
from openatlas.forms.util import form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.imports import (
    Project, check_duplicates, check_single_type_duplicates, check_type_id,
    clean_reference_pages, get_id_from_origin_id, get_origin_ids, import_data_)

_('invalid columns')
_('possible duplicates')
_('invalid administrative units')
_('invalid dates')
_('invalid reference system class')
_('invalid reference system')
_('invalid reference system value')
_('invalid match type')
_('invalid type ids')
_('single type duplicates')
_('invalid value types')
_('invalid value type ids')
_('invalid value type values')
_('invalid coordinates')
_('invalid OpenAtlas class')
_('invalid reference id')
_('invalid origin reference id')
_('empty names')
_('empty ids')
_('empty parent id')
_('missing name column')
_('ids already in database')
_('double ids in import')
_('multiple parent ids')
_('invalid openatlas parent id')
_('invalid parent id')
_('invalid parent class')


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
        name = Project.get_by_id(self.project_id).name \
            if self.project_id else ''
        if name != self.name.data and Project.get_by_name(self.name.data):
            self.name.errors.append(_('error name exists'))
            valid = False
        return valid


class CheckHandler:
    def __init__(self) -> None:
        self.warning: dict[Any, set[Any]] = defaultdict(set)
        self.error: dict[Any, set[Any]] = defaultdict(set)
        self.messages: dict[str, list[str]] = {'error': [], 'warn': []}

    def set_warning(self, name: str, value: Optional[str] = None) -> None:
        self.warning[name].add(str(value))
        self.generate_warning_messages()

    def set_error(self, name: str, value: Optional[str] = None) -> None:
        self.error[name].add(str(value))
        self.generate_error_messages()

    def add_warn_message(self, message: str) -> None:
        self.messages['warn'].append(message)

    def add_error_message(self, message: str) -> None:
        self.messages['error'].append(message)

    def clear_warning_messages(self) -> None:
        self.messages['warn'].clear()

    def clear_error_messages(self) -> None:
        self.messages['error'].clear()

    def generate_warning_messages(self) -> None:
        self.clear_warning_messages()
        for key, value in self.warning.items():
            row_ids = f": {', '.join(value)}" if None not in value else None
            self.add_warn_message(_(key.replace('_', ' ')) + f"{row_ids}")

    def generate_error_messages(self) -> None:
        self.clear_error_messages()
        for key, value in self.error.items():
            if key == 'missing_name_column':
                self.add_error_message(_('missing name column'))
            else:
                self.add_error_message(
                    f"{_(key.replace('_', ' '))}: {', '.join(value)}")
        if self.messages['error']:
            raise ValueError()


@app.route('/import/index')
@required_group('contributor')
def import_index() -> str:
    table = Table([_('project'), _('entities'), _('description')])
    for project in Project.get_all():
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
        id_ = Project.insert(form.name.data, form.description.data)
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
    project = Project.get_by_id(id_)
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
                        _('delete %(name)s?',
                          name=project.name.replace("'", "")) +
                        "')")])
        content += '<p>' + uc_first(_('new import')) + ':</p>'
        buttons = []
        for class_ in \
                ['source'] \
                + g.view_class_mapping['event'] \
                + g.view_class_mapping['actor'] \
                + ['place', 'artifact', 'bibliography', 'edition', 'type']:
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
    project = Project.get_by_id(id_)
    form = ProjectForm(obj=project)
    form.project_id = id_
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.update()
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
    Project.delete(id_)
    flash(_('project deleted'), 'info')
    return redirect(url_for('import_index'))


class ImportForm(FlaskForm):
    file: Any = FileField(_('file'), [validators.InputRequired()])
    preview = BooleanField(_('preview only'), default=True)
    duplicate = BooleanField(_('check for duplicates'), default=True)
    save = SubmitField(_('import'))

    def validate(self, extra_validators: validators = None) -> bool:
        valid = FlaskForm.validate(self)
        if Path(str(request.files['file'].filename)).suffix.lower() != '.csv':
            self.file.errors.append(_('file type not allowed'))
            valid = False
        return valid


@app.route('/import/data/<int:project_id>/<class_>', methods=['GET', 'POST'])
@required_group('manager')
def import_data(project_id: int, class_: str) -> str:
    project = Project.get_by_id(project_id)
    form = ImportForm()
    table = None
    imported = False
    file_data = get_backup_file_data()
    class_label = g.classes[class_].label
    checks = CheckHandler()
    if form.validate_on_submit():
        try:
            checked_data: list[Any] = []
            table = check_data_for_table_representation(
                form,
                class_,
                checks,
                checked_data,
                project)
        except Exception as e:
            g.logger.log('error', 'import', 'import check failed', e)
            flash(_('error at import'), 'error')
            return render_template(
                'import_data.html',
                form=form,
                messages=checks.messages,
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
                import_data_(project, class_, checked_data)
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
        messages=checks.messages,
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            [_('import'), url_for('import_index')],
            project,
            class_label])


def check_data_for_table_representation(
        form: ImportForm,
        class_: str,
        checks: CheckHandler,
        checked_data: list[Any],
        project: Project) -> Table:
    file_ = request.files['file']
    file_path = app.config['TMP_PATH'] / secure_filename(str(file_.filename))
    file_.save(str(file_path))
    data_frame = pd.read_csv(file_path, keep_default_na=False, dtype=str)
    headers = get_clean_header(data_frame, class_, checks)
    table_data = []
    origin_ids = []
    names = []
    for _index, row in data_frame.iterrows():
        if not row.get('id'):
            checks.set_warning('empty_ids')
            continue
        if not row.get('name'):
            checks.set_warning('empty_names', row.get('id'))
            continue
        if row.get('parent_id') and row.get('openatlas_parent_id'):
            checks.set_error('multiple_parent_ids', row.get('id'))
        if class_ == 'type' and not (
                row.get('parent_id') or row.get('openatlas_parent_id')):
            checks.set_error('empty_parend_id', row.get('id'))
        table_row = []
        checked_row = {}
        for item in headers:
            table_row.append(
                check_cell_value(row, item, class_, checks, project))
            checked_row[item] = row[item]
            if item == 'name' and form.duplicate.data:
                names.append(row['name'].lower())
            if item == 'id' and row[item]:
                origin_ids.append(str(row['id']))
        table_data.append(table_row)
        checked_data.append(checked_row)
    if form.duplicate.data and (duplicates := check_duplicates(class_, names)):
        checks.set_warning('possible_duplicates', ', '.join(duplicates))
    if doubles := [i for i, count in Counter(origin_ids).items() if count > 1]:
        checks.set_error('double_ids_in_import', ', '.join(doubles))
    if origin_ids and (existing := get_origin_ids(project, origin_ids)):
        checks.set_error('ids_already_in_database', ', '.join(existing))
    if 'openatlas_class' in headers:
        entity_dict: dict[str, Any] = {
            row.get('id'): row['openatlas_class'].replace(' ', '_')
            for row in checked_data}
        for row in checked_data:
            if parent_id := row.get('parent_id'):
                if parent_id not in origin_ids:
                    checks.set_error('invalid_parent_id', row.get('id'))
                if not check_parent(
                        row['openatlas_class'].replace(' ', '_'),
                        entity_dict[row['parent_id']]):
                    checks.set_error('invalid_parent_class', row.get('id'))
    return Table(headers, rows=table_data)


def check_parent(entity_class: str, parent_class: str) -> bool:
    parent_class = parent_class.lower()
    is_parent = False
    match entity_class.lower():
        case 'feature':
            if parent_class == 'place':
                is_parent = True
        case 'stratigraphic_unit':
            if parent_class == 'feature':
                is_parent = True
        case 'artifact':
            if parent_class in g.view_class_mapping['place'] + ['artifact']:
                is_parent = True
        case 'human_remains':
            if (parent_class in
                    g.view_class_mapping['place'] + ['human_remains']):
                is_parent = True
        case 'type':
            if parent_class == 'type':
                is_parent = True
        case _:
            is_parent = False
    return is_parent


def get_clean_header(
        data_frame: DataFrame,
        class_: str,
        messages: CheckHandler) -> list[str]:
    columns = get_allowed_columns(class_)
    headers = data_frame.columns.to_list()
    if 'name' not in headers:
        messages.set_error('missing_name_column')
    for item in headers:
        if item.startswith('reference_system_'):
            columns['allowed'].append(item)
        if item not in columns['allowed']:
            columns['invalid'].append(item)
            del data_frame[item]
    if columns['invalid']:
        messages.set_warning('invalid_columns', ', '.join(columns['invalid']))
    return data_frame.columns.to_list()


def get_allowed_columns(class_: str) -> dict[str, list[str]]:
    columns = ['name', 'id', 'description']
    if class_ not in ['type']:
        columns.extend([
            'type_ids', 'value_types', 'origin_type_ids',
            'origin_value_types'])
    if class_ not in g.view_class_mapping['reference']:
        columns.extend([
            'begin_from', 'begin_to', 'begin_comment',
            'end_from', 'end_to', 'end_comment',
            'reference_ids', 'origin_reference_ids'])
    if class_ in ['place', 'person', 'group']:
        columns.append('alias')
    if class_ in ['place', 'artifact']:
        columns.append('wkt')
    if class_ in ['place', 'artifact', 'type']:
        columns.extend([
            'parent_id', 'openatlas_parent_id'])
    if class_ in ['place', 'type']:
        columns.extend(['openatlas_class'])
    if class_ in ['place']:
        columns.extend(['administrative_unit_id', 'historical_place_id'])
    return {
        'allowed': columns,
        'valid': [],
        'invalid': []}


def check_cell_value(
        row: Series,
        item: str,
        class_: str,
        checks: CheckHandler,
        project: Project) -> str:
    value = row[item]
    id_ = row.get('id')
    if openatlas_class := row.get('openatlas_class'):
        if openatlas_class in g.classes:
            class_ = openatlas_class
    match item:
        case ('type_ids' | 'origin_type_ids') if value:
            type_ids = []
            invalids_type_ids = []
            valid_ids = []
            for type_id in str(value).split():
                if item == 'origin_type_ids':
                    if openatlas_id := get_id_from_origin_id(project, type_id):
                        type_id = openatlas_id
                    else:
                        invalids_type_ids.append(type_id)
                        checks.set_warning('invalid_type_origin_ids', id_)
                type_ids.append(type_id)
                if check_type_id(type_id, class_):
                    valid_ids.append(type_id)
                else:
                    invalids_type_ids.append(type_id)
                    checks.set_warning('invalid_type_ids', id_)
            check_single_type = check_single_type_duplicates(valid_ids)
            for type_id in valid_ids:
                if type_id in check_single_type:
                    invalids_type_ids.append(type_id)
                    checks.set_error('single_type_duplicates', id_)
            for i, type_id in enumerate(type_ids):
                if type_id in invalids_type_ids:
                    type_ids[i] = error_span(type_id)
            value = ' '.join(type_ids)
        case ('value_types' | 'origin_value_types') if value:
            value_types = []
            for value_type in str(value).split():
                values = str(value_type).split(';')
                if item == 'origin_value_types':
                    if openatlas_id := get_id_from_origin_id(
                            project,
                            values[0]):
                        values[0] = openatlas_id
                    else:
                        checks.set_warning(
                            'invalid_origin_value_type_ids', id_)
                if len(values) != 2 or not values[1]:
                    value_types.append(error_span(value_type))
                    checks.set_warning('invalid_value_types', id_)
                    continue
                if not check_type_id(values[0], class_):
                    values[0] = error_span(values[0])
                    checks.set_warning('invalid_value_type_ids', id_)
                number = values[1][1:] if values[1].startswith('-') \
                    else values[1]
                if (not number.isdigit() and
                        not number.replace('.', '', 1).isdigit()):
                    values[1] = error_span(values[1])
                    checks.set_warning('invalid_value_type_values', id_)
                value_types.append(';'.join(values))
            value = ' '.join(value_types)
        case 'reference_ids' if value:
            references = []
            if clean_references := clean_reference_pages(str(value)):
                for reference in clean_references:
                    values = str(reference).split(';')
                    if not values[0].isdigit():
                        values[0] = error_span(values[0])
                        checks.set_warning('invalid_reference_id', id_)
                    else:
                        try:
                            ref = ApiEntity.get_by_id(int(values[0]))
                            if not ref.class_.view == 'reference':
                                raise EntityDoesNotExistError
                        except EntityDoesNotExistError:
                            values[0] = error_span(values[0])
                            checks.set_warning('invalid_reference_id', id_)
                    references.append(';'.join(values))
            else:
                checks.set_warning('invalid_reference_id', id_)
            value = ' '.join(references)
        case 'origin_reference_ids' if value:
            origin_references = []
            if clean_references := clean_reference_pages(str(value)):
                for reference in clean_references:
                    values = str(reference).split(';')
                    if origin_id := get_id_from_origin_id(project, values[0]):
                        ref = ApiEntity.get_by_id(int(origin_id))
                        if not ref.class_.view == 'reference':
                            values[0] = error_span(values[0])
                            checks.set_warning(
                                'invalid_origin_reference_id',
                                id_)
                    else:
                        checks.set_warning('invalid_origin_reference_id', id_)
                        values[0] = error_span(values[0])
                    origin_references.append(';'.join(values))
            else:
                checks.set_warning('invalid_origin_reference_id', id_)
            value = ' '.join(origin_references)
        case 'wkt' if value:
            try:
                wkt.loads(row[item])
            except WKTReadingError:
                value = error_span(value)
                checks.set_warning('invalid_coordinates', id_)
        case 'begin_from' | 'begin_to' | 'end_from' | 'end_to' if value:
            try:
                value = value.split('-')
                value = [int(item) for item in value]
                value = value + [None] * (3 - len(value))
                value = datetime64_to_timestamp(form_to_datetime64(
                    value[0],
                    value[1],
                    value[2],
                    to_date=item in ['begin_to', 'end_to']))
                row[item] = value if all(value) else ''
            except ValueError:
                row[item] = ''
                value = '' if str(value) == 'NaT' else error_span(value)
                checks.set_warning('invalid_dates', id_)
        case 'administrative_unit_id' | 'historical_place_id' if value:
            if ((not str(value).isdigit() or int(value) not in g.types) or
                    g.types[g.types[int(value)].root[0]].name not in [
                        'Administrative unit', 'Historical place']):
                value = error_span(value)
                checks.set_warning('invalid_administrative_units', id_)
        case 'openatlas_class' if value:
            if (value.lower().replace(' ', '_') not in
                    (g.view_class_mapping['place'] +
                     g.view_class_mapping['artifact']+
                     g.view_class_mapping['type'])):
                value = error_span(value)
                checks.set_warning('invalid_openatlas_class', id_)
        case 'openatlas_parent_id' if value:
            entity = None
            try:
                entity = Entity.get_by_id(value)
            except ImATeapot:
                checks.set_error('invalid_parent_id', id_)
            openatlas_class = row.get('openatlas_class') or 'type'
            if entity and not check_parent(
                    openatlas_class,
                    entity.class_.label):
                checks.set_error('invalid_parent_class', id_)
        case _ if item.startswith('reference_system_') and value:
            item = item.replace('reference_system_', '')
            reference_system = get_reference_system_by_name(item)
            if not reference_system:
                value = error_span(value)
                checks.set_warning('invalid_reference_system', id_)
            if reference_system and class_ not in reference_system.classes:
                value = error_span(value)
                checks.set_warning('invalid_reference_system_class', id_)
            values = str(value).split(';')
            if len(values) != 2:
                value = error_span(value)
                checks.set_warning('invalid_reference_system_value', id_)
            elif values[1] not in get_match_types():
                if values[1]:
                    value = f'{values[0]};{error_span(values[1])}'
                else:
                    value = error_span(value)
                checks.set_warning('invalid_match_type', id_)
    return str(value)


def error_span(value: str) -> str:
    return f'<span class="error">{value}</span>'
