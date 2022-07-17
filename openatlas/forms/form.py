from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, Optional, Union

from flask import g, render_template
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, HiddenField, SelectField, SelectMultipleField, StringField,
    SubmitField, widgets)
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.forms import base_manager, entity_manager
from openatlas.forms.field import TableField, TableMultiField, TreeField
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
    'involvement': ['date', 'description', 'continue'],
    'note': ['description']}


def get_entity_form(
        class_name: Optional[str] = None,
        entity: Optional[Entity] = None,
        origin: Optional[Entity] = None) -> base_manager.BaseManager:
    class_name = entity.class_.name if not class_name else class_name
    manager_name = ''.join(i.capitalize() for i in class_name.split('_'))
    return getattr(entity_manager, f'{manager_name}Manager')(
        class_=g.classes[
            'type' if class_name.startswith('hierarchy') else class_name],
        entity=entity,
        origin=origin)


def get_form(
        class_: str,
        entity: Optional[Union[Entity, Link, Type]] = None) -> FlaskForm:

    class Form(FlaskForm):
        opened = HiddenField()
        validate = validate

    if class_ == 'note':
        setattr(Form, 'public', BooleanField(_('public'), default=False))
    return Form()


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
    involved_with = ''
    if class_ == 'involvement' and not entity and origin:
        involved_with = 'actor' if origin.class_.view == 'event' else 'event'
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
        'involvement': {
            involved_with: TableMultiField(_(involved_with), [InputRequired()])
            if involved_with else None,
            'activity': SelectField(_('activity'))}}
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
