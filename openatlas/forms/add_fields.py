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
    InputRequired, NoneOf, NumberRange, Optional as OptionalValidator, URL)

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
                entity.class_.attributes['name']['label'],
                validators=get_validators(entity.class_.attributes['name']),
                render_kw={
                    'readonly' if entity.system else 'autofocus': True}))
    if 'alias' in entity.class_.attributes:
        setattr(form, 'alias', FieldList(RemovableListField()))


def get_validators(item: dict[str, Any]):
    validators = []
    if item['required']:
        validators.append(InputRequired())
    if item.get('format') == 'url':
        validators.append(URL())
        validators.append(OptionalValidator())
    return validators


def add_reference_systems(form: Any, class_: OpenatlasClass) -> None:
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
                placeholder=system.example_id,
                choices=[('', '')] + [
                    (str(g.types[id_].id), g.types[id_].name)
                    for id_ in g.reference_match_type.subs],
                reference_system_id=system.id,
                default={
                    'value': '',
                    'precision': str(next(iter(system.types)).id)
                    if system.types else None}))


def add_description(
        form: Any,
        entity: Entity,
        origin: Optional[Entity] = None) -> None:
    attribute_description = entity.class_.attributes['description']
    if 'annotated' not in attribute_description:
        setattr(
            form,
            'description',
            TextAreaField(
                _('description'),
                render_kw={'rows': 8},
                validators=get_validators(attribute_description)))
        return
    source = entity
    if entity.class_.name == 'source_translation':
        source = origin or entity.get_linked_entity('P73', inverse=True)
    setattr(
        form,
        'annotation',
        TextAnnotationField(
            label=attribute_description['label'],
            source_text=entity.get_annotated_text() if entity.id else '',
            linked_entities=[
                {'id': e.id, 'name': e.name}
                for e in source.get_linked_entities('P67')] if source else []))
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
            TreeField(str(type_.id) + '*', type_id=type_.id))
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
    from openatlas.forms.form import filter_entities
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
        if 'type' in relation['classes']:
            root = g.types[entity.root[0]] if entity.root else origin
            setattr(
                form,
                relation['name'],
                TreeField(
                    relation['label'],
                    type_id=root.id,
                    filter_ids=[entity.id] if entity else [],
                    is_type_form=True))
            if root.directional:
                setattr(
                    form,
                    'name_inverse',
                    StringField(_('inverse')))
        elif relation['multiple']:
            selection: Any = []
            if entity.id:
                selection = entity.get_linked_entities(
                    relation['property'],
                    relation['classes'],
                    inverse=relation['inverse'])
            elif origin and origin.class_.name in relation['classes']:
                selection = [origin]
            setattr(
                form,
                name,
                TableMultiField(
                    filter_entities(entity, items, relation),
                    selection,
                    description=relation['tooltip'],
                    label=relation['label'],
                    validators=validators))
        else:
            selection = None
            if entity.id:
                selection = entity.get_linked_entity(
                    relation['property'],
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
                    filter_entities(entity, items, relation),
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


def add_buttons(form: Any, entity: Entity, relation: dict[str, Any]) -> None:
    field = SubmitField
    if 'description' in entity.class_.attributes \
            and 'annotated' in entity.class_.attributes['description']:
        field = SubmitAnnotationField
    setattr(form, 'save', field(_('save') if entity.id else _('insert')))
    if not entity.id:
        for item in entity.class_.display['form_buttons']:
            match item:
                case 'insert_and_continue' \
                        if not relation.get('additional_fields'):
                    setattr(
                        form,
                        item,
                        field(_('insert and continue')))
                    setattr(form, 'continue_', HiddenField())
                case 'insert_continue_sub':
                    label = 'unknown'
                    match entity.class_.name:
                        case 'place':
                            label = 'feature'
                        case 'feature':
                            label = 'stratigraphic unit'
                        case 'stratigraphic_unit':
                            label = 'artifact'
                    setattr(
                        form,
                        item,
                        SubmitField(_('insert and add') + ' ' + _(label)))
                case 'insert_continue_human_remains':
                    setattr(
                        form,
                        item,
                        SubmitField(
                            _('insert and add') + ' ' + _('human remains')))
