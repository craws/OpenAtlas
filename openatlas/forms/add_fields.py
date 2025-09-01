from __future__ import annotations

from collections import OrderedDict
from typing import Any, Optional

from flask import g
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    FieldList, HiddenField, IntegerField, StringField, TextAreaField)
from wtforms.validators import (
    InputRequired, NoneOf, NumberRange, Optional as OptionalValidator)

from openatlas.display.util2 import is_authorized
from openatlas.forms.field import (
    ReferenceField, RemovableListField, SubmitAnnotationField, SubmitField,
    TableField, TableMultiField, TextAnnotationField, TreeField,
    TreeMultiField, ValueTypeField, ValueTypeRootField)
from openatlas.models.dates import check_if_entity_has_time
from openatlas.models.entity import Entity
from openatlas.models.openatlas_class import OpenatlasClass


def add_name_fields(form: Any, entity: Entity) -> None:
    if 'name' in entity.class_.attributes:
        setattr(
            form,
            'name',
            StringField(
                _('name'),
                validators=[InputRequired()],
                render_kw={'autofocus': True}))
    if 'alias' in entity.class_.attributes:
        setattr(form, 'alias', FieldList(RemovableListField()))


def add_reference_systems(form: Any, class_: OpenatlasClass) -> None:
    precisions = [('', '')] + [
        (str(g.types[id_].id), g.types[id_].name)
        for id_ in g.reference_match_type.subs]
    reference_systems = list(g.reference_systems.values())
    reference_systems.sort(key=lambda x: x.name.casefold())
    for system in reference_systems:
        if class_.name not in system.classes:
            continue
        setattr(
            form,
            f'reference_system_id_{system.id}',
            ReferenceField(
                system.name,
                description=system.description,
                placeholder=system.placeholder,
                choices=precisions,
                reference_system_id=system.id,
                default={
                    'value': '',
                    'precision': str(system.precision_default_id)}))


def add_description(
        form: Any,
        entity: Entity,
        origin: Optional[Entity] = None) -> None:
    if 'description' not in entity.class_.attributes:
        return
    if 'annotated' not in entity.class_.attributes['description']:
        setattr(
            form,
            'description',
            TextAreaField(_('description'), render_kw={'rows': 8}))
        return
    source = entity
    if entity.class_.name == 'source_translation':
        source = origin or entity.get_linked_entity('P73', inverse=True)
    setattr(
        form,
        'annotation',
        TextAnnotationField(
            label=entity.class_.attributes['description']['label'],
            source_text=entity.get_annotated_text() if entity.id else '',
            linked_entities=[
                {'id': e.id, 'name': e.name}
                for e in source.get_linked_entities('P67')]))
    setattr(form, 'description', HiddenField())


def add_class_types(form: Any, class_: OpenatlasClass) -> None:
    if not class_.hierarchies:
        return
    types = OrderedDict({id_: g.types[id_] for id_ in class_.hierarchies})
    if class_.standard_type_id in types:
        types.move_to_end(class_.standard_type_id, last=False)
    for type_ in types.values():
        add_type(form, type_)


def add_type(form: Any, type_: Entity):
    add_form = None
    if is_authorized('editor'):
        class AddDynamicType(FlaskForm):
            pass

        setattr(AddDynamicType, 'name-dynamic', StringField(_('super')))
        setattr(
            AddDynamicType,
            f'{type_.id}-dynamic',
            TreeField(str(type_.id) + '*', type_id=str(type_.id)))
        setattr(
            AddDynamicType,
            'description-dynamic',
            TextAreaField(_('description')))
        add_form = AddDynamicType()
    validators = [InputRequired()] if type_.required else []
    if type_.category == 'value':
        field = ValueTypeRootField(type_.name, type_.id)
    elif type_.multiple:
        field = TreeMultiField(str(type_.id), validators, form=add_form)
    else:
        field = TreeField(str(type_.id), validators, form=add_form)
    setattr(form, str(type_.id), field)
    if type_.category == 'value':
        add_value_type_fields(form, type_.subs)


def add_relations(form: Any, entity: Entity, origin: Entity | None) -> None:
    entities = {}  # Collect entities per class to prevent multiple fetching
    for name, relation in entity.class_.relations.items():
        if relation['mode'] != 'direct':
            continue
        validators = [InputRequired()] if relation['required'] else None
        items = []
        for class_ in relation['classes']:
            class_ = 'place' if class_ == 'object_location' else class_
            if class_ not in entities:
                entities[class_] = Entity.get_by_class(class_, True, True)
            items += entities[class_]
        if relation['multiple']:
            selection: Any = []
            if entity.id:
                selection = entity.get_linked_entities(
                    relation['properties'],
                    relation['classes'],
                    inverse=relation['inverse'])
            elif origin and origin.class_.name in relation['classes']:
                selection = [origin]
            setattr(
                form,
                name,
                TableMultiField(
                    items,
                    selection,
                    description=relation['tooltip'],
                    label=relation['label'],
                    validators=validators))
        else:
            selection = None
            if entity.id:
                selection = entity.get_linked_entity(
                    relation['properties'],
                    relation['classes'],
                    relation['inverse'])
            elif origin and origin.class_.name in relation['classes']:
                selection = origin
            if selection and selection.class_.name == 'object_location':
                selection = selection.get_linked_entity_safe('P53', True)
            setattr(
                form,
                name,
                TableField(
                    items,
                    selection,
                    label=relation['label'],
                    description=relation['tooltip'],
                    validators=validators))


