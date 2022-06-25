from typing import Any, Optional, Union

from flask import g
from flask_wtf import FlaskForm

from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type


def pre_populate_form(
        form: FlaskForm,
        item: Union[Entity, Link],
        location: Optional[Entity]) -> FlaskForm:
    # if isinstance(item, Entity):
    #    populate_reference_systems(form, item)
    if isinstance(item, ReferenceSystem) and item.system:
        form.name.render_kw['readonly'] = 'readonly'
    return form


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
    elif entity.class_.name in ['artifact', 'human_remains']:
        owner = entity.get_linked_entity('P52')
        form.actor.data = owner.id if owner else None
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
