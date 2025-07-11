from collections import OrderedDict
from typing import Any, Optional

from flask import g
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import FieldList, HiddenField, StringField, TextAreaField
from wtforms.validators import InputRequired

from openatlas.display.util2 import is_authorized
from openatlas.forms.add_fields import add_value_type_fields
from openatlas.forms.field import (
    RemovableListField, SubmitField, TreeField, TreeMultiField,
    ValueTypeRootField)
from openatlas.models.entity import Entity
from openatlas.models.openatlas_class import OpenatlasClass


def get_entity_form(entity: Entity, origin: Optional[Entity] = None) -> Any:
    class Form(FlaskForm):
        pass

    add_name_fields(entity, Form)
    add_types(entity.class_, Form)
    add_buttons(entity, Form)
    form: Any = Form(obj=entity)
    return form


def add_name_fields(entity: Entity, form: Any) -> None:
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


def add_buttons(entity: Entity, form: Any) -> None:
    setattr(form, 'save', SubmitField(_('save') if entity.id else _('save')))
    if not entity.id: # and 'continue' in self.fields:
        setattr(
            form,
            'insert_and_continue',
            SubmitField(_('insert and continue')))
        setattr(form, 'continue_', HiddenField())


def add_types(class_: OpenatlasClass, form: Any) -> None:
    if class_.hierarchies:
        types = OrderedDict({id_: g.types[id_] for id_ in class_.hierarchies})
        if class_.standard_type_id in types:
            types.move_to_end(class_.standard_type_id, last=False)
        for type_ in types.values():
            class AddDynamicType(FlaskForm):
                pass

            setattr(AddDynamicType, 'name-dynamic', StringField(_('name')))
            setattr(
                AddDynamicType,
                f'{type_.id}-dynamic',
                TreeField(str(type_.id), type_id=str(type_.id)))
            setattr(
                AddDynamicType,
                'description-dynamic',
                TextAreaField(_('description')))
            add_form = AddDynamicType() if is_authorized('editor') else None
            if add_form:
                getattr(add_form, f'{type_.id}-dynamic').label.text = 'super'
            validators = [InputRequired()] if type_.required else []
            if type_.category == 'value':
                setattr(
                    form,
                    str(type_.id),
                    ValueTypeRootField(type_.name, type_.id))
                add_value_type_fields(form, type_.subs)
            elif type_.multiple:
                setattr(
                    form,
                    str(type_.id),
                    TreeMultiField(str(type_.id), validators, form=add_form))
            else:
                setattr(
                    form,
                    str(type_.id),
                    TreeField(str(type_.id), validators, form=add_form))


