from typing import Optional

from flask import g, render_template, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, StringField, widgets
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.table import Table
from openatlas.display.util import get_base_table_data
from openatlas.forms import base_manager, manager
from openatlas.forms.field import SubmitField, TableMultiField, TreeField
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.type import Type


def get_manager(
        class_name: Optional[str] = None,
        entity: Optional[Entity] = None,
        origin: Optional[Entity] = None,
        link_: Optional[Link] = None) -> base_manager.BaseManager:
    name = entity.class_.name if entity and not class_name else class_name
    manager_name = ''.join(i.capitalize() for i in name.split('_'))
    manager_instance = getattr(manager, f'{manager_name}Manager')(
        class_=g.classes['type' if name.startswith('hierarchy') else name],
        entity=entity,
        origin=origin,
        link_=link_)
    if request.method != 'POST' and not entity and not link_:
        manager_instance.populate_insert()
    return manager_instance


def get_add_reference_form(class_: str) -> FlaskForm:
    class Form(FlaskForm):
        pass

    setattr(Form, class_, TableMultiField(_(class_), [InputRequired()]))
    setattr(Form, 'page', StringField(_('page')))
    setattr(Form, 'save', SubmitField(_('insert')))
    return Form()


def get_table_form(class_: str, linked_entities: list[Entity]) -> str:
    entities = Entity.get_by_view(class_, types=True, aliases=True)
    linked_ids = [entity.id for entity in linked_entities]
    table = Table([''] + g.table_headers[class_], order=[[1, 'asc']])
    for entity in entities:
        if entity.id not in linked_ids:
            input_ = f"""
                <input
                    id="selection-{entity.id}"
                    name="values"
                    type="checkbox"
                    value="{entity.id}">"""
            table.rows.append(
                [input_] + get_base_table_data(entity, show_links=False))
    if not table.rows:
        return '<span class="uc-first">' + _('no entries') + '</span>'
    return render_template(
        'forms/form_table.html',
        table=table.display(class_))


def get_move_form(type_: Type) -> FlaskForm:
    class Form(FlaskForm):
        is_type_form = HiddenField()
        checkbox_values = HiddenField()
        selection = SelectMultipleField(
            '',
            [InputRequired()],
            coerce=int,
            option_widget=widgets.CheckboxInput(),
            widget=widgets.ListWidget(prefix_label=False))
        save = SubmitField(_('move entities'))

    root = g.types[type_.root[0]]
    setattr(Form, str(root.id), TreeField(str(root.id)))
    choices = []
    if root.class_.name == 'administrative_unit':
        for entity in type_.get_linked_entities('P89', True):
            place = entity.get_linked_entity('P53', True)
            if place:
                choices.append((entity.id, place.name))
    elif root.name in app.config['PROPERTY_TYPES']:
        for row in Link.get_links_by_type(type_):
            domain = Entity.get_by_id(row['domain_id'])
            range_ = Entity.get_by_id(row['range_id'])
            choices.append((row['id'], domain.name + ' - ' + range_.name))
    else:
        for entity in type_.get_linked_entities('P2', True):
            choices.append((entity.id, entity.name))
    form = Form(obj=type_)
    form.selection.choices = choices
    return form
