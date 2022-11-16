from __future__ import annotations

import ast
from typing import Any, Optional

from flask import g, render_template
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    Field, FloatField, HiddenField, StringField, TextAreaField, FileField)
from wtforms.widgets import HiddenInput, TextInput, FileInput

from openatlas.forms.util import get_table_content
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.util.table import Table
from openatlas.util.util import get_base_table_data, is_authorized


class RemovableListInput(TextInput):
    def __call__(
            self,
            field: RemovableListField,
            *args: Any,
            **kwargs: Any) -> RemovableListInput:
        [name, index] = field.id.split('-')
        return super().__call__(field, **kwargs) + render_template(
            'forms/removable_list_field.html',
            name=name,
            id=index)


class RemovableListField(Field):
    widget = RemovableListInput()

    def _value(self) -> str:
        return self.data


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
        return super().__call__(field, **kwargs) + render_template(
            'forms/table_multi_select.html',
            field=field,
            selection=[e.name for e in entities if e.id in data],
            table=table)


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
        return super().__call__(field, **kwargs) + render_template(
            'forms/table_select.html',
            field=field,
            table=table.display(field.id),
            selection=selection)


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
        return super().__call__(field, **kwargs) + render_template(
            'forms/tree_multi_select.html',
            field=field,
            root=g.types[int(field.type_id)],
            selection=sorted([g.types[id_].name for id_ in data]),
            data=Type.get_tree_data(int(field.id), data))


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
        return super().__call__(field, **kwargs) + render_template(
            'forms/tree_select.html',
            field=field,
            selection=selection,
            root=g.types[int(field.type_id)],
            data=Type.get_tree_data(
                int(field.type_id),
                selected_ids,
                field.filters_ids))


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
        return super().__call__(field, **kwargs) + \
            render_template('forms/drag_n_drop_field.html')


class DragNDropField(FileField):
    """A :class:`FileField` that allows choosing multiple files."""

    data: list[str]
    widget = DragNDrop(multiple=True)

    def process_formdata(self, value_list: list[str]) -> None:
        self.data = value_list
