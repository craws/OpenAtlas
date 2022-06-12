from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
from collections import OrderedDict
from typing import Any, Optional, Union

from flask import g
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    FieldList, HiddenField, IntegerField, StringField, TextAreaField)
from wtforms.validators import (
    InputRequired, NoneOf, NumberRange, Optional as OptionalValidator, URL)

from openatlas.forms.field import (RemovableListField, TreeField,
                                   TreeMultiField, ValueFloatField)
from openatlas.forms.util import check_if_entity_has_time
from openatlas.models.entity import Entity
from openatlas.models.type import Type


def add_types(form: Any, class_: str) -> None:
    types = OrderedDict(
        {id_: g.types[id_] for id_ in g.classes[class_].hierarchies})
    if g.classes[class_].standard_type_id in types:  # Standard type to top
        types.move_to_end(g.classes[class_].standard_type_id, last=False)
    for type_ in types.values():
        if type_.multiple:
            setattr(form, str(type_.id), TreeMultiField(str(type_.id)))
        else:
            setattr(form, str(type_.id), TreeField(str(type_.id)))
        if type_.category == 'value':
            add_value_type_fields(form, type_.subs)


def add_value_type_fields(form: Any, subs: list[int]) -> None:
    for sub_id in subs:
        sub = g.types[sub_id]
        setattr(
            form,
            str(sub.id),
            ValueFloatField(sub.name, [OptionalValidator()]))
        add_value_type_fields(form, sub.subs)


class BaseForm:
    name: str = ''
    fields: list[str] = []
    form: FlaskForm = None
    entity: Optional[Entity] = None
    origin: Optional[Entity] = None

    def __init__(
            self,
            name: str,
            entity: Union[Entity, None],
            origin: Union[Entity, None]):

        self.name = name
        self.entity = entity
        self.origin = origin

        class Form(FlaskForm):
            origin_id = HiddenField()

        if 'name' in self.fields:
            setattr(Form, 'name', StringField(
                _('URL') if name == 'external_reference' else _('name'),
                [InputRequired(), URL()] if name == 'external_reference'
                else [InputRequired()],
                render_kw={'autofocus': True}))
        if 'alias' in self.fields:
            setattr(Form, 'alias', FieldList(RemovableListField('')))
        if name in g.classes and g.classes[name].hierarchies:
            add_types(Form, name)
        if 'date' in self.fields:
            add_date_fields(
                Form,
                bool(
                    current_user.settings['module_time']
                    or check_if_entity_has_time(entity)))
        if 'description' in self.fields:
            label = _('content') if name == 'source' else _('description')
            setattr(Form, 'description', TextAreaField(label))
            if name == 'type':
                type_ = entity if entity else origin
                if isinstance(type_, Type):
                    root = g.types[type_.root[0]] if type_.root else type_
                    if root.category == 'value':
                        del Form.description
                        setattr(Form, 'description', StringField(_('unit')))
        if 'map' in self.fields:
            setattr(Form, 'gis_points', HiddenField(default='[]'))
            setattr(Form, 'gis_polygons', HiddenField(default='[]'))
            setattr(Form, 'gis_lines', HiddenField(default='[]'))
        self.form = Form(obj=self.entity) if self.entity else Form()

    def additional_fields(self) -> dict[str, Any]:
        pass

    def populate_insert(self) -> None:
        pass

    def populate_update(self) -> None:
        pass

    def process_form_data(self, entity: Optional[Entity] = None) -> None:
        pass


def convert(value: str) -> list[int]:
    if not value:
        return []
    ids = ast.literal_eval(value)
    return ids if isinstance(ids, list) else [int(ids)]


def add_date_fields(form: Any, has_time: bool) -> None:
    validator_second = [OptionalValidator(), NumberRange(min=0, max=59)]
    validator_minute = [OptionalValidator(), NumberRange(min=0, max=59)]
    validator_hour = [OptionalValidator(), NumberRange(min=0, max=23)]
    validator_day = [OptionalValidator(), NumberRange(min=1, max=31)]
    validator_month = [OptionalValidator(), NumberRange(min=1, max=12)]
    validator_year = [
        OptionalValidator(),
        NumberRange(min=-4713, max=9999),
        NoneOf([0])]

    setattr(form, 'begin_year_from', IntegerField(
        render_kw={'placeholder': _('YYYY')}, validators=validator_year))
    setattr(form, 'begin_month_from', IntegerField(
        render_kw={'placeholder': _('MM')}, validators=validator_month))
    setattr(form, 'begin_day_from', IntegerField(
        render_kw={'placeholder': _('DD')}, validators=validator_day))
    if has_time:
        setattr(form, 'begin_hour_from', IntegerField(
            render_kw={'placeholder': _('hh')}, validators=validator_hour))
        setattr(form, 'begin_minute_from', IntegerField(
            render_kw={'placeholder': _('mm')}, validators=validator_minute))
        setattr(form, 'begin_second_from', IntegerField(
            render_kw={'placeholder': _('ss')}, validators=validator_second))
    setattr(form, 'begin_year_to', IntegerField(
        render_kw={'placeholder': _('YYYY')}, validators=validator_year))
    setattr(form, 'begin_month_to', IntegerField(
        render_kw={'placeholder': _('MM')}, validators=validator_month))
    setattr(form, 'begin_day_to', IntegerField(
        render_kw={'placeholder': _('DD')}, validators=validator_day))
    if has_time:
        setattr(form, 'begin_hour_to', IntegerField(
            render_kw={'placeholder': _('hh')}, validators=validator_hour))
        setattr(form, 'begin_minute_to', IntegerField(
            render_kw={'placeholder': _('mm')}, validators=validator_minute))
        setattr(form, 'begin_second_to', IntegerField(
            render_kw={'placeholder': _('ss')}, validators=validator_second))
    setattr(form, 'begin_comment', StringField(
        render_kw={'placeholder': _('comment')}))
    setattr(form, 'end_year_from', IntegerField(
        render_kw={'placeholder': _('YYYY')}, validators=validator_year))
    setattr(form, 'end_month_from', IntegerField(
        render_kw={'placeholder': _('MM')}, validators=validator_month))
    setattr(form, 'end_day_from', IntegerField(
        render_kw={'placeholder': _('DD')}, validators=validator_day))
    if has_time:
        setattr(form, 'end_hour_from', IntegerField(
            render_kw={'placeholder': _('hh')}, validators=validator_hour))
        setattr(form, 'end_minute_from', IntegerField(
            render_kw={'placeholder': _('mm')}, validators=validator_minute))
        setattr(form, 'end_second_from', IntegerField(
            render_kw={'placeholder': _('ss')}, validators=validator_second))
    setattr(form, 'end_year_to', IntegerField(
        render_kw={'placeholder': _('YYYY')}, validators=validator_year))
    setattr(form, 'end_month_to', IntegerField(
        render_kw={'placeholder': _('MM')}, validators=validator_month))
    setattr(form, 'end_day_to', IntegerField(
        render_kw={'placeholder': _('DD')}, validators=validator_day))
    if has_time:
        setattr(form, 'end_hour_to', IntegerField(
            render_kw={'placeholder': _('hh')}, validators=validator_hour))
        setattr(form, 'end_minute_to', IntegerField(
            render_kw={'placeholder': _('mm')}, validators=validator_minute))
        setattr(form, 'end_second_to', IntegerField(
            render_kw={'placeholder': _('ss')}, validators=validator_second))
    setattr(form, 'end_comment', StringField(
        render_kw={'placeholder': _('comment')}))
