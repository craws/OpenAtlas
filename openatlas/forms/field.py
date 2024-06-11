from __future__ import annotations

import ast
from typing import Any, Optional

from flask import g, render_template, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import (
    BooleanField, Field, FileField, FloatField, HiddenField, StringField,
    TextAreaField)
from wtforms.validators import InputRequired
from wtforms.widgets import FileInput, HiddenInput, Input, TextInput

from openatlas import app
from openatlas.display.table import Table
from openatlas.display.util import get_base_table_data
from openatlas.display.util2 import is_authorized
from openatlas.forms.util import string_to_entity_list
from openatlas.models.entity import Entity
from openatlas.models.type import Type


class RemovableListInput(HiddenInput):
    def __call__(
            self,
            field: RemovableListField,
            *args: Any,
            **kwargs: Any) -> str:
        [name, index] = field.id.split('-')
        classes = kwargs['class'] if 'class' in kwargs else ''
        return render_template(
            'forms/removable_list_field.html',
            value=field.data,
            classes=classes,
            name=name,
            id=index)


class RemovableListField(HiddenField):
    widget = RemovableListInput()


class ValueTypeRoot(Input):
    def __call__(
            self,
            field: ValueTypeField,
            *args: Any,
            **kwargs: Any) -> Markup:
        type_ = g.types[field.type_id]
        return Markup(f'{value_type_expand_icon(type_)}')


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
            **kwargs: Any) -> Markup:
        type_ = g.types[field.type_id]
        padding = len(type_.root)
        expand_col = \
            f' <div class="me-1">{value_type_expand_icon(type_)}</div>'
        return Markup(f'''
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
    def __call__(self: Any, field: TableMultiField, **kwargs: Any) -> str:
        if request and request.method == 'POST':
            field.selection = []
            if request.form[field.name]:
                field.selection = \
                    string_to_entity_list(request.form[field.name])
        if field.selection:
            field.data = [e.id for e in field.selection]
            field.data_list = sorted([e.name for e in field.selection])
        field.table = table_multi(
            field.entities,
            field.selection,
            field.filter_ids)
        return super().__call__(field, **kwargs) + Markup(
            render_template('forms/table_multi_select.html', field=field))


class TableMultiField(HiddenField):
    widget = TableMultiSelect()

    def __init__(
            self,
            entities: list[Entity],
            selection: Optional[list[Entity]] = None,
            filter_ids: Optional[list[int]] = None,
            description: Optional[str] = None,
            **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.entities = entities
        self.selection = selection or []
        self.filter_ids = filter_ids or []
        self.description = description


def table_multi(
        entities: list[Entity],
        selection: list[Entity],
        filter_ids: list[int]) -> Table:
    filter_ids = filter_ids or []
    selection_ids = [e.id for e in selection] if selection else []
    view = entities[0].class_.view if entities else 'place'
    table_ = Table(
        [''] + g.table_headers[view],
        order=[[0, 'desc'], [1, 'asc']],
        defs=[{'orderDataType': 'dom-checkbox', 'targets': 0}])
    for e in [e for e in entities if e.id not in filter_ids]:
        row = get_base_table_data(e, show_links=False)
        row.insert(
            0,
            f'<input type="checkbox" value="{e.name}" id="{e.id}" '
            f'{" checked" if e.id in selection_ids else ""}>')
        table_.rows.append(row)
    return table_


class ValueFloatField(FloatField):
    pass


class TableSelect(HiddenInput):
    def __call__(self, field: Any, **kwargs: Any) -> str:

        def get_form(class_name_: str) -> Any:
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
                'description_dynamic',
                TextAreaField(_('description')))
            return SimpleEntityForm()

        field.forms = {}
        for class_name in field.add_dynamical:
            field.forms[class_name] = get_form(class_name)

        if request and request.method == 'POST':
            field.selection = \
                Entity.get_by_id(int(request.form[field.name])) \
                if request.form[field.name] else None

        field.data = ''
        field.data_string = ''
        if field.selection:
            field.data = field.selection.id
            field.data_string = field.selection.name
        if field.id == 'entity':
            field.table = table_annotation(field.entities)
        else:
            field.table = table(field.id, field.entities, field.filter_ids)
        return super().__call__(field, **kwargs) + Markup(
            render_template('forms/table_select.html', field=field))


class TableField(HiddenField):
    widget = TableSelect()

    def __init__(
            self,
            entities: list[Entity],
            selection: Optional[Entity] = None,
            filter_ids: Optional[list[int]] = None,
            validators: Optional[Any] = None,
            add_dynamic: Optional[list[str]] = None,
            **kwargs: Any) -> None:
        super().__init__(validators=validators, **kwargs)
        self.entities = entities
        self.selection = selection
        self.filter_ids = filter_ids or []
        self.add_dynamical = \
            (add_dynamic or []) if is_authorized('editor') else []
        self.add_dynamical.reverse()  # Reverse needed (CSS .float-end)


class TableCidocSelect(HiddenInput):
    def __call__(self, field: Any, **kwargs: Any) -> str:

        if request and request.method == 'POST':
            if code := request.form[field.name]:
                field.selection = g.properties[code] if \
                    field.id == 'property' else g.cidoc_classes[code]
        field.data = field.selection.code if field.data else ''
        field.data_string = f'{field.selection.code} {field.selection.name}' \
            if field.selection else ''
        field.table = table_cidoc(field.id, field.items)
        return super().__call__(field, **kwargs) + Markup(
            render_template('forms/table_select.html', field=field))


class TableCidocField(HiddenField):
    widget = TableCidocSelect()

    def __init__(self, items: list[Any], **kwargs: Any) -> None:
        super().__init__(validators=[InputRequired()], **kwargs)
        self.items = items
        self.selection = None


def table(
        table_id: str,
        entities: list[Entity],
        filter_ids: Optional[list[int]] = None) -> Table:
    table_ = Table(
        g.table_headers[entities[0].class_.name if entities else 'place'])
    for e in [e for e in entities if not filter_ids or e.id not in filter_ids]:
        data = get_base_table_data(e, show_links=False)
        data[0] = format_name_and_aliases(e, table_id)
        table_.rows.append(data)
    return table_


def table_annotation(entities: list[Entity]) -> Table:
    table_ = Table(['name', 'class', 'description'])
    for item in entities:
        table_.rows.append([
            format_name_and_aliases(item, 'entity'),
            item.class_.name,
            item.description])
    return table_


def table_cidoc(table_id: str, items: list[Any]) -> Table:
    table_ = Table(
        ['code', 'name'],
        defs=[
            {'orderDataType': 'cidoc-model', 'targets': [0]},
            {'sType': 'numeric', 'targets': [0]}])
    for i in items:
        onclick = f'''
            onclick="selectFromTable(this,
            '{table_id}', '{i.code}', '{i.code} {i.name}');"'''
        table_.rows.append([f'<a href="#" {onclick}>{i.code}</a>', i.name])
    return table_