def add_date_fields(form_class: Any, entity: Optional[Entity] = None) -> None:
    validator_second = [OptionalValidator(), NumberRange(min=0, max=59)]
    validator_minute = [OptionalValidator(), NumberRange(min=0, max=59)]
    validator_hour = [OptionalValidator(), NumberRange(min=0, max=23)]
    validator_day = [OptionalValidator(), NumberRange(min=1, max=31)]
    validator_month = [OptionalValidator(), NumberRange(min=1, max=12)]
    validator_year = [
        OptionalValidator(),
        NumberRange(min=-4713, max=9999),
        NoneOf([0])]
    has_time = bool(
        current_user.settings['module_time']
        or (entity and check_if_entity_has_time(entity.dates)))
    setattr(
        form_class,
        'begin_year_from',
        IntegerField(
            render_kw={'placeholder': _('YYYY')},
            validators=validator_year))
    setattr(
        form_class,
        'begin_month_from',
        IntegerField(
            render_kw={'placeholder': _('MM')},
            validators=validator_month))
    setattr(
        form_class,
        'begin_day_from',
        IntegerField(
            render_kw={'placeholder': _('DD')},
            validators=validator_day))
    if has_time:
        setattr(
            form_class,
            'begin_hour_from',
            IntegerField(
                render_kw={'placeholder': _('hh')},
                validators=validator_hour))
        setattr(
            form_class,
            'begin_minute_from',
            IntegerField(
                render_kw={'placeholder': _('mm')},
                validators=validator_minute))
        setattr(
            form_class,
            'begin_second_from',
            IntegerField(
                render_kw={'placeholder': _('ss')},
                validators=validator_second))
    setattr(
        form_class,
        'begin_year_to',
        IntegerField(
            render_kw={'placeholder': _('YYYY')},
            validators=validator_year))
    setattr(
        form_class,
        'begin_month_to',
        IntegerField(
            render_kw={'placeholder': _('MM')},
            validators=validator_month))
    setattr(
        form_class,
        'begin_day_to',
        IntegerField(
            render_kw={'placeholder': _('DD')},
            validators=validator_day))
    if has_time:
        setattr(
            form_class,
            'begin_hour_to',
            IntegerField(
                render_kw={'placeholder': _('hh')},
                validators=validator_hour))
        setattr(
            form_class,
            'begin_minute_to',
            IntegerField(
                render_kw={'placeholder': _('mm')},
                validators=validator_minute))
        setattr(
            form_class,
            'begin_second_to',
            IntegerField(
                render_kw={'placeholder': _('ss')},
                validators=validator_second))
    setattr(
        form_class,
        'begin_comment',
        StringField(render_kw={'placeholder': _('comment')}))
    setattr(
        form_class,
        'end_year_from',
        IntegerField(
            render_kw={'placeholder': _('YYYY')},
            validators=validator_year))
    setattr(
        form_class,
        'end_month_from',
        IntegerField(
            render_kw={'placeholder': _('MM')},
            validators=validator_month))
    setattr(
        form_class,
        'end_day_from',
        IntegerField(
            render_kw={'placeholder': _('DD')},
            validators=validator_day))
    if has_time:
        setattr(
            form_class,
            'end_hour_from',
            IntegerField(
                render_kw={'placeholder': _('hh')},
                validators=validator_hour))
        setattr(
            form_class,
            'end_minute_from',
            IntegerField(
                render_kw={'placeholder': _('mm')},
                validators=validator_minute))
        setattr(
            form_class,
            'end_second_from',
            IntegerField(
                render_kw={'placeholder': _('ss')},
                validators=validator_second))
    setattr(
        form_class,
        'end_year_to',
        IntegerField(
            render_kw={'placeholder': _('YYYY')},
            validators=validator_year))
    setattr(
        form_class,
        'end_month_to',
        IntegerField(
            render_kw={'placeholder': _('MM')},
            validators=validator_month))
    setattr(
        form_class,
        'end_day_to',
        IntegerField(
            render_kw={'placeholder': _('DD')},
            validators=validator_day))
    if has_time:
        setattr(
            form_class,
            'end_hour_to',
            IntegerField(
                render_kw={'placeholder': _('hh')},
                validators=validator_hour))
        setattr(
            form_class,
            'end_minute_to',
            IntegerField(
                render_kw={'placeholder': _('mm')},
                validators=validator_minute))
        setattr(
            form_class,
            'end_second_to',
            IntegerField(
                render_kw={'placeholder': _('ss')},
                validators=validator_second))
    setattr(
        form_class,
        'end_comment',
        StringField(render_kw={'placeholder': _('comment')}))


def add_value_type_fields(form_class: FlaskForm, subs: list[int]) -> None:
    for sub_id in subs:
        sub = g.types[sub_id]
        setattr(
            form_class,
            str(sub.id),
            ValueTypeField(sub.name, sub.id, [OptionalValidator()]))
        add_value_type_fields(form_class, sub.subs)


def add_buttons(form: Any, entity: Entity) -> None:
    field = SubmitField
    if 'description' in entity.class_.attributes \
            and 'annotated' in entity.class_.attributes['description']:
        field = SubmitAnnotationField
    setattr(form, 'save', field(_('save') if entity.id else _('insert')))
    if not entity.id and entity.class_.display['form']['insert_and_continue']:
        setattr(form, 'insert_and_continue', field(_('insert and continue')))
        setattr(form, 'continue_', HiddenField())
