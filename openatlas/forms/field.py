from __future__ import annotations

import ast
from typing import Any, Optional

from flask import g, render_template
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, Field, FileField, FloatField, HiddenField, StringField,
    TextAreaField)
from wtforms.widgets import (
    FileInput, HTMLString, HiddenInput, Input, TextInput)

from openatlas import app
from openatlas.display.table import Table
from openatlas.display.util import get_base_table_data, is_authorized
from openatlas.models.entity import Entity
from openatlas.models.type import Type


class RemovableListInput(HiddenInput):
    def __call__(
            self,
            field: RemovableListField,
            *args: Any,
            **kwargs: Any) -> str:
        [name, index] = field.id.split('-')
        return render_template(
            'forms/removable_list_field.html',
            value=field.data,
            name=name,
            id=index)


class RemovableListField(HiddenField):
    widget = RemovableListInput()


class ValueTypeRoot(Input):
    def __call__(
            self,
            field: ValueTypeField,
            *args: Any,
            **kwargs: Any) -> RemovableListInput:
        type_ = g.types[field.type_id]
        return HTMLString(f'{value_type_expand_icon(type_)}')


class ValueTypeRootField(FloatField):
    def __init__(
            self,
            label: str,
            type_id: int,
            validators: Any = None,
            **kwargs: Any) -> None:
        super().__init__(label, validators, **kwargs)
        self.type_id = type_id

    widget = ValueTypeRoot()


class ValueTypeInput(TextInput):
    def __call__(
            self,
            field: ValueTypeField,
            *args: Any,
            **kwargs: Any) -> RemovableListInput:
        type_ = g.types[field.type_id]
        padding = len(type_.root)
        expand_col = \
            f' <div class="me-1">{value_type_expand_icon(type_)}</div>'
        return HTMLString(f'''
            <div class="row g-1" >
              <div class="col-4  d-flex" style="padding-left:{padding}rem">
                {expand_col if type_.subs else ''}
                <label
                  class="text-truncate mt-1"
                  title="{type_.name}"
                  for="{field.id}">{type_.name}</label>
              </div>
              <div class="col">
                <input
                  type="text"
                  class="{app.config['CSS']['string_field']} value-type"
                  name="{field.id}" id="{field.id}"
                  value="{field.data or ''}" />
              </div>
              <div
                class="col-2 text-truncate"
                title="{type_.description or ''}">{type_.description or ''}
              </div>
            </div>''')


class ValueTypeField(FloatField):
    def __init__(
            self,
            label: str,
            type_id: int,
            validators: Any = None,
            **kwargs: Any) -> None:
        super().__init__(label, validators, **kwargs)
        type_ = g.types[type_id]
        sub_of = ' '.join([f'sub-of-{i}' for i in type_.root])
        self.selectors = \
            f'value-type-field {sub_of} direct-sub-of-{type_.root[-1]} d-none'
        self.field_data = 'data-show'
        self.type_id = type_id

    widget = ValueTypeInput()


class ReferenceInput(Input):
    def __call__(
            self,
            field: ReferenceField,
            *args: Any,
            **kwargs: Any) -> str:
        return render_template('forms/reference_field.html', field=field)


class ReferenceField(Field):
    def __init__(
            self,
            label: str,
            validators: Any = None,
            choices: Optional[list[tuple[str, str]]] = None,
            placeholder: Optional[str] = None,
            reference_system_id: int = 0,
            **kwargs: Any) -> None:
        super().__init__(label, validators, **kwargs)
        self.placeholder = placeholder
        self.choices = choices
        self.reference_system_id = reference_system_id
        self.data = {"value": "", "precision": ""}
        self.row_css = "reference-system-switch"

    def process_formdata(self, valuelist: list[str]) -> None:
        self.data = {
            'value': valuelist[0] if len(valuelist) == 2 else '',
            'precision': valuelist[1] if len(valuelist) == 2 else ''}

    widget = ReferenceInput()


class TableMultiSelect(HiddenInput):

    def __call__(
            self,
            field: TableMultiField,
            **kwargs: Any) -> TableMultiSelect:
        data = field.data or []
        data = ast.literal_eval(data) if isinstance(data, str) else data
        class_ = field.id if field.id != 'given_place' else 'place'
        aliases = current_user.settings['table_show_aliases']
        if class_ in ['group', 'person']:
            entities = Entity.get_by_class(class_, types=True, aliases=aliases)
        else:
            entities = Entity.get_by_view(class_, types=True, aliases=aliases)
        table = Table(
            [''] + g.table_headers[class_],
            order=[[0, 'desc'], [1, 'asc']],
            defs=[{'orderDataType': 'dom-checkbox', 'targets': 0}])
        for entity in list(
                filter(
                    lambda x: x.id not in field.filter_ids,
                    entities)):  # type: Entity
            row = get_base_table_data(entity, show_links=False)
            row.insert(0, f"""
                <input type="checkbox" id="{entity.id}" value="{entity.name}"
                {'checked' if entity.id in data else ''}>""")
            table.rows.append(row)
        return render_template(
            'forms/table_multi_select.html',
            field=field,
            selection=[e for e in entities if e.id in data],
            table=table) + super().__call__(field, **kwargs)