class TreeMultiSelect(HiddenInput):
    def __call__(self, field: TreeField, **kwargs: Any) -> str:
        data = field.data or []
        data = ast.literal_eval(data) if isinstance(data, str) else data
        return Markup(render_template(
            'forms/tree_multi_select.html',
            field=field,
            root=g.types[int(field.type_id)],
            selection=sorted(data, key=lambda k: g.types[k].name),
            data=Type.get_tree_data(int(field.id), data))) \
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

    def __call__(self, field: TreeField, **kwargs: Any) -> str:
        selection = ''
        selected_ids = []
        if field.data:
            field.data = field.data[0] \
                if isinstance(field.data, list) else field.data
            selection = g.types[int(field.data)].name
            selected_ids.append(g.types[int(field.data)].id)
        return Markup(render_template(
            'forms/tree_select.html',
            field=field,
            selection=selection,
            root=g.types[int(field.type_id)],
            data=Type.get_tree_data(
                int(field.type_id),
                selected_ids,
                field.filters_ids,
                field.is_type_form))) + super().__call__(field, **kwargs)


class TreeField(HiddenField):

    def __init__(
            self,
            label: str,
            validators: Any = None,
            type_id: str = '',
            filter_ids: Optional[list[int]] = None,
            is_type_form: Optional[bool] = False,
            form: Any = None,
            **kwargs: Any) -> None:
        super().__init__(label, validators, **kwargs)
        self.form = form
        self.type_id = type_id or self.id
        self.filters_ids = filter_ids
        self.is_type_form = is_type_form

    widget = TreeSelect()


class DragNDrop(FileInput):
    def __call__(
            self,
            field: RemovableListField,
            *args: Any,
            **kwargs: Any) -> str:
        accept = ', '.join([
            f'.{filename}' for filename
            in g.settings['file_upload_allowed_extension']])
        return super().__call__(field, accept=accept, **kwargs) \
            + Markup(render_template('forms/drag_n_drop_field.html'))


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

    def __call__(self, field: Field, **kwargs: Any) -> str:
        kwargs['class_'] = (kwargs['class_'] + ' uc-first') \
            if 'class_' in kwargs else 'uc-first'
        return Markup(
            f'''<button
             type="submit"
             id="{field.id}"
             {self.html_params(name=field.name, **kwargs)}
             >{field.label.text}</button>''')


class SubmitField(BooleanField):
    widget = SubmitInput()


def generate_password_field() -> CustomField:
    return CustomField(
        '',
        content=f'''
            <span class="uc-first {app.config["CSS"]["button"]["primary"]}"
            id="generate-password">{_("generate password")}</span>''')


def value_type_expand_icon(type_: Type) -> str:
    return f'''
        <span onkeydown="
            if (onActivateKeyInput(event))
                switch_value_type({type_.id},this.children[0])"
        >
            <i
            aria-pressed=false
            role="button"
            tabindex="0"
            onclick="switch_value_type({type_.id},this)"
            id="value-type-switcher-{type_.id}"
            class="fa fa-chevron-right value-type-switcher input-height-sm">
            </i>
        </span>'''


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
