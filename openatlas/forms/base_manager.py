from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
import time
from typing import Any, Optional, Union

from flask import g
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from wtforms import (
    FieldList, HiddenField, SelectMultipleField, StringField, SubmitField,
    TextAreaField, widgets)
from wtforms.validators import InputRequired, URL

from openatlas.forms.add_fields import (
    add_date_fields, add_reference_systems, add_types)
from openatlas.forms.field import RemovableListField, TableField
from openatlas.forms.populate import (
    populate_dates, populate_reference_systems, populate_types)
from openatlas.forms.process import process_form_dates
from openatlas.forms.util import check_if_entity_has_time
from openatlas.forms.validation import validate
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.openatlas_class import OpenatlasClass
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.util.util import sanitize, uc_first


class BaseManager:
    class_: OpenatlasClass
    fields: list[str] = []
    form: FlaskForm = None
    entity: Optional[Entity] = None
    origin: Optional[Entity] = None
    link_: Optional[Link] = None
    data: dict[str, Any] = {}

    def __init__(
            self,
            class_: OpenatlasClass,
            entity: Union[Entity, None],
            origin: Union[Entity, None],
            link_: Union[Link, None]):

        self.class_ = class_
        self.entity = entity
        self.origin = origin
        self.link_ = link_

        class Form(FlaskForm):
            opened = HiddenField()
            origin_id = HiddenField()
            validate = validate

        self.form_class = Form
        if 'name' in self.fields:
            readonly = bool(
                isinstance(self.entity, ReferenceSystem)
                and self.entity.system)
            setattr(Form, 'name', StringField(
                _('name'),
                [InputRequired()],
                render_kw={'autofocus': True, 'readonly': readonly}))
        if 'url' in self.fields:
            setattr(Form, 'name', StringField(
                _('URL'),
                [InputRequired(), URL()],
                render_kw={'autofocus': True}))
        if 'alias' in self.fields:
            setattr(Form, 'alias', FieldList(RemovableListField('')))
        add_types(self)
        for id_, field in self.additional_fields().items():
            setattr(Form, id_, field)
        add_reference_systems(self.class_, self.form_class)
        if 'date' in self.fields:
            add_date_fields(self.form_class, bool(
                current_user.settings['module_time']
                or check_if_entity_has_time(entity)))
        if 'description' in self.fields:
            setattr(Form, 'description', TextAreaField(_('description')))
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
        if self.link_:
            self.form = Form(obj=self.link_)
        elif self.entity:
            self.form = Form(obj=self.entity)
        else:
            self.form = Form()
        self.customize_labels()

    def customize_labels(self) -> None:
        if self.class_.name in ('administrative_unit', 'type') \
                and 'classes' not in self.form:
            type_ = self.entity if self.entity else self.origin
            if isinstance(type_, Type):
                root = g.types[type_.root[0]] if type_.root else type_
                getattr(self.form, str(root.id)).label.text = 'super'

    def add_buttons(self) -> None:
        setattr(
            self.form_class,
            'save',
            SubmitField(
                _('save') if self.entity or self.link_ else _('insert')))
        if not self.entity and not self.link_ and 'continue' in self.fields:
            setattr(
                self.form_class,
                'insert_and_continue',
                SubmitField(uc_first(_('insert and continue'))))
            setattr(self.form_class, 'continue_', HiddenField())

    def additional_fields(self) -> dict[str, Any]:
        return {}

    def get_root_type(self) -> Type:
        type_ = self.entity if isinstance(self.entity, Type) else self.origin
        root = g.types[type_.root[0]] if type_.root else type_
        return root

    def populate_insert(self) -> None:
        pass

    def populate_update(self) -> None:
        self.form.opened.data = time.time()
        populate_types(self)
        populate_reference_systems(self)
        if 'date' in self.fields:
            populate_dates(self)
        if hasattr(self.form, 'alias'):
            for alias in self.entity.aliases.values():
                self.form.alias.append_entry(alias)
            self.form.alias.append_entry('')

    def process_form_data(self):
        data: dict[str, Any] = {
            'attributes': process_form_dates(self.form),
            'links': {'insert': [], 'delete': [], 'delete_inverse': []}}
        if 'map' in self.fields:
            data['links']['delete'].append('P52')
            data['gis'] = {
                shape: getattr(self.form, f'gis_{shape}s').data
                for shape in ['point', 'line', 'polygon']}
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
                    data['links']['delete'].append('P2')
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