class TableMultiField(HiddenField):
    def __init__(
            self,
            label: Optional[str] = None,
            validators: Optional[Any] = None,
            filter_ids: Optional[list[int]] = None,
            **kwargs: Any) -> None:
        super().__init__(label, validators, **kwargs)
        self.filter_ids = filter_ids or []

    widget = TableMultiSelect()


class ValueFloatField(FloatField):
    pass


class TableSelect(HiddenInput):

    def __call__(self, field: TableField, **kwargs: Any) -> TableSelect:

        def get_form(class_name_: str) -> FlaskForm:
            class SimpleEntityForm(FlaskForm):
                name_dynamic = StringField(_('name'))

            if class_name_ in g.classes \
                    and g.classes[class_name_].hierarchies \
                    and g.classes[class_name_].standard_type_id:
                standard_type_id = g.classes[class_name_].standard_type_id
                setattr(
                    SimpleEntityForm,
                    f'{field.id}-{class_name_}-standard-type-dynamic',
                    TreeField(
                        str(standard_type_id),
                        type_id=str(standard_type_id)))
            setattr(
                SimpleEntityForm,
                "description_dynamic",
                TextAreaField(_('description')))
            return SimpleEntityForm()

        field.forms = {}
        for class_name in field.add_dynamical:
            field.forms[class_name] = get_form(class_name)

        table, selection = get_table_content(
            field.id,
            field.data,
            field.filter_ids)
        return render_template(
            'forms/table_select.html',
            field=field,
            table=table.display(field.id),
            selection=selection) + super().__call__(field, **kwargs)


class TableField(HiddenField):
    def __init__(
            self,
            label: Optional[str] = None,
            validators: Optional[Any] = None,
            filter_ids: Optional[list[int]] = None,
            add_dynamic: Optional[list[str]] = None,
            related_tables: Optional[list[str]] = None,
            **kwargs: Any) -> None:
        super().__init__(label, validators, **kwargs)
        self.filter_ids = filter_ids or []
        self.related_tables = related_tables or []
        self.add_dynamical = \
            (add_dynamic or []) if is_authorized('editor') else []

    widget = TableSelect()


class TreeMultiSelect(HiddenInput):
    def __call__(self, field: TreeField, **kwargs: Any) -> TreeMultiSelect:
        data = field.data or []
        data = ast.literal_eval(data) if isinstance(data, str) else data
        return render_template(
            'forms/tree_multi_select.html',
            field=field,
            root=g.types[int(field.type_id)],
            selection=sorted(data, key=lambda k: g.types[k].name),
            data=Type.get_tree_data(int(field.id), data)) \
            + super().__call__(field, **kwargs)


class TreeMultiField(HiddenField):
    def __init__(
            self,
            label: str,
            validators: Any = None,
            form: Any = None,
            type_id: Optional[int] = None,
            **kwargs: Any) -> None:
        super().__init__(label, validators, **kwargs)
        self.form = form
        self.type_id = type_id or self.id

    widget = TreeMultiSelect()


class TreeSelect(HiddenInput):

    def __call__(self, field: TreeField, **kwargs: Any) -> TreeSelect:
        selection = ''
        selected_ids = []
        if field.data:
            field.data = field.data[0] \
                if isinstance(field.data, list) else field.data
            selection = g.types[int(field.data)].name
            selected_ids.append(g.types[int(field.data)].id)
        return render_template(
            'forms/tree_select.html',
            field=field,
            selection=selection,
            root=g.types[int(field.type_id)],
            data=Type.get_tree_data(
                int(field.type_id),
                selected_ids,
                field.filters_ids)) + super().__call__(field, **kwargs)


class TreeField(HiddenField):

    def __init__(
            self,
            label: str,
            validators: Any = None,
            form: Any = None,
            type_id: str = '',
            filter_ids: Optional[list[int]] = None,
            **kwargs: Any) -> None:
        super().__init__(label, validators, **kwargs)
        self.form = form
        self.type_id = type_id or self.id
        self.filters_ids = filter_ids

    widget = TreeSelect()


