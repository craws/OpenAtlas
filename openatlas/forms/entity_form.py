from typing import Any, Optional

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, HiddenField, SelectMultipleField, StringField, widgets)

from openatlas.database.connect import Transaction
from openatlas.display.util2 import uc_first
from openatlas.forms.add_fields import (
    add_buttons, add_class_types, add_date_fields, add_description,
    add_name_fields, add_reference_systems, add_relations, get_validators)
from openatlas.forms.field import DragNDropField, TreeField
from openatlas.forms.populate import populate_insert, populate_update
from openatlas.forms.process import process_dates
from openatlas.forms.util import convert
from openatlas.forms.validation import file, validate
from openatlas.models.entity import Entity, insert
from openatlas.models.gis import InvalidGeomException
from openatlas.models.openatlas_class import get_reverse_relation


def get_entity_form(
        entity: Entity,
        origin: Optional[Entity] = None,
        relation: Optional[str] = None) -> Any:
    class Form(FlaskForm):
        opened = HiddenField()
        validate = validate

    add_name_fields(Form, entity)
    add_class_types(Form, entity.class_)
    add_relations(Form, entity, origin)
    add_reference_systems(Form, entity.class_)
    for key, value in entity.class_.attributes.items():
        match key:
            case 'creator' | 'example_id' | 'license_holder' | \
                 'resolver_url' | 'website_url':
                setattr(
                    Form,
                    key,
                    StringField(
                        value['label'],
                        validators=get_validators(value)))
            case 'dates':
                add_date_fields(Form, entity)
            case 'description':
                add_description(Form, entity, origin)
            case 'file':
                if not entity.id:
                    setattr(
                        Form,
                        'file',
                        DragNDropField(
                            value['label'],
                            validators=get_validators(value)))
                    setattr(Form, 'validate_file', file)
            case 'location':
                for shape in ['points', 'polygons', 'lines']:
                    setattr(Form, f'gis_{shape}', HiddenField(default='[]'))
            case 'public':
                setattr(
                    Form,
                    'public',
                    BooleanField(
                        value['label'],
                        validators=get_validators(value)))
            case 'reference_system_classes':
                if choices := get_reference_system_class_choices(entity):
                    setattr(
                        Form,
                        'reference_system_classes',
                        SelectMultipleField(
                            _('classes'),
                            choices=choices,  # type: ignore
                            option_widget=widgets.CheckboxInput(),
                            widget=widgets.ListWidget(prefix_label=False)))

    add_buttons(
        Form,
        entity,
        origin.class_.relations[relation] if origin and relation else {})
    form: Any = Form(obj=entity)
    if request.method == 'GET' and entity.id:
        populate_update(form, entity)
    elif request.method == 'GET':
        populate_insert(form, entity)
    return form


def get_reference_system_class_choices(entity: Entity) -> list[tuple]:
    choices = []
    for class_ in g.classes.values():
        if 'reference_system' in class_.extra \
                and class_.name not in entity.classes \
                and not (
                    entity.name == 'GeoNames'
                    and class_.name not in g.class_groups['place']['classes']):
            choices.append((
                class_.name,
                uc_first(g.classes[class_.name].label)))
    return choices


def process_form_data(
        entity: Entity,
        form: Any,
        origin: Entity | None,
        relation_name: str | None) -> Entity:
    data = {
        'name': entity.class_.name,
        'openatlas_class_name': entity.class_.name,
        'description': entity.description,
        'begin_from': entity.dates.begin_from,
        'begin_to': entity.dates.begin_to,
        'begin_comment': entity.dates.begin_comment,
        'end_from': entity.dates.end_from,
        'end_to': entity.dates.end_to,
        'end_comment': entity.dates.end_comment}
    for attr in entity.class_.attributes:
        match attr:
            case 'dates':
                data.update(process_dates(form))
            case 'location':
                data['gis'] = {
                    shape: getattr(form, f'gis_{shape}s').data
                    for shape in ['point', 'line', 'polygon']}
            case _ if hasattr(form, attr) and (
                    getattr(form, attr).data or getattr(form, attr).data == 0):
                value = getattr(form, attr).data
                data[attr] = value.strip() if isinstance(value, str) else value
            case _:
                data[attr] = None
    try:
        Transaction.begin()
        if entity.id:
            delete_links(entity)
            entity.update(data)
        else:
            entity = insert(data)
        if entity.class_.hierarchies:
            process_types(entity, form)
        process_relations(entity, form, origin, relation_name)
        process_reference_systems(entity, form)
        Transaction.commit()
    except InvalidGeomException as e:
        Transaction.rollback()
        g.logger.log('error', 'database', 'invalid geom', e)
        raise e from None
    except Exception as e:
        Transaction.rollback()
        g.logger.log('error', 'database', 'transaction failed', e)
        raise e from None
    return entity


def process_reference_systems(entity: Entity, form: Any):
    entity.delete_links('P67', ['reference_system'], inverse=True)
    for system in g.reference_systems.values():
        if entity.class_.name not in system.classes:
            continue
        data = getattr(form, f'reference_system_id_{system.id}').data
        if data['value']:
            entity.link(
                'P67',
                system,
                data['value'],
                inverse=True,
                type_id=data['precision'])


def process_types(entity: Entity, form: Any) -> None:
    for type_ in [g.types[id_] for id_ in entity.class_.hierarchies]:
        if data := convert(getattr(form, str(type_.id)).data):
            if type_.class_.name == 'administrative_unit':
                # manager.data['administrative_units'] += value
                pass
            else:  # if entity.class_.group['name'] != 'type': # Todo: needed?
                entity.link('P2', [g.types[id_] for id_ in data])


def process_relations(
        entity: Entity,
        form: Any,
        origin: Entity | None,
        relation_name: str | None) -> None:
    for name, relation in entity.class_.relations.items():
        if relation['mode'] == 'tab':
            continue
        if hasattr(form, name) and (ids := convert(getattr(form, name).data)):
            entities = Entity.get_by_ids(ids)
            if 'object_location' in relation['classes']:
                locations = []
                for place in entities:
                    locations.append(place.get_linked_entity_safe('P53'))
                entities = locations
            entity.link(
                relation['property'],
                entities,
                inverse=relation['inverse'])
    if origin and relation_name:
        origin_relation = origin.class_.relations[relation_name]
        if not origin.class_.relations[relation_name]['additional_fields']:
            relation = get_reverse_relation(
                origin.class_,
                origin_relation,
                entity.class_)
            if not relation or relation['mode'] != 'direct':
                origin.link(
                    origin_relation['property'],
                    entity,
                    inverse=origin_relation['inverse'])


def delete_links(entity: Entity) -> None:
    if entity.class_.hierarchies:  # Todo: what about place types?
        entity.delete_links('P2', ['type'])
    for relation in entity.class_.relations.values():
        if relation['mode'] == 'direct':
            entity.delete_links(
                relation['property'],
                relation['classes'],
                relation['inverse'])
