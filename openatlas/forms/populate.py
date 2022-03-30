import time
from typing import Any, Optional, Union

from flask import g
from flask_wtf import FlaskForm

from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.util.util import format_date_part


def pre_populate_form(
        form: FlaskForm,
        item: Union[Entity, Link],
        location: Optional[Entity]) -> FlaskForm:
    form.opened.data = time.time()
    if hasattr(form, 'begin_year_from'):
        populate_dates(form, item)
    if isinstance(item, Entity):
        populate_reference_systems(form, item)
    if isinstance(item, ReferenceSystem) and item.system:
        form.name.render_kw['readonly'] = 'readonly'
    if isinstance(item, Entity) and item.class_.view == 'event':
        form.event_id.data = item.id

    # Types
    types: dict[Any, Any] = item.types
    if location:
        types |= location.types  # Administrative units and historical places
    type_data: dict[int, list[int]] = {}
    for type_, value in types.items():
        root = g.types[type_.root[0]] if type_.root else type
        if root.id not in type_data:
            type_data[root.id] = []
        type_data[root.id].append(type_.id)
        if root.category == 'value':
            getattr(form, str(type_.id)).data = value
    for root_id, types_ in type_data.items():
        if hasattr(form, str(root_id)):
            getattr(form, str(root_id)).data = types_
    return form


def populate_reference_systems(form: FlaskForm, item: Entity) -> None:
    system_links = {
        # Can't use isinstance for class check here
        link_.domain.id: link_ for link_ in item.get_links('P67', True)
        if link_.domain.class_.name == 'reference_system'}
    for key in form.data:
        field = getattr(form, key)
        if field.id.startswith('reference_system_id_'):
            system_id = int(field.id.replace('reference_system_id_', ''))
            if system_id in system_links:
                field.data = system_links[system_id].description
                precision_field = getattr(
                    form,
                    f'reference_system_precision_{system_id}')
                precision_field.data = str(system_links[system_id].type.id)


def populate_dates(form: FlaskForm, item: Union[Entity, Link]) -> None:
    if item.begin_from:
        form.begin_year_from.data = format_date_part(item.begin_from, 'year')
        form.begin_month_from.data = format_date_part(item.begin_from, 'month')
        form.begin_day_from.data = format_date_part(item.begin_from, 'day')
        form.begin_comment.data = item.begin_comment
        if item.begin_to:
            form.begin_year_to.data = format_date_part(item.begin_to, 'year')
            form.begin_month_to.data = format_date_part(item.begin_to, 'month')
            form.begin_day_to.data = format_date_part(item.begin_to, 'day')
    if item.end_from:
        form.end_year_from.data = format_date_part(item.end_from, 'year')
        form.end_month_from.data = format_date_part(item.end_from, 'month')
        form.end_day_from.data = format_date_part(item.end_from, 'day')
        form.end_comment.data = item.end_comment
        if item.end_to:
            form.end_year_to.data = format_date_part(item.end_to, 'year')
            form.end_month_to.data = format_date_part(item.end_to, 'month')
            form.end_day_to.data = format_date_part(item.end_to, 'day')


def populate_update_form(form: FlaskForm, entity: Union[Entity, Type]) -> None:
    if hasattr(form, 'alias'):
        for alias in entity.aliases.values():
            form.alias.append_entry(alias)
        form.alias.append_entry('')
    if entity.class_.view == 'actor':
        if res := entity.get_linked_entity('P74'):
            form.residence.data = res.get_linked_entity_safe('P53', True).id
        if first := entity.get_linked_entity('OA8'):
            form.begins_in.data = first.get_linked_entity_safe('P53', True).id
        if last := entity.get_linked_entity('OA9'):
            form.ends_in.data = last.get_linked_entity_safe('P53', True).id
    elif entity.class_.name == 'artifact':
        owner = entity.get_linked_entity('P52')
        form.actor.data = owner.id if owner else None
    elif entity.class_.view == 'event':
        super_event = entity.get_linked_entity('P9')
        form.event.data = super_event.id if super_event else ''
        preceding = entity.get_linked_entity('P134', True)
        form.event_preceding.data = preceding.id if preceding else ''
        if entity.class_.name == 'move':
            if place_from := entity.get_linked_entity('P27'):
                form.place_from.data = \
                    place_from.get_linked_entity_safe('P53', True).id
            if place_to := entity.get_linked_entity('P26'):
                form.place_to.data = \
                    place_to.get_linked_entity_safe('P53', True).id
            person_data = []
            object_data = []
            for linked_entity in entity.get_linked_entities('P25'):
                if linked_entity.class_.name == 'person':
                    person_data.append(linked_entity.id)
                elif linked_entity.class_.view == 'artifact':
                    object_data.append(linked_entity.id)
            form.person.data = person_data
            form.artifact.data = object_data
        else:
            if place := entity.get_linked_entity('P7'):
                form.place.data = place.get_linked_entity_safe('P53', True).id
        if entity.class_.name == 'acquisition':
            form.given_place.data = \
                [entity.id for entity in entity.get_linked_entities('P24')]
        if entity.class_.name == 'production':
            form.artifact.data = \
                [entity.id for entity in entity.get_linked_entities('P108')]
    elif isinstance(entity, Type):
        if hasattr(form, 'name_inverse'):  # Directional, e.g. actor relation
            name_parts = entity.name.split(' (')
            form.name.data = name_parts[0]
            if len(name_parts) > 1:
                form.name_inverse.data = name_parts[1][:-1]  # remove the ")"
        root = g.types[entity.root[0]] if entity.root else entity
        if root:  # Set super if exists and is not same as root
            super_ = g.types[entity.root[-1]]
            getattr(
                form,
                str(root.id)).data = super_.id \
                if super_.id != root.id else None
    elif entity.class_.view == 'source':
        form.artifact.data = [
            item.id for item in
            entity.get_linked_entities('P128', inverse=True)]
