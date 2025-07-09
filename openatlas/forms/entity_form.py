from typing import Any, Optional

from flask import g
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import FieldList, FileField, HiddenField, StringField
from wtforms.validators import InputRequired

from openatlas.forms.field import RemovableListField, SubmitField, TreeField
from openatlas.models.entity import Entity


def get_entity_form(entity: Entity, origin: Optional[Entity] = None) -> Any:
    class Form(FlaskForm):
        pass

    if 'name' in entity.class_.attributes:
        setattr(
            Form,
            'name',
            StringField(
                _('name'),
                validators=[InputRequired()],
                render_kw={'autofocus': True}))
    if 'alias' in entity.class_.attributes:
        setattr(Form, 'alias', FieldList(RemovableListField()))

    #if entity.class_.name == 'file' and not entity.id:
    #    setattr(Form, 'file', FileField(validators=[InputRequired()]))
    #if entity.class_.name in ['place', 'type']:
    #    root = origin or g.types[entity.root[0]]
    #    setattr(Form, root.name, TreeField('Super'))
    #    if entity.class_.name == 'place':
    #        setattr(Form, 'latitude', StringField())
    #        setattr(Form, 'longitude', StringField())
    add_buttons()
    form: Any = Form(obj=entity)
    return form


def add_buttons(entity: Entity, form_class: Any) -> None:
    setattr(
        form_class,
        'save',
        SubmitField(_('save') if entity.id else _('save')))
    if not entity.id: # and 'continue' in self.fields:
        setattr(
            form_class,
            'insert_and_continue',
            SubmitField(_('insert and continue')))
        setattr(form_class, 'continue_', HiddenField())


