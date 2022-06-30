from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, Optional, Union

from flask import g, render_template, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, HiddenField, MultipleFileField,
    SelectField, SelectMultipleField, StringField, SubmitField, widgets)
from wtforms.validators import (
    InputRequired, Optional as OptionalValidator, URL)

from openatlas import app
from openatlas.forms import base_manager, entity_manager
from openatlas.forms.field import (
    TableField, TableMultiField, TreeField)
from openatlas.forms.populate_org import pre_populate_form
from openatlas.forms.validation import validate
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.util.table import Table
from openatlas.util.util import get_base_table_data, uc_first

FORMS = {
    'actor_function': ['date', 'description', 'continue'],
    'actor_actor_relation': ['date', 'description', 'continue'],
    'administrative_unit': ['name', 'description', 'continue'],
    'feature': ['name', 'date', 'description', 'continue', 'map'],
    'file': ['name', 'description'],
    'hierarchy': ['name', 'description'],
    'involvement': ['date', 'description', 'continue'],
    'note': ['description'],
    'place': ['name', 'alias', 'date', 'description', 'continue', 'map'],
    'reference_system': ['name', 'description'],
    'source': ['name', 'description', 'continue'],
    'source_translation': ['name', 'description', 'continue'],
    'stratigraphic_unit': ['name', 'date', 'description', 'continue', 'map'],
    'type': ['name', 'date', 'description', 'continue']}


def get_entity_form(
        param: Union[str, Entity],
        origin: Optional[Entity] = None) -> base_manager.BaseManager:
    class_name = param.class_.name if isinstance(param, Entity) else param
    manager_name = ''.join(i.capitalize() for i in class_name.split('_'))
    return getattr(entity_manager, f'{manager_name}Manager')(
        class_=g.classes[class_name],
        entity=param if isinstance(param, Entity) else None,
        origin=origin)


def get_form(
        class_: str,
        entity: Optional[Union[Entity, Link, Type]] = None,
        origin: Union[Entity, Type, None] = None,
        location: Optional[Entity] = None) -> FlaskForm:

    class Form(FlaskForm):
        opened = HiddenField()
        validate = validate

    if class_ == 'note':
        setattr(Form, 'public', BooleanField(_('public'), default=False))
    if not entity or (request and request.method != 'GET'):
        form = Form()
    else:
        form = pre_populate_form(Form(obj=entity), entity, location)
    customize_labels(class_, form, entity, origin)
    return form


def customize_labels(
        name: str,
        form: FlaskForm,
        item: Optional[Union[Entity, Link]] = None,
        origin: Union[Entity, Type, None] = None, ) -> None:
    if name == 'source_translation':
        form.description.label.text = _('content')
    if name in ('administrative_unit', 'type'):
        type_ = item if item else origin
        if isinstance(type_, Type):
            root = g.types[type_.root[0]] if type_.root else type_
            getattr(form, str(root.id)).label.text = 'super'


