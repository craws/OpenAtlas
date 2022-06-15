from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
from collections import OrderedDict
from typing import Any, Optional, Union

from flask import g
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    FieldList, HiddenField, IntegerField, SelectField, StringField,
    SubmitField, TextAreaField)
from wtforms.validators import (
    InputRequired, NoneOf, NumberRange, Optional as OptionalValidator, URL)
from openatlas.forms.field import (
    RemovableListField, TreeField, TreeMultiField, ValueFloatField)
from openatlas.forms.util import check_if_entity_has_time
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.util.util import uc_first


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

        self.form_class = Form
        if 'name' in self.fields:
            setattr(Form, 'name', StringField(
                _('URL') if name == 'external_reference' else _('name'),
                [InputRequired(), URL()] if name == 'external_reference'
                else [InputRequired()],
                render_kw={'autofocus': True}))
        if 'alias' in self.fields:
            setattr(Form, 'alias', FieldList(RemovableListField('')))
        self.add_types(Form)
        for id_, field in self.additional_fields().items():
            setattr(Form, id_, field)
        self.add_reference_systems(Form)
        if 'date' in self.fields:
            self.add_date_fields(
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
        self.add_buttons()
        self.form = Form(obj=self.entity) if self.entity else Form()

    def add_types(self, form: Any):
        if self.name in g.classes and g.classes[self.name].hierarchies:
            types = OrderedDict(
                {id_: g.types[id_] for id_ in
                 g.classes[self.name].hierarchies})
            if g.classes[
                    self.name].standard_type_id in types:  # Standard to top
                types.move_to_end(
                    g.classes[self.name].standard_type_id, last=False)
            for type_ in types.values():
                if type_.multiple:
                    setattr(form, str(type_.id), TreeMultiField(str(type_.id)))
                else:
                    setattr(form, str(type_.id), TreeField(str(type_.id)))
                if type_.category == 'value':
                    self.add_value_type_fields(type_.subs)

    def add_buttons(self) -> None:
        setattr(
            self.form_class,
            'save',
            SubmitField(_('save') if self.entity else _('insert')))
        if not self.entity and 'continue' in self.fields and (
                self.name in [
                    'involvement', 'artifact', 'human_remains',
                    'source_translation', 'type']
                or not self.origin):
            setattr(
                self.form_class,
                'insert_and_continue',
                SubmitField(uc_first(_('insert and continue'))))
            setattr(self.form_class, 'continue_', HiddenField())

    def add_reference_systems(self, form: Any) -> None:
        precisions = [('', '')] + [
            (str(g.types[id_].id), g.types[id_].name)
            for id_ in Type.get_hierarchy('External reference match').subs]
        systems = list(g.reference_systems.values())
        systems.sort(key=lambda x: x.name.casefold())
        for system in systems:
            if self.name not in system.classes:
                continue
            setattr(
                form,
                f'reference_system_id_{system.id}',
                StringField(
                    uc_first(system.name),
                    [OptionalValidator()],
                    description=system.description,
                    render_kw={
                        'autocomplete': 'off',
                        'placeholder': system.placeholder}))
            setattr(
                form,
                f'reference_system_precision_{system.id}',
                SelectField(
                    _('precision'),
                    choices=precisions,
                    default=system.precision_default_id))

    def additional_fields(self) -> dict[str, Any]:
        pass

    def populate_insert(self) -> None:
        pass

    def populate_update(self) -> None:
        pass

    def process_form_data(self, entity: Optional[Entity] = None) -> None:
        pass

    def add_value_type_fields(self, subs: list[int]) -> None:
        for sub_id in subs:
            sub = g.types[sub_id]
            setattr(
                self.form_class,
                str(sub.id),
                ValueFloatField(sub.name, [OptionalValidator()]))
            self.add_value_type_fields(sub.subs)

    def add_date_fields(self, has_time: bool) -> None:
        validator_second = [OptionalValidator(), NumberRange(min=0, max=59)]
        validator_minute = [OptionalValidator(), NumberRange(min=0, max=59)]
        validator_hour = [OptionalValidator(), NumberRange(min=0, max=23)]
        validator_day = [OptionalValidator(), NumberRange(min=1, max=31)]
        validator_month = [OptionalValidator(), NumberRange(min=1, max=12)]
        validator_year = [
            OptionalValidator(),
            NumberRange(min=-4713, max=9999),
            NoneOf([0])]

        setattr(
            self.form_class,
            'begin_year_from',
            IntegerField(
                render_kw={'placeholder': _('YYYY')},
                validators=validator_year))
        setattr(
            self.form_class,
            'begin_month_from',
            IntegerField(
                render_kw={'placeholder': _('MM')},
                validators=validator_month))
        setattr(
            self.form_class,
            'begin_day_from',
            IntegerField(
                render_kw={'placeholder': _('DD')},
                validators=validator_day))
        if has_time:
            setattr(
                self.form_class,
                'begin_hour_from',
                IntegerField(
                    render_kw={'placeholder': _('hh')},
                    validators=validator_hour))
            setattr(
                self.form_class,
                'begin_minute_from',
                IntegerField(
                    render_kw={'placeholder': _('mm')},
                    validators=validator_minute))
            setattr(
                self.form_class,
                'begin_second_from',
                IntegerField(
                    render_kw={'placeholder': _('ss')},
                    validators=validator_second))
        setattr(
            self.form_class,
            'begin_year_to',
            IntegerField(
                render_kw={'placeholder': _('YYYY')},
                validators=validator_year))
        setattr(
            self.form_class,
            'begin_month_to',
            IntegerField(
                render_kw={'placeholder': _('MM')},
                validators=validator_month))
        setattr(
            self.form_class,
            'begin_day_to',
            IntegerField(
                render_kw={'placeholder': _('DD')},
                validators=validator_day))
        if has_time:
            setattr(
                self.form_class,
                'begin_hour_to',
                IntegerField(
                    render_kw={'placeholder': _('hh')},
                    validators=validator_hour))
            setattr(
                self.form_class,
                'begin_minute_to',
                IntegerField(
                    render_kw={'placeholder': _('mm')},
                    validators=validator_minute))
            setattr(
                self.form_class,
                'begin_second_to',
                IntegerField(
                    render_kw={'placeholder': _('ss')},
                    validators=validator_second))
        setattr(
            self.form_class,
            'begin_comment',
            StringField(render_kw={'placeholder': _('comment')}))
        setattr(
            self.form_class,
            'end_year_from',
            IntegerField(
                render_kw={'placeholder': _('YYYY')},
                validators=validator_year))
        setattr(
            self.form_class,
            'end_month_from',
            IntegerField(
                render_kw={'placeholder': _('MM')},
                validators=validator_month))
        setattr(
            self.form_class,
            'end_day_from',
            IntegerField(
                render_kw={'placeholder': _('DD')},
                validators=validator_day))
        if has_time:
            setattr(
                self.form_class,
                'end_hour_from',
                IntegerField(
                    render_kw={'placeholder': _('hh')},
                    validators=validator_hour))
            setattr(
                self.form_class,
                'end_minute_from',
                IntegerField(
                    render_kw={'placeholder': _('mm')},
                    validators=validator_minute))
            setattr(
                self.form_class,
                'end_second_from',
                IntegerField(
                    render_kw={'placeholder': _('ss')},
                    validators=validator_second))
        setattr(
            self.form_class,
            'end_year_to',
            IntegerField(
                render_kw={'placeholder': _('YYYY')},
                validators=validator_year))
        setattr(
            self.form_class,
            'end_month_to',
            IntegerField(
                render_kw={'placeholder': _('MM')},
                validators=validator_month))
        setattr(
            self.form_class,
            'end_day_to',
            IntegerField(
                render_kw={'placeholder': _('DD')},
                validators=validator_day))
        if has_time:
            setattr(
                self.form_class,
                'end_hour_to',
                IntegerField(
                    render_kw={'placeholder': _('hh')},
                    validators=validator_hour))
            setattr(
                self.form_class,
                'end_minute_to',
                IntegerField(
                    render_kw={'placeholder': _('mm')},
                    validators=validator_minute))
            setattr(
                self.form_class,
                'end_second_to',
                IntegerField(
                    render_kw={'placeholder': _('ss')},
                    validators=validator_second))
        setattr(
            self.form_class,
            'end_comment',
            StringField(render_kw={'placeholder': _('comment')}))


def convert(value: str) -> list[int]:
    if not value:
        return []
    ids = ast.literal_eval(value)
    return ids if isinstance(ids, list) else [int(ids)]
