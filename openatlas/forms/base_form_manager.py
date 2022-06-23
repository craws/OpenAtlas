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
    FieldList, HiddenField, StringField, SubmitField, TextAreaField)
from wtforms.validators import InputRequired, URL

from openatlas.forms.add_fields import (
    add_date_fields, add_reference_systems, add_types)
from openatlas.forms.field import RemovableListField
from openatlas.forms.populate import populate_dates, \
    populate_reference_systems, populate_types
from openatlas.forms.process import process_form_dates
from openatlas.forms.util import check_if_entity_has_time
from openatlas.models.entity import Entity
from openatlas.models.openatlas_class import OpenatlasClass
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.util.util import sanitize, uc_first


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
        add_types(self.class_, self.form_class)
        for id_, field in self.additional_fields().items():
            setattr(Form, id_, field)
        add_reference_systems(self.class_, self.form_class)
        if 'date' in self.fields:
            add_date_fields(self.form_class,
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

    def additional_fields(self) -> dict[str, Any]:
        pass

    def populate_insert(self) -> None:
        pass

    def populate_update(self) -> None:
        self.form.opened.data = time.time()
        populate_types(self)
        populate_reference_systems(self)
        if hasattr(self.form, 'begin_year_from'):
            populate_dates(self)

    def process_form_data(self):
        data: dict[str, Any] = {
            'attributes': process_form_dates(self.form),
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


def convert(value: str) -> list[int]:
    if not value:
        return []
    ids = ast.literal_eval(value)
    return ids if isinstance(ids, list) else [int(ids)]
