from typing import Union

from flask import g
from flask_wtf import FlaskForm

from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type


def pre_populate_form(
        form: FlaskForm,
        item: Union[Entity, Link]) -> FlaskForm:
    # if isinstance(item, Entity):
    #    populate_reference_systems(form, item)
    if isinstance(item, ReferenceSystem) and item.system:
        form.name.render_kw['readonly'] = 'readonly'
    return form


def populate_update_form(form: FlaskForm, entity: Union[Entity, Type]) -> None:
    if isinstance(entity, Type):
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
