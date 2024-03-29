from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from flask import g, render_template, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, StringField, widgets
from wtforms.validators import InputRequired, URL

from openatlas import app
from openatlas.display.table import Table
from openatlas.display.util import get_base_table_data
from openatlas.display.util2 import show_table_icons
from openatlas.forms import base_manager, manager
from openatlas.forms.field import SubmitField, TableMultiField, TreeField
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.views.entity_index import file_preview

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.type import Type


def get_manager(
        class_name: Optional[str] = None,
        entity: Optional[Entity] = None,
        origin: Optional[Entity] = None,
        link_: Optional[Link] = None,
        copy: Optional[bool] = False) -> base_manager.BaseManager:
    name = entity.class_.name if entity and not class_name else class_name
    manager_name = ''.join(i.capitalize() for i in name.split('_'))
    manager_instance = getattr(manager, f'{manager_name}Manager')(
        class_=g.classes['type' if name.startswith('hierarchy') else name],
        entity=entity,
        origin=origin,
        link_=link_,
        copy=copy)
    if request.method != 'POST' and not entity and not link_:
        manager_instance.populate_insert()
    return manager_instance


def get_add_reference_form(class_: str) -> Any:
    class Form(FlaskForm):
        pass

    setattr(Form, class_, TableMultiField(_(class_), [InputRequired()]))
    setattr(Form, 'page', StringField(_('page')))
    setattr(Form, 'save', SubmitField(_('insert')))
    return Form()


def get_table_form(classes: list[str], excluded: list[int]) -> str:
    entities = Entity.get_by_class(classes, types=True, aliases=True)
    table = Table([''] + g.table_headers[classes[0]], order=[[2, 'asc']])
    if classes[0] == 'file' and show_table_icons():
        table.header.insert(1, _('icon'))
    for entity in entities:
        if entity.id not in excluded:
            input_ = f"""
                <input
                    id="selection-{entity.id}"
                    name="values"
                    type="checkbox"
                    value="{entity.id}">"""
            rows = [input_]
            if classes[0] == 'file' and show_table_icons():
                rows.append(file_preview(entity.id))
            rows.extend(get_base_table_data(entity, show_links=False))

            table.rows.append(rows)
    if not table.rows:
        return '<p class="uc-first">' + _('no entries') + '</p>'
    return render_template(
        'forms/form_table.html',
        table=table.display(classes[0]))


def get_move_form(type_: Type) -> Any:
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


def get_vocabs_form() -> Any:  # pragma: no cover
    class Form(FlaskForm):
        base_url = StringField(
            _('base URL'),
            validators=[InputRequired(), URL()])
        endpoint = StringField(_('endpoint'), validators=[InputRequired()])
        vocabs_user = StringField(_('user'))
        save = SubmitField(_('save'))

    return Form()
