import time
from typing import Any, Optional

from flask import g, request
from flask_wtf import FlaskForm
from wtforms import HiddenField

from openatlas.forms.add_fields import (
    add_buttons, add_date_fields, add_description, add_name_fields,
    add_reference_systems, add_relations, add_types)
from openatlas.forms.populate import populate_dates, populate_reference_systems
from openatlas.forms.process import process_date
from openatlas.forms.util import convert
from openatlas.forms.validation import validate
from openatlas.models.entity import Entity, insert


def get_entity_form(entity: Entity, origin: Optional[Entity] = None) -> Any:
    class Form(FlaskForm):
        opened = HiddenField()
        validate = validate

    add_name_fields(Form, entity)
    add_types(Form, entity.class_)
    add_relations(Form, entity, origin)
    add_reference_systems(Form, entity.class_)
    add_date_fields(Form, entity)
    add_description(Form, entity, origin)
    add_buttons(Form, entity)
    form: Any = Form(obj=entity)
    if request.method == 'GET' and entity.id:
        populate_update(form, entity)
    # elif request.method == 'GET' and entity.id:
    #    populate_insert(form, entity, origin, date)
    return form


def process_form_data(entity: Entity, form: Any) -> Entity:
    data = {
        'name': entity.class_.name,
        'openatlas_class_name': entity.class_.name,
        'cidoc_class_code': entity.class_.cidoc_class.code,
        'description': entity.description,
        'begin_from': entity.begin_from,
        'begin_to': entity.begin_to,
        'begin_comment': entity.begin_comment,
        'end_from': entity.end_from,
        'end_to': entity.end_to,
        'end_comment': entity.end_comment}
    for attr in entity.class_.attributes:
        data[attr] = None
        if attr == 'date':
            data.update(process_date(form, entity))
        elif getattr(form, attr).data or getattr(form, attr).data == 0:
            value = getattr(form, attr).data
            data[attr] = value.strip() if isinstance(value, str) else value
    if entity.id:
        delete_links(entity)
        entity.update(data)
    else:
        entity = insert_entity(form, data)
    process_types(entity, form)
    process_relations(entity, form)
    process_reference_systems(entity, form)
    return entity


def process_reference_systems(entity: Entity, form: Any):
    entity.delete_links(['P67'])
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
            # if entity.class_.name in \ # Todo: check needed?
            #         ['actor_function', 'actor_relation', 'involvement']:
            #    continue
            if type_.class_.name == 'administrative_unit':
                pass
                # manager.data['administrative_units'] += value
            else:  # if entity.class_.view != 'type': # Todo: check needed?
                entity.link('P2', [g.types[id_] for id_ in data])


def process_relations(entity: Entity, form: Any) -> None:
    for name, relation in entity.class_.relations.items():
        if relation['mode'] == 'tab':
            continue
        if hasattr(form, name) and (ids := convert(getattr(form, name).data)):
            entities = Entity.get_by_ids(ids)
            if 'object_location' in relation['class']:
                locations = []
                for place in entities:
                    locations.append(place.get_linked_entity_safe('P53'))
                entities = locations
            entity.link(
                relation['property'],
                entities,
                inverse=relation['inverse'])


def insert_entity(form: Any, data: dict[str, Any]) -> Entity:
    entity = insert(data)
    # if hasattr(form, 'file'):
    #    file = request.files['file']
    #    ext = secure_filename(str(file.filename)).rsplit('.', 1)[1].lower()
    #    path = app.config['UPLOAD_DIR'] / f'{entity.id}.{ext}'
    #    file.save(str(path))
    #    if f'.{ext}' in app.config['IMAGE_EXTENSIONS']:
    #        call(f'exiftran -ai {path}', shell=True)  # Fix rotation
    return entity


def delete_links(entity: Entity) -> None:
    if entity.class_.hierarchies:  # Todo: what about place types?
        entity.delete_links_by_property_and_class('P2', ['type'])
    for relation in entity.class_.relations.values():
        if relation['mode'] == 'direct':
            entity.delete_links_by_property_and_class(
                relation['property'],
                relation['class'],
                relation['inverse'])


def populate_update(form: Any, entity: Entity) -> None:
    form.opened.data = time.time()  # Todo: what if POST because of not valid?
    # Todo: deal with link types
    # types: dict[Any, Any] = manager.link_.types \
    #    if manager.link_ else manager.entity.types
    # Todo: deal with place types
    # if manager.entity and manager.entity.class_.name == 'place':
    #     if location := \
    #             manager.entity.get_linked_entity_safe('P53', types=True):
    #        types |= location.types  # Admin. units and historical places
    # Todo: implement copy
    # if entity.id and not copy:
    #     form.entity_id.data = entity.id
    populate_reference_systems(form, entity)
    if 'date' in entity.class_.attributes:
        populate_dates(form, entity)
    #if hasattr(self.form, 'alias'):
    #    for alias in self.entity.aliases.values():
    #        self.form.alias.append_entry(alias)
    #    self.form.alias.append_entry('')

    type_data: dict[int, list[int]] = {}
    for type_, value in entity.types.items():
        root = g.types[type_.root[0]] if type_.root else type
        if root.id not in type_data:
            type_data[root.id] = []
        type_data[root.id].append(type_.id)
        if root.category == 'value':
            getattr(form, str(type_.id)).data = value
    for root_id, types_ in type_data.items():
        if hasattr(form, str(root_id)):
            getattr(form, str(root_id)).data = types_
