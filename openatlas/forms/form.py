from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from flask import g, render_template, request
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, StringField, widgets
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired, URL

from openatlas import app
from openatlas.display.table import Table
from openatlas.display.util import get_base_table_data
from openatlas.display.util2 import show_table_icons, uc_first
from openatlas.forms import base_manager, manager
from openatlas.forms.field import (
    SubmitField, TableCidocField, TableField, TableMultiField, TreeField)
from openatlas.models.entity import Entity, Link
from openatlas.views.entity_index import file_preview

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.type import Type


def get_manager(
        class_name: Optional[str] = None,
        entity: Optional[Entity] = None,
        origin: Optional[Entity] = None,
        link_: Optional[Link] = None,
        copy: Optional[bool] = False) -> base_manager.BaseManager:
    name = entity.class_.name if entity and not class_name else class_name
    manager_name = ''.join(i.capitalize() for i in name.split('_'))
    manager_instance = getattr(manager, f'{manager_name}Manager')(
        class_=g.classes['type' if name.startswith('hierarchy') else name],
        entity=entity,
        origin=origin,
        link_=link_,
        copy=copy)
    if request.method != 'POST' and not entity and not link_:
        manager_instance.populate_insert()
    return manager_instance


def get_add_reference_form(class_: str) -> Any:
    class Form(FlaskForm):
        pass

    setattr(
        Form,
        class_,
        TableMultiField(
            Entity.get_by_view(
                class_,
                types=True,
                aliases=current_user.settings['table_show_aliases']),
            validators=[InputRequired()]))
    setattr(Form, 'page', StringField(_('page')))
    setattr(Form, 'save', SubmitField(_('insert')))
    return Form()


def get_annotation_image_form(
        image_id: int,
        entity: Optional[Entity] = None,
        insert: Optional[bool] = True) -> Any:
    class Form(FlaskForm):
        text = TextAreaField(_('annotation'))
    if insert:
        setattr(
            Form,
            'coordinate',
            HiddenField(_('coordinates'), validators=[InputRequired()]))
    setattr(
        Form,
        'entity',
        TableField(
            Entity.get_by_id(image_id).get_linked_entities('P67', sort=True),
            entity))
    setattr(Form, 'save', SubmitField(_('save')))
    return Form()


def get_annotation_text_form(
        source_id: int,
        entity: Optional[Entity] = None,
        insert: Optional[bool] = True) -> Any:

    class Form(FlaskForm):
        text = TextAreaField(_('annotation'))
        link_start = IntegerField()
        link_end = IntegerField()

    if insert:
        pass

    setattr(
        Form,
        'entity',
        TableField(
            Entity.get_by_id(source_id).get_linked_entities('P67', sort=True),
            entity))
    setattr(Form, 'save', SubmitField(_('save')))
    return Form()


def get_table_form(classes: list[str], excluded: list[int]) -> str:
    entities = Entity.get_by_class(classes, types=True, aliases=True)
    table = Table([''] + g.table_headers[classes[0]], order=[[2, 'asc']])
    if classes[0] == 'file' and show_table_icons():
        table.header.insert(1, _('icon'))
    for entity in entities:
        if entity.id not in excluded:
            input_ = f"""
                <input
                    id="selection-{entity.id}"
                    name="values"
                    type="checkbox"
                    value="{entity.id}">"""
            rows = [input_]
            if classes[0] == 'file' and show_table_icons():
                rows.append(file_preview(entity.id))
            rows.extend(get_base_table_data(entity, show_links=False))
            table.rows.append(rows)
    if not table.rows:
        return '<p class="uc-first">' + _('no entries') + '</p>'
    return render_template(
        'forms/form_table.html',
        table=table.display(classes[0]))


def get_cidoc_form() -> Any:
    class Form(FlaskForm):
        pass

    for name in ('domain', 'property', 'range'):
        setattr(
            Form,
            name,
            TableCidocField(
                g.properties.values() if name == 'property'
                else g.cidoc_classes.values()))
    setattr(Form, 'save', SubmitField(_('test')))
    return Form()


def get_move_form(type_: Type) -> Any:
    class Form(FlaskForm):
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
    choices = []
    if root.class_.name == 'administrative_unit':
        for entity in type_.get_linked_entities('P89', True, sort=True):
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
    form = Form(obj=type_)
    form.selection.choices = choices
    return form


def get_vocabs_form() -> Any:  # pragma: no cover
    class Form(FlaskForm):
        base_url = StringField(
            _('base URL'),
            validators=[InputRequired(), URL()])
        endpoint = StringField(_('endpoint'), validators=[InputRequired()])
        vocabs_user = StringField(_('user'))
        save = SubmitField(_('save'))

    return Form()