class DragNDrop(FileInput):
    def __call__(
            self,
            field: RemovableListField,
            *args: Any,
            **kwargs: Any) -> RemovableListInput:
        accept = ', '.join([f'.{filename}' for filename
                            in g.settings['file_upload_allowed_extension']])
        return super().__call__(field, accept=accept, **kwargs) \
            + render_template('forms/drag_n_drop_field.html')


class DragNDropField(FileField):
    """A :class:`FileField` that allows choosing multiple files."""

    data: list[str]
    widget = DragNDrop(multiple=True)

    def process_formdata(self, valuelist: list[str]) -> None:
        self.data = valuelist


class CustomField(Field):

    def __init__(
            self,
            label: str,
            content: str,
            validators: Any = None,
            **kwargs: Any) -> None:
        super().__init__(label, validators, **kwargs)
        self.content = content


class SubmitInput(Input):
    input_type = 'submit'

    def __call__(self, field, **kwargs):
        if 'class_' in kwargs:
            kwargs['class_'] = kwargs['class_'] + ' uc-first'
        else:
            kwargs['class_'] = 'uc-first'

        return HTMLString(
            f'''<button
             {self.html_params(name=field.name, **kwargs)}
             >{field.label.text}</button>''')


class SubmitField(BooleanField):
    widget = SubmitInput()


def generate_password_field() -> CustomField:
    return CustomField(
        '',
        content=f'''<span 
                class="uc-first {app.config["CSS"]["button"]["primary"]}" 
                id="generate-password">{_("generate password")}</span>''')


def value_type_expand_icon(type_: Type) -> str:
    return f'''
        <i
          onclick="switch_value_type({type_.id},this)"
          role="button"
          id="value-type-switcher-{type_.id}"
          class="fa fa-chevron-right value-type-switcher input-height-sm">
        </i>'''


def get_table_content(
        class_name: str,
        selected_data: Any,
        filter_ids: Optional[list[int]] = None) -> tuple[Table, str]:
    filter_ids = filter_ids or []
    selection = ''
    if class_name in ('cidoc_domain', 'cidoc_property', 'cidoc_range'):
        table = Table(
            ['code', 'name'],
            defs=[
                {'orderDataType': 'cidoc-model', 'targets': [0]},
                {'sType': 'numeric', 'targets': [0]}])
        for id_, entity in (
          g.properties if class_name == 'cidoc_property'
          else g.cidoc_classes).items():
            onclick = f'''
                onclick="selectFromTable(
                    this,
                    '{class_name}',
                    '{id_}',
                    '{entity.code} {entity.name}');"'''
            table.rows.append([
                f'<a href="#" {onclick}>{entity.code}</a>',
                entity.name])
    else:
        aliases = current_user.settings['table_show_aliases']
        if 'place' in class_name or class_name in \
                ['begins_in', 'ends_in', 'residence']:
            class_ = 'place'
            entities = Entity.get_by_view(
                'place',
                types=True,
                aliases=aliases)
        elif class_name == 'event_preceding':
            class_ = 'event'
            entities = Entity.get_by_class(
                ['activity', 'acquisition', 'move', 'production'],
                types=True,
                aliases=aliases)
        elif class_name == 'artifact_super':
            class_ = 'place'
            entities = Entity.get_by_class(
                g.view_class_mapping['place'] + ['artifact'],
                types=True,
                aliases=aliases)
        elif class_name == 'human_remains_super':
            class_ = 'place'
            entities = Entity.get_by_class(
                g.view_class_mapping['place'] + ['human_remains'],
                types=True,
                aliases=aliases)
        else:
            class_ = class_name
            entities = Entity.get_by_view(
                class_,
                types=True,
                aliases=aliases)
        table = Table(g.table_headers[class_])
        for entity in list(
          filter(lambda x: x.id not in filter_ids, entities)):  # type: ignore
            if selected_data and entity.id == int(selected_data):
                selection = entity.name
            data = get_base_table_data(entity, show_links=False)
            data[0] = format_name_and_aliases(entity, class_name)
            table.rows.append(data)
    return table, selection


def format_name_and_aliases(entity: Entity, field_id: str) -> str:
    link = \
        f"""<a value="{entity.name}"  href='#' onclick="selectFromTable(this,
        '{field_id}', {entity.id})">{entity.name}</a>"""
    if entity.aliases:
        html = f'<p>{link}</p>'
        for i, alias in enumerate(entity.aliases.values()):
            html += alias if i else f'<p>{alias}</p>'
        return html
    return link
