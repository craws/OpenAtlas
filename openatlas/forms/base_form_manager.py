from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
import time
from collections import OrderedDict
from typing import Any, Optional, Union

from flask import g
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from wtforms import (
    FieldList, HiddenField, IntegerField, SelectField, StringField,
    SubmitField, TextAreaField)
from wtforms.validators import (
    InputRequired, NoneOf, NumberRange, Optional as OptionalValidator, URL)

from openatlas.forms.field import (
    RemovableListField, TreeField, TreeMultiField, ValueFloatField)
from openatlas.forms.util import check_if_entity_has_time, form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.openatlas_class import OpenatlasClass
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.util.util import format_date_part, sanitize, uc_first


class BaseFormManager:
    class_: OpenatlasClass
    fields: list[str] = []
    form: FlaskForm = None
    entity: Optional[Entity] = None
    origin: Optional[Entity] = None
    data: dict[str, Any] = {}

    def __init__(
            self,
            class_: OpenatlasClass,
            entity: Union[Entity, None],
            origin: Union[Entity, None]):

        self.class_ = class_
        self.entity = entity
        self.origin = origin

        class Form(FlaskForm):
            opened = HiddenField()
            origin_id = HiddenField()

        self.form_class = Form
        if 'name' in self.fields:
            setattr(Form, 'name', StringField(
                _('URL') if class_.name == 'external_reference' else _('name'),
                [InputRequired(), URL()] if class_.name == 'external_reference'
                else [InputRequired()],
                render_kw={'autofocus': True}))
        if 'alias' in self.fields:
            setattr(Form, 'alias', FieldList(RemovableListField('')))
        self.add_types()
        for id_, field in self.additional_fields().items():
            setattr(Form, id_, field)
        self.add_reference_systems()
        if 'date' in self.fields:
            self.add_date_fields(
                bool(
                    current_user.settings['module_time']
                    or check_if_entity_has_time(entity)))
        if 'description' in self.fields:
            label = _('content') \
                if class_.name == 'source' else _('description')
            setattr(Form, 'description', TextAreaField(label))
            if class_.name == 'type':
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

    def add_types(self):
        if self.class_.name in g.classes \
                and g.classes[self.class_.name].hierarchies:
            types = OrderedDict(
                {id_: g.types[id_] for id_ in
                 g.classes[self.class_.name].hierarchies})
            if g.classes[
                    self.class_.name].standard_type_id in types:
                types.move_to_end(  # Standard type to top
                    g.classes[self.class_.name].standard_type_id,
                    last=False)
            for type_ in types.values():
                if type_.multiple:
                    setattr(
                        self.form_class,
                        str(type_.id),
                        TreeMultiField(str(type_.id)))
                else:
                    setattr(
                        self.form_class,
                        str(type_.id),
                        TreeField(str(type_.id)))
                if type_.category == 'value':
                    self.add_value_type_fields(type_.subs)

    def add_buttons(self) -> None:
        setattr(
            self.form_class,
            'save',
            SubmitField(_('save') if self.entity else _('insert')))
        if not self.entity and 'continue' in self.fields and (
                self.class_.name in [
                    'involvement', 'artifact', 'human_remains',
                    'source_translation', 'type']
                or not self.origin):
            setattr(
                self.form_class,
                'insert_and_continue',
                SubmitField(uc_first(_('insert and continue'))))
            setattr(self.form_class, 'continue_', HiddenField())

    def add_reference_systems(self) -> None:
        precisions = [('', '')] + [
            (str(g.types[id_].id), g.types[id_].name)
            for id_ in Type.get_hierarchy('External reference match').subs]
        systems = list(g.reference_systems.values())
        systems.sort(key=lambda x: x.name.casefold())
        for system in systems:
            if self.class_.name not in system.classes:
                continue
            setattr(
                self.form_class,
                f'reference_system_id_{system.id}',
                StringField(
                    uc_first(system.name),
                    [OptionalValidator()],
                    description=system.description,
                    render_kw={
                        'autocomplete': 'off',
                        'placeholder': system.placeholder}))
            setattr(
                self.form_class,
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
        self.form.opened.data = time.time()
        if hasattr(self.form, 'begin_year_from'):
            self.populate_dates()

    def populate_dates(self) -> None:
        if self.entity.begin_from:
            self.form.begin_year_from.data = \
                format_date_part(self.entity.begin_from, 'year')
            self.form.begin_month_from.data = \
                format_date_part(self.entity.begin_from, 'month')
            self.form.begin_day_from.data = \
                format_date_part(self.entity.begin_from, 'day')
            if 'begin_hour_from' in self.form:
                self.form.begin_hour_from.data = \
                    format_date_part(self.entity.begin_from, 'hour')
                self.form.begin_minute_from.data = \
                    format_date_part(self.entity.begin_from, 'minute')
                self.form.begin_second_from.data = \
                    format_date_part(self.entity.begin_from, 'second')
            self.form.begin_comment.data = self.entity.begin_comment
            if self.entity.begin_to:
                self.form.begin_year_to.data = \
                    format_date_part(self.entity.begin_to, 'year')
                self.form.begin_month_to.data = \
                    format_date_part(self.entity.begin_to, 'month')
                self.form.begin_day_to.data = \
                    format_date_part(self.entity.begin_to, 'day')
                if 'begin_hour_from' in self.form:
                    self.form.begin_hour_to.data = \
                        format_date_part(
                        self.entity.begin_to, 'hour')
                    self.form.begin_minute_to.data = \
                        format_date_part(self.entity.begin_to, 'minute')
                    self.form.begin_second_to.data = \
                        format_date_part(self.entity.begin_to, 'second')
        if self.entity.end_from:
            self.form.end_year_from.data = \
                format_date_part(self.entity.end_from, 'year')
            self.form.end_month_from.data = \
                format_date_part(self.entity.end_from, 'month')
            self.form.end_day_from.data = \
                format_date_part(self.entity.end_from, 'day')
            if 'begin_hour_from' in self.form:
                self.form.end_hour_from.data = \
                    format_date_part(self.entity.end_from, 'hour')
                self.form.end_minute_from.data = \
                    format_date_part(self.entity.end_from, 'minute')
                self.form.end_second_from.data = \
                    format_date_part(self.entity.end_from, 'second')
            self.form.end_comment.data = self.entity.end_comment
            if self.entity.end_to:
                self.form.end_year_to.data = \
                    format_date_part(self.entity.end_to, 'year')
                self.form.end_month_to.data = \
                    format_date_part(self.entity.end_to, 'month')
                self.form.end_day_to.data = \
                    format_date_part(self.entity.end_to, 'day')
                if 'begin_hour_from' in self.form:
                    self.form.end_hour_to.data = \
                        format_date_part(self.entity.end_to, 'hour')
                    self.form.end_minute_to.data = \
                        format_date_part(self.entity.end_to, 'minute')
                    self.form.end_second_to.data = \
                        format_date_part(self.entity.end_to, 'second')

    def process_form_data(self):
        data: dict[str, Any] = {
            'attributes': self.process_form_dates(),
            'links': {'insert': [], 'delete': set(), 'delete_inverse': set()}}
        for key, value in self.form.data.items():
            field_type = getattr(self.form, key).type
            if field_type in [
                    'TreeField',
                    'TreeMultiField',
                    'TableField',
                    'TableMultiField']:
                if value:
                    ids = ast.literal_eval(value)
                    value = ids if isinstance(ids, list) else [int(ids)]
                else:
                    value = []
            if key.startswith((
                    'begin_',
                    'end_',
                    'name_inverse',
                    'multiple',
                    'page',
                    'reference_system_precision_',
                    'website_url',
                    'resolver_url',
                    'placeholder',
                    'classes')) \
                    or field_type in [
                        'CSRFTokenField',
                        'HiddenField',
                        'MultipleFileField',
                        'SelectMultipleField',
                        'SubmitField',
                        'TableField',
                        'TableMultiField']:
                continue
            if key == 'name':
                name = self.form.data['name']
                if hasattr(self.form, 'name_inverse'):
                    name = self.form.name.data.replace(
                        '(', '').replace(')', '').strip()
                    if self.form.name_inverse.data.strip():
                        inverse = self.form.name_inverse.data. \
                            replace('(', ''). \
                            replace(')', '').strip()
                        name += ' (' + inverse + ')'
                if self.entity.class_.name == 'type':
                    name = sanitize(name, 'text')
                elif isinstance(self.entity, ReferenceSystem) \
                        and self.entity.system:
                    name = self.entity.name  # Don't change the name
                    # type
                data['attributes']['name'] = name
            elif key == 'description':
                data['attributes'][key] = self.form.data[key]
            elif key == 'alias':
                data['aliases'] = value
            elif field_type in ['TreeField', 'TreeMultiField']:
                if g.types[int(getattr(self.form, key).id)].class_.name \
                        == 'administrative_unit':
                    if 'administrative_units' not in data:
                        data['administrative_units'] = []
                    data['administrative_units'] += value
                elif self.entity.class_.view != 'type':
                    data['links']['delete'].add('P2')
                    data['links']['insert'].append({
                        'property': 'P2',
                        'range': [g.types[id_] for id_ in value]})
            elif field_type == 'ValueFloatField':
                if value is not None:  # Allow the number zero
                    data['links']['insert'].append({
                        'property': 'P2',
                        'description': value,
                        'range': g.types[int(key)]})
            elif key.startswith('reference_system_id_'):
                system = Entity.get_by_id(
                    int(key.replace('reference_system_id_', '')))
                precision_field = getattr(
                    self.form,
                    key.replace('id_', 'precision_'))
                data['links']['delete_reference_system'] = True
                if value:
                    data['links']['insert'].append({
                        'property': 'P67',
                        'range': system,
                        'description': value,
                        'type_id': precision_field.data,
                        'inverse': True})
            else:  # pragma: no cover
                abort(418, f'Form error: {key}, {field_type}, value={value}')
        self.data = data

    def process_form_dates(self) -> dict[str, Any]:
        data = {
            'begin_from': None, 'begin_to': None, 'begin_comment': None,
            'end_from': None, 'end_to': None, 'end_comment': None}
        if hasattr(self.form, 'begin_year_from') \
                and self.form.begin_year_from.data:
            data['begin_comment'] = self.form.begin_comment.data
            data['begin_from'] = form_to_datetime64(
                self.form.begin_year_from.data,
                self.form.begin_month_from.data,
                self.form.begin_day_from.data,
                self.form.begin_hour_from.data
                if 'begin_hour_from' in self.form else None,
                self.form.begin_minute_from.data
                if 'begin_hour_from' in self.form else None,
                self.form.begin_second_from.data
                if 'begin_hour_from' in self.form else None)
            data['begin_to'] = form_to_datetime64(
                self.form.begin_year_to.data,
                self.form.begin_month_to.data,
                self.form.begin_day_to.data,
                self.form.begin_hour_to.data
                if 'begin_hour_from' in self.form else None,
                self.form.begin_minute_to.data
                if 'begin_hour_from' in self.form else None,
                self.form.begin_second_to.data
                if 'begin_hour_from' in self.form else None,
                to_date=True)
        if hasattr(self.form, 'end_year_from') \
                and self.form.end_year_from.data:
            data['end_comment'] = self.form.end_comment.data
            data['end_from'] = form_to_datetime64(
                self.form.end_year_from.data,
                self.form.end_month_from.data,
                self.form.end_day_from.data,
                self.form.end_hour_from.data
                if 'begin_hour_from' in self.form else None,
                self.form.end_minute_from.data
                if 'begin_hour_from' in self.form else None,
                self.form.end_second_from.data
                if 'begin_hour_from' in self.form else None)
            data['end_to'] = form_to_datetime64(
                self.form.end_year_to.data,
                self.form.end_month_to.data,
                self.form.end_day_to.data,
                self.form.end_hour_to.data
                if 'begin_hour_from' in self.form else None,
                self.form.end_minute_to.data
                if 'begin_hour_from' in self.form else None,
                self.form.end_second_to.data
                if 'begin_hour_from' in self.form else None,
                to_date=True)
        return data

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
