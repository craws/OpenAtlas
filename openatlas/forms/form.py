from __future__ import annotations

from typing import Any, Optional

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, StringField, widgets
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired, URL

from openatlas import app
from openatlas.display.table import entity_table
from openatlas.display.util2 import uc_first
from openatlas.forms.add_fields import add_date_fields, add_type
from openatlas.forms.field import (
    LinkTableField, SubmitField, TableCidocField, TableField, TableMultiField,
    TreeField)
from openatlas.forms.populate import populate_dates
from openatlas.forms.validation import validate
from openatlas.models.entity import Entity, Link, get_entity_ids_with_links
from openatlas.models.openatlas_class import Relation


def filter_entities(
        entity: Entity,
        items: list[Entity],
        relation: Relation,
        is_link_form: bool = False) -> list[Entity]:
    filter_ids = [entity.id] if relation.name != 'relative' else []
    if relation.name in ['subs', 'super']:
        filter_ids += [
            e.id for e in entity.get_linked_entities_recursive(
                relation.property,
                relation.name == 'subs')]
    if is_link_form:
        if relation.reverse_relation \
                and not relation.reverse_relation.multiple:
            filter_ids += get_entity_ids_with_links(
                relation.property,
                relation.classes,
                relation.inverse)
        filter_ids += [
            e.id for e in entity.get_linked_entities(
                relation.property,
                inverse=relation.inverse)]
    return [item for item in items if item.id not in filter_ids]


def annotate_image_form(
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
            Entity.get_by_id(image_id).get_linked_entities(
                'P67',
                aliases=True,
                sort=True),
            entity))
    setattr(Form, 'save', SubmitField(_('save')))
    return Form()


def add_additional_link_fields(
        form: Any,
        relation: Relation,
        link_: Optional[Link] = None) -> None:
    for item in relation.additional_fields:
        match item:
            case 'dates':
                add_date_fields(form, link_)
            case 'description':
                setattr(
                    form,
                    'description',
                    TextAreaField(_(item), render_kw={'rows': 8}))
            case 'page':
                setattr(
                    form,
                    'description',
                    StringField(_(item), render_kw={'rows': 8}))


def link_form(origin: Entity, relation: Relation) -> Any:
    class Form(FlaskForm):
        pass

    entities = Entity.get_by_class(relation.classes, types=True, aliases=True)
    table = entity_table(
        filter_entities(origin, entities, relation, is_link_form=True),
        forms={'checkbox': True})
    setattr(Form, 'checkbox_values', HiddenField())
    setattr(Form, relation.name, LinkTableField(table=table, label=''))
    if table.rows:
        setattr(Form, 'save', SubmitField(_('save')))
    return Form('checkbox-form')


def link_detail_form(
        origin: Entity,
        relation: Relation,
        selection_id: Optional[int] = None) -> Any:
    class Form(FlaskForm):
        validate = validate

    selection = Entity.get_by_id(selection_id) if selection_id else None
    validators = [InputRequired()]
    if 'actor' in relation.additional_fields:
        entities = Entity.get_by_class(
            origin.class_.name,
            types=True,
            aliases=current_user.settings['table_show_aliases'])
        setattr(
            Form,
            'actor',
            TableField(entities, selection=origin, validators=validators))
    if relation.type:
        add_type(Form, Entity.get_hierarchy(relation.type))
    entities = Entity.get_by_class(
        relation.classes,
        types=True,
        aliases=current_user.settings['table_show_aliases'])
    entities = filter_entities(origin, entities, relation)
    if relation.multiple:
        table = TableMultiField(
            entities,
            selection=[selection] if selection else None,
            validators=validators)
    else:
        table = TableField(
            entities,
            selection=selection,
            validators=validators)
    setattr(Form, relation.name, table)
    add_additional_link_fields(Form, relation)
    setattr(Form, 'save', SubmitField(_('insert')))
    return Form()


def link_update_form(link_: Link, relation: Relation) -> Any:
    class Form(FlaskForm):
        validate = validate

    hierarchy = None
    if relation.type:
        hierarchy = Entity.get_hierarchy(relation.type)
        add_type(Form, hierarchy)
    add_additional_link_fields(Form, relation, link_)
    setattr(Form, 'save', SubmitField(_('save')))
    form = Form()
    if request.method == 'GET':
        if hierarchy:
            getattr(form, str(hierarchy.id)).data = \
                link_.type.id if link_.type else None
        for item in relation.additional_fields:
            match item:
                case 'dates':
                    populate_dates(form, link_.dates)
                case 'description' | 'page':
                    getattr(form, 'description').data = link_.description
    return form


def cidoc_form() -> Any:
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


def move_form(type_: Entity) -> Any:
    class Form(FlaskForm):
        checkbox_values = HiddenField()
        # noinspection PyTypeChecker
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
        for entity in type_.get_linked_entities(
                'P89',
                inverse=True,
                sort=True):
            place = entity.get_linked_entity('P53', inverse=True)
            if place:
                choices.append((entity.id, place.name))
    elif root.name in app.config['PROPERTY_TYPES']:
        for row in Link.get_links_by_type(type_):
            domain = Entity.get_by_id(row['domain_id'])
            range_ = Entity.get_by_id(row['range_id'])
            choices.append((row['id'], domain.name + ' - ' + range_.name))
    else:
        for entity in type_.get_linked_entities('P2', inverse=True):
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