class ActorBaseManager(BaseManager):
    fields = ['name', 'alias', 'date', 'description', 'continue']

    def populate_update(self) -> None:
        super().populate_update()
        if residence := self.entity.get_linked_entity('P74'):
            self.form.residence.data = \
                residence.get_linked_entity_safe('P53', True).id
        if first := self.entity.get_linked_entity('OA8'):
            self.form.begins_in.data = \
                first.get_linked_entity_safe('P53', True).id
        if last := self.entity.get_linked_entity('OA9'):
            self.form.ends_in.data = \
                last.get_linked_entity_safe('P53', True).id

    def process_form_data(self):
        super().process_form_data()
        self.data['links']['delete'] += ['P74', 'OA8', 'OA9']
        if self.form.residence.data:
            residence = Entity.get_by_id(int(self.form.residence.data))
            self.data['links']['insert'].append({
                'property': 'P74',
                'range': residence.get_linked_entity_safe('P53')})
        if self.form.begins_in.data:
            begin_place = Entity.get_by_id(int(self.form.begins_in.data))
            self.data['links']['insert'].append({
                'property': 'OA8',
                'range': begin_place.get_linked_entity_safe('P53')})
        if self.form.ends_in.data:
            end_place = Entity.get_by_id(int(self.form.ends_in.data))
            self.data['links']['insert'].append({
                'property': 'OA9',
                'range': end_place.get_linked_entity_safe('P53')})


class EventBaseManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        fields = {
            'event_id': HiddenField(),
            'event': TableField(_('sub event of')),
            'event_preceding': TableField(_('preceding event'))}
        if self.class_.name != 'move':
            fields['place'] = TableField(_('location'))
        return fields

    def populate_update(self) -> None:
        super().populate_update()
        self.form.event_id.data = self.entity.id
        if super_event := self.entity.get_linked_entity('P9'):
            self.form.event.data = super_event.id
        if preceding_event := self.entity.get_linked_entity('P134', True):
            self.form.event_preceding.data = preceding_event.id
        if self.class_.name != 'move':
            if place := self.entity.get_linked_entity('P7'):
                self.form.place.data = \
                    place.get_linked_entity_safe('P53', True).id

    def process_form_data(self):
        super().process_form_data()
        self.data['links']['delete'].append('P9')
        self.data['links']['delete_inverse'].append('P134')
        self.data['links']['insert'].append({
            'property': 'P9',
            'range': self.form.event.data})
        self.data['links']['insert'].append({
            'property': 'P134',
            'range': self.form.event_preceding.data,
            'inverse': True})
        if self.class_.name != 'move':
            self.data['links']['delete'].append('P7')
            if self.form.place.data:
                self.data['links']['insert'].append({
                    'property': 'P7',
                    'range': Link.get_linked_entity_safe(
                        int(self.form.place.data),
                        'P53')})


class HierarchyBaseManager(BaseManager):
    fields = ['name', 'description']

    def additional_fields(self) -> dict[str, Any]:
        return {
            'classes': SelectMultipleField(
                _('classes'),
                render_kw={'disabled': True},
                description=_('tooltip hierarchy forms'),
                choices=Type.get_class_choices(self.entity),
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False))}


def convert(value: str) -> list[int]:
    if not value:
        return []
    ids = ast.literal_eval(value)
    return ids if isinstance(ids, list) else [int(ids)]