def add_buttons(
        form: Any,
        name: str,
        entity: Union[Entity, Type, Link, None],
        origin: Optional[Entity] = None) -> FlaskForm:
    if entity:
        return form
    insert_add = uc_first(_('insert and add')) + ' '
    if name == 'place':
        setattr(
            form,
            'insert_and_continue',
            SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(
            form,
            'insert_continue_sub',
            SubmitField(insert_add + _('feature')))
    elif name == 'feature' and origin and origin.class_.name == 'place':
        setattr(
            form,
            'insert_and_continue',
            SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(
            form,
            'insert_continue_sub',
            SubmitField(insert_add + _('stratigraphic unit')))
    elif name == 'stratigraphic_unit':
        setattr(
            form,
            'insert_and_continue',
            SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(
            form,
            'insert_continue_sub',
            SubmitField(insert_add + _('artifact')))
        setattr(
            form,
            'insert_continue_human_remains',
            SubmitField(insert_add + _('human remains')))
    return form


def additional_fields(
        class_: str,
        code: Union[str, None],
        entity: Union[Entity, Link, ReferenceSystem, Type, None],
        origin: Union[Entity, Type, None]) -> dict[str, Any]:
    # Preparations
    involved_with = ''
    if class_ == 'involvement' and not entity and origin:
        involved_with = 'actor' if origin.class_.view == 'event' else 'event'
    root_id = ''
    directional = False
    if class_ in ['administrative_unit', 'type']:
        type_ = entity if entity else origin
        if isinstance(type_, Type):
            root = g.types[type_.root[0]] if type_.root else type_
            root_id = str(root.id)
            directional = root.directional
    precision_id = ''
    choices = None
    if class_ == 'reference_system':
        precision_id = str(Type.get_hierarchy('External reference match').id)
        choices = ReferenceSystem.get_class_choices(entity)  # type: ignore

    fields: dict[str, dict[str, Any]] = {
        'actor_actor_relation': {
            'inverse': BooleanField(_('inverse')),
            'actor': TableMultiField(_('actor'), [InputRequired()])
            if not entity else '',
            'relation_origin_id': HiddenField() if not entity else ''},
        'actor_function': {
            'member_origin_id': HiddenField() if not entity else None,
            'actor' if code == 'member' else 'group':
                TableMultiField(_('actor'), [InputRequired()])
                if not entity else None},
        'administrative_unit': {
            'is_type_form': HiddenField(),
            root_id: TreeField(root_id) if root_id else None,
            'name_inverse': StringField(_('inverse'))
            if directional else None},
        'file': {
            'file': MultipleFileField(_('file'), [InputRequired()])
            if not entity else None,
            'page': StringField()  # Needed to link file to ref. after insert
            if not entity and origin and origin.class_.view == 'reference'
            else None},
        'hierarchy': {
            'multiple': BooleanField(
                _('multiple'),
                description=_('tooltip hierarchy multiple'))
            if code == 'custom' or (
                    entity
                    and isinstance(entity, Type)
                    and entity.category != 'value') else None,
            'classes': SelectMultipleField(
                _('classes'),
                render_kw={'disabled': True},
                description=_('tooltip hierarchy forms'),
                choices=[],
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False))},
        'involvement': {
            involved_with: TableMultiField(_(involved_with), [InputRequired()])
            if involved_with else None,
            'activity': SelectField(_('activity'))},
        'reference_system': {
            'website_url':
                StringField(_('website URL'), [OptionalValidator(), URL()]),
            'resolver_url':
                StringField(_('resolver URL'), [OptionalValidator(), URL()]),
            'placeholder': StringField(_('example ID')),
            precision_id: TreeField(precision_id),
            'classes': SelectMultipleField(
                _('classes'),
                render_kw={'disabled': True},
                choices=choices,
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False))
            if choices else None},
        'source': {
            'artifact': TableMultiField(description=_(
                'Link artifacts as the information carrier of the source'))},
        'type': {
            'is_type_form': HiddenField(),
            root_id: TreeField(root_id) if root_id else None,
            'name_inverse': StringField(_('inverse'))
            if directional else None}}
    if class_ not in fields:
        return {}
    return {k: v for k, v in fields[class_].items() if k and v}


def get_add_reference_form(class_: str) -> FlaskForm:
    class Form(FlaskForm):
        pass

    setattr(Form, class_, TableField(_(class_), [InputRequired()]))
    setattr(Form, 'page', StringField(_('page')))
    setattr(Form, 'save', SubmitField(uc_first(_('insert'))))
    return Form()


def get_table_form(class_: str, linked_entities: list[Entity]) -> str:
    """ Returns a form with a list of entities with checkboxes."""
    if class_ == 'place':
        entities = Entity.get_by_class('place', types=True, aliases=True)
    elif class_ == 'artifact':
        entities = Entity.get_by_class(
            ['artifact', 'human_remains'],
            types=True)
    else:
        entities = Entity.get_by_view(class_, types=True, aliases=True)
    linked_ids = [entity.id for entity in linked_entities]
    table = Table([''] + g.table_headers[class_], order=[[1, 'asc']])
    for entity in entities:
        if entity.id in linked_ids:
            continue  # Don't show already linked entries
        input_ = f"""
            <input
                id="selection-{entity.id}"
                name="values"
                type="checkbox"
                value="{entity.id}">"""
        table.rows.append(
            [input_] + get_base_table_data(entity, show_links=False))
    if not table.rows:
        return uc_first(_('no entries'))
    return render_template(
        'forms/form_table.html',
        table=table.display(class_))


def get_move_form(type_: Type) -> FlaskForm:
    class Form(FlaskForm):
        is_type_form = HiddenField()
        checkbox_values = HiddenField()
        selection = SelectMultipleField(
            '',
            [InputRequired()],
            coerce=int,
            option_widget=widgets.CheckboxInput(),
            widget=widgets.ListWidget(prefix_label=False))
        save = SubmitField(uc_first(_('move entities')))

    root = g.types[type_.root[0]]
    setattr(Form, str(root.id), TreeField(str(root.id)))
    form = Form(obj=type_)
    choices = []
    if root.class_.name == 'administrative_unit':
        for entity in type_.get_linked_entities('P89', True):
            place = entity.get_linked_entity('P53', True)
            if place:
                choices.append((entity.id, place.name))
    elif root.name in app.config['PROPERTY_TYPES']:
        for row in Link.get_links_by_type(type_):
            domain = Entity.get_by_id(row['domain_id'])
            range_ = Entity.get_by_id(row['range_id'])
            choices.append((row['id'], domain.name + ' - ' + range_.name))
    else:
        for entity in type_.get_linked_entities('P2', True):
            choices.append((entity.id, entity.name))
    form.selection.choices = choices
    return form
