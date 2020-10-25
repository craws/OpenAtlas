from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, List, Optional as OptionalType
from wtforms.validators import Optional

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField, HiddenField)
from wtforms.validators import InputRequired

from openatlas.forms.field import TableMultiField, TreeMultiField, TreeField, ValueFloatField
from openatlas.models.entity import Entity
from openatlas.models.node import Node
from openatlas.util.display import uc_first

forms = {'source': ['name', 'description', 'continue'],
         }


def build_form(name: str, entity: OptionalType[Entity] = None) -> FlaskForm:
    class Form(FlaskForm):  # type: ignore
        opened = HiddenField()

    if 'name' in forms[name]:
        setattr(Form, 'name', StringField(validators=[InputRequired()],
                                          render_kw={'autofocus': True}))
    add_fields(name, Form)

    for id_, node in Node.get_nodes_for_form(uc_first(name)).items():
        setattr(Form, str(id_), TreeMultiField(str(id_)) if node.multiple else TreeField(str(id_)))
        if node.value_type:
            add_value_type_fields(Form, node.subs)

    if 'description' in forms[name]:
        label = _('content') if name == 'source' else _('description')
        setattr(Form, 'description', TextAreaField(label))
    setattr(Form, 'save', SubmitField(_('insert')))
    if not entity and 'continue' in forms[name]:
        setattr(Form, 'insert_and_continue', SubmitField(_('insert and continue')))
        setattr(Form, 'continue_', HiddenField())
    return populate_form(Form(obj=entity), entity) if entity else Form()


def populate_form(form: FlaskForm, entity: Entity) -> FlaskForm:
    form.save.label.text = 'update'
    return form


def add_value_type_fields(form: any, subs: List[int]) -> None:
    for sub_id in subs:
        sub = g.nodes[sub_id]
        setattr(form, str(sub.id), ValueFloatField(sub.name, [Optional()]))
        add_value_type_fields(form, sub.subs)


def add_fields(name: str, form: Any) -> None:
    if name == 'source':
        setattr(form, 'information_carrier', TableMultiField())
