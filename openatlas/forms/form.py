from __future__ import annotations  # Needed for Python 4.0 type annotations

import time
from collections import OrderedDict
from typing import Any, Dict, List, Optional as OptionalType

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (HiddenField, StringField, SubmitField, TextAreaField)
from wtforms.validators import InputRequired, Optional

from openatlas import app
from openatlas.forms import date
from openatlas.forms.field import (TableField, TableMultiField, TreeField, TreeMultiField,
                                   ValueFloatField)
from openatlas.models.entity import Entity
from openatlas.models.node import Node
from openatlas.util.display import uc_first

forms = {'source': ['name', 'description', 'continue'],
         'event': ['name', 'date', 'description', 'continue'],
         }


def build_form(name: str,
               entity: OptionalType[Entity] = None,
               code: Optional[str] = None) -> FlaskForm:

    class Form(FlaskForm):  # type: ignore
        opened = HiddenField()

    if 'name' in forms[name]:
        setattr(Form, 'name', StringField(validators=[InputRequired()],
                                          render_kw={'autofocus': True}))
    types = OrderedDict(Node.get_nodes_for_form(uc_first(name)))
    for id_, node in types.items():  # Move base type to top
        if node.name in app.config['BASE_TYPES']:
            types.move_to_end(node.id, last=False)
            break

    for id_, node in types.items():
        setattr(Form, str(id_), TreeMultiField(str(id_)) if node.multiple else TreeField(str(id_)))
        if node.value_type:
            add_value_type_fields(Form, node.subs)
    add_fields(name, Form, code=entity.class_.code if entity else code)
    if 'date' in forms[name]:
        date.add_date_fields(Form)
        setattr(Form, 'validate', date.validate)

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
    if entity and request and request.method == 'GET':
        if hasattr(form, 'begin_year_from'):
            date.populate_dates(form, entity)
        nodes = entity.nodes
        # 4ht parameter entity2 (location) at places with build_form2, is this needed?
        # if isinstance(entity2, Entity):
        #     nodes.update(entity2.nodes)  # type: ignore
        form.opened.data = time.time()
        node_data: Dict[int, List[int]] = {}
        for node, node_value in nodes.items():  # type: ignore
            root = g.nodes[node.root[-1]] if node.root else node
            if root.id not in node_data:
                node_data[root.id] = []
            node_data[root.id].append(node.id)
            if root.value_type:
                getattr(form, str(node.id)).data = node_value
        for root_id, nodes_ in node_data.items():
            if hasattr(form, str(root_id)):
                getattr(form, str(root_id)).data = nodes_
    return form


def add_value_type_fields(form: any, subs: List[int]) -> None:
    for sub_id in subs:
        sub = g.nodes[sub_id]
        setattr(form, str(sub.id), ValueFloatField(sub.name, [Optional()]))
        add_value_type_fields(form, sub.subs)


def add_fields(name: str, form: Any, code: Optional[str] = None) -> None:
    if name == 'source':
        setattr(form, 'information_carrier', TableMultiField())
    elif code == 'E7':
        setattr(form, 'event', TableField(_('sub event of')))
        setattr(form, 'event_id', HiddenField())
        setattr(form, 'place', TableField(_('location')))

# place = TableField(_('location'))
# place_from = TableField(_('from'))
# place_to = TableField(_('to'))
# object = TableMultiField()
# person = TableMultiField()
# event_id = HiddenField()
# given_place = TableMultiField(_('given place'))
