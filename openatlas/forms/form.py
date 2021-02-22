from __future__ import annotations  # Needed for Python 4.0 type annotations

import time
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Union

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm, widgets
from flask_wtf.csrf import generate_csrf
from wtforms import (BooleanField, FieldList, FileField, HiddenField, SelectField,
                     SelectMultipleField, StringField, SubmitField, TextAreaField, widgets)
from wtforms.validators import InputRequired, Optional as OptionalValidator, URL

from openatlas import app
from openatlas.forms import date
from openatlas.forms.field import (TableField, TableMultiField, TreeField, TreeMultiField,
                                   ValueFloatField)
from openatlas.forms.validation import validate
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.display import get_base_table_data, uc_first
from openatlas.util.table import Table
from openatlas.util.util import get_file_stats

forms = {'actor_actor_relation': ['date', 'description', 'continue'],
         'artifact': ['name', 'date', 'description', 'continue', 'map'],
         'bibliography': ['name', 'description', 'continue'],
         'edition': ['name', 'description', 'continue'],
         'external_reference': ['name', 'description', 'continue'],
         'event': ['name', 'date', 'description', 'continue'],
         'feature': ['name', 'date', 'description', 'continue', 'map'],
         'file': ['name', 'description'],
         'find': ['name', 'date', 'description', 'continue', 'map'],
         'group': ['name', 'alias', 'date', 'description', 'continue'],
         'hierarchy': ['name', 'description'],
         'human_remains': ['name', 'date', 'description', 'continue', 'map'],
         'information_carrier': ['name', 'description', 'continue'],
         'involvement': ['date', 'description', 'continue'],
         'member': ['date', 'description', 'continue'],
         'node': ['name', 'description', 'continue'],
         'legal_body': ['name', 'alias', 'date', 'description', 'continue'],
         'note': ['description'],
         'person': ['name', 'alias', 'date', 'description', 'continue'],
         'place': ['name', 'alias', 'date', 'description', 'continue', 'map'],
         'reference_system': ['name', 'description'],
         'source': ['name', 'description', 'continue'],
         'source_translation': ['name', 'description', 'continue'],
         'stratigraphic_unit': ['name', 'date', 'description', 'continue', 'map']}


def build_form(name: str,
               item: Optional[Entity, Link] = None,  # The entity or link which is to be updated
               code: Optional[str] = None,
               origin: Union[Entity, Node, None] = None,
               location: Optional[Entity] = None) -> FlaskForm:
    # Builds a form for CIDOC CRM entities which has to be dynamic because of types,
    # module settings and class specific fields

    class Form(FlaskForm):  # type: ignore
        opened = HiddenField()
        validate = validate

    if 'name' in forms[name]:  # Set label and validators for name field
        label = _('URL') if name == 'external_reference' else _('name')
        validators = [InputRequired(), URL()] if name == 'external_reference' else [InputRequired()]
        setattr(Form, 'name', StringField(label,
                                          validators=validators,
                                          render_kw={'autofocus': True}))

    if 'alias' in forms[name]:
        setattr(Form, 'alias', FieldList(StringField(''), description=_('tooltip alias')))
    code = item.class_.code if item and isinstance(item, Entity) else code
    add_types(Form, name)
    add_fields(Form, name, code, item, origin)
    add_reference_systems(Form, name)
    if 'date' in forms[name]:
        date.add_date_fields(Form)
    if 'description' in forms[name]:
        label = _('content') if name == 'source' else _('description')
        setattr(Form, 'description', TextAreaField(label))
        if name == 'node':  # Change description field if value type
            node = item if item else origin
            root = g.nodes[node.root[-1]] if node.root else node
            if root.value_type:
                del Form.description
                setattr(Form, 'description', StringField(_('unit')))
    if 'map' in forms[name]:
        setattr(Form, 'gis_points', HiddenField(default='[]'))
        setattr(Form, 'gis_polygons', HiddenField(default='[]'))
        setattr(Form, 'gis_lines', HiddenField(default='[]'))
    add_buttons(Form, name, item, origin)
    if not item or (request and request.method != 'GET'):
        form = Form()
    else:
        form = populate_form(Form(obj=item), item, location)
    customize_labels(name, form, item, origin)
    return form


def populate_form(form: FlaskForm,
                  item: Union[Entity, Link],
                  location: Union[Entity, None]) -> FlaskForm:
    # Dates
    if hasattr(form, 'begin_year_from'):
        date.populate_dates(form, item)

    # Nodes
    nodes: Dict[Node, str] = item.nodes
    if location:  # Needed for administrative unit and historical place nodes
        nodes.update(location.nodes)
    form.opened.data = time.time()
    node_data: Dict[int, List[int]] = {}
    for node, node_value in nodes.items():
        root = g.nodes[node.root[-1]] if node.root else node
        if root.id not in node_data:
            node_data[root.id] = []
        node_data[root.id].append(node.id)
        if root.value_type:
            getattr(form, str(node.id)).data = node_value
    for root_id, nodes_ in node_data.items():
        if hasattr(form, str(root_id)):
            getattr(form, str(root_id)).data = nodes_
    if isinstance(item, Entity):
        populate_reference_systems(form, item)
    return form


def populate_reference_systems(form: FlaskForm, item: Entity) -> None:
    system_links = {link_.domain.id: link_ for link_ in item.get_links('P67', True)
                    if link_.domain.view_name == 'reference_system'}
    for field in form:
        if field.id.startswith('reference_system_id_'):
            system_id = int(field.id.replace('reference_system_id_', ''))
            if system_id in system_links:
                field.data = system_links[system_id].description
                getattr(form, 'reference_system_precision_{id}'.format(
                    id=system_id)).data = str(system_links[system_id].type.id)


def customize_labels(name: str,
                     form: FlaskForm,
                     item: Optional[Entity, Link] = None,
                     origin: Union[Entity, Node, None] = None,) -> None:
    if name == 'source_translation':
        form.description.label.text = _('content')
    if name == 'node':
        node = item if item else origin
        root = g.nodes[node.root[-1]] if node.root else node
        getattr(form, str(root.id)).label.text = 'super'


def add_buttons(form: Any,
                name: str,
                entity: Union[Entity, None],
                origin: Optional[Entity] = None) -> FlaskForm:
    setattr(form, 'save', SubmitField(_('save') if entity else _('insert')))
    if entity:
        return form
    if 'continue' in forms[name] and (
            name in ['involvement', 'find', 'human_remains', 'node'] or not origin):
        setattr(form, 'insert_and_continue', SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
    insert_and_add = uc_first(_('insert and add')) + ' '
    if name == 'place':
        setattr(form, 'insert_and_continue', SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(form, 'insert_continue_sub', SubmitField(insert_and_add + _('feature')))
    elif name == 'feature' and origin and origin.system_type == 'place':
        setattr(form, 'insert_and_continue', SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(form, 'insert_continue_sub', SubmitField(insert_and_add + _('stratigraphic unit')))
    elif name == 'stratigraphic_unit':
        setattr(form, 'insert_and_continue', SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(form, 'insert_continue_sub', SubmitField(insert_and_add + _('find')))
        setattr(form,
                'insert_continue_human_remains',
                SubmitField(insert_and_add + _('human remains')))
    return form


# TODO: this should probably go to a custom field in field.py
def add_reference_systems(form: Any, form_name: str) -> None:
    precisions = [('', '')]
    for id_ in Node.get_hierarchy('External reference match').subs:
        precisions.append((str(g.nodes[id_].id), g.nodes[id_].name))
    for system in g.reference_systems.values():
        forms_ = [form_['name'] for form_ in system.get_forms().values()]
        form_name = form_name.replace('_', ' ').title().replace('Node', 'Type')
        if form_name not in forms_:
            continue
        setattr(form,
                'reference_system_id_{id}'.format(id=system.id),
                StringField(system.name,
                            validators=[OptionalValidator()],
                            description=system.description,
                            render_kw={'autocomplete': 'off', 'placeholder': system.placeholder}))

        setattr(form,
                'reference_system_precision_{id}'.format(id=system.id),
                SelectField(uc_first(_('precision')),
                            choices=precisions,
                            default=system.precision_default_id))


def add_value_type_fields(form: Any, subs: List[int]) -> None:
    for sub_id in subs:
        sub = g.nodes[sub_id]
        setattr(form, str(sub.id), ValueFloatField(sub.name, [OptionalValidator()]))
        add_value_type_fields(form, sub.subs)


def add_types(form: Any, name: str) -> None:
    types = OrderedDict(Node.get_nodes_for_form(g.classes[name].standard_type))
    for node in types.values():  # Move standard type to top
        if node.standard:
            types.move_to_end(node.id, last=False)
            break

    for node in types.values():
        if node.multiple:
            setattr(form, str(node.id), TreeMultiField(str(node.id)))
        else:
            setattr(form, str(node.id), TreeField(str(node.id)))
        if node.value_type:
            add_value_type_fields(form, node.subs)


def add_fields(form: Any,
               name: str,
               code: Union[str, None],
               item: Union[Entity, Node, Link, None],
               origin: Union[Entity, Node, None]) -> None:
    if name == 'actor_actor_relation':
        setattr(form, 'inverse', BooleanField(_('inverse')))
        if not item:
            setattr(form, 'actor', TableMultiField(_('actor'), [InputRequired()]))
            setattr(form, 'relation_origin_id', HiddenField())
    elif name == 'event':
        setattr(form, 'event_id', HiddenField())
        setattr(form, 'event', TableField(_('sub event of')))
        if code == 'E7':
            setattr(form, 'place', TableField(_('location')))
        if code == 'E8':
            setattr(form, 'place', TableField(_('location')))
            setattr(form, 'given_place', TableMultiField(_('given place')))
        elif code == 'E9':
            setattr(form, 'place_from', TableField(_('from')))
            setattr(form, 'place_to', TableField(_('to')))
            setattr(form, 'object', TableMultiField())
            setattr(form, 'person', TableMultiField())
    elif name == 'file' and not item:
        setattr(form, 'file', FileField(_('file'), [InputRequired()]))
    elif name == 'group':
        setattr(form, 'residence', TableField(_('residence')))
        setattr(form, 'begins_in', TableField(_('begins in')))
        setattr(form, 'ends_in', TableField(_('ends in')))
    elif name == 'hierarchy':
        if (code and code == 'custom') or (item and not item.value_type):
            setattr(form, 'multiple', BooleanField(_('multiple'),
                                                   description=_('tooltip hierarchy multiple')))
        setattr(form, 'forms', SelectMultipleField(_('forms'),
                                                   render_kw={'disabled': True},
                                                   description=_('tooltip hierarchy forms'),
                                                   choices=[],
                                                   option_widget=widgets.CheckboxInput(),
                                                   widget=widgets.ListWidget(prefix_label=False),
                                                   coerce=int))
    elif name == 'involvement':
        if not item and origin:
            involved_with = 'actor' if origin.view_name == 'event' else 'event'
            setattr(form, involved_with, TableMultiField(_(involved_with), [InputRequired()]))
        setattr(form, 'activity', SelectField(_('activity')))
    elif name == 'legal_body':
        setattr(form, 'residence', TableField(_('residence')))
        setattr(form, 'begins_in', TableField(_('begins in')))
        setattr(form, 'ends_in', TableField(_('ends in')))
    elif name == 'member' and not item:
        setattr(form, 'member_origin_id', HiddenField())
        setattr(form,
                'actor' if code == 'member' else 'group',
                TableMultiField(_('actor'), [InputRequired()]))
    elif name == 'node':
        setattr(form, 'is_node_form', HiddenField())
        node = item if item else origin
        root = g.nodes[node.root[-1]] if node.root else node
        setattr(form, str(root.id), TreeField(str(root.id)))
        if root.directional:
            setattr(form, 'name_inverse', StringField(_('inverse')))
    elif name == 'person':
        setattr(form, 'residence', TableField(_('residence')))
        setattr(form, 'begins_in', TableField(_('born in')))
        setattr(form, 'ends_in', TableField(_('died in')))
    elif name == 'reference_system':
        setattr(form, 'website_url', StringField(_('website URL'),
                                                 validators=[OptionalValidator(), URL()]))
        setattr(form, 'resolver_url', StringField(_('resolver URL'),
                                                  validators=[OptionalValidator(), URL()]))
        setattr(form, 'placeholder', StringField(_('example ID')))
        precision_node_id = str(Node.get_hierarchy('External reference match').id)
        setattr(form, precision_node_id, TreeField(precision_node_id))
        choices = ReferenceSystem.get_form_choices(item)
        if choices:
            setattr(form, 'forms', SelectMultipleField(
                _('forms'),
                render_kw={'disabled': True},
                choices=choices,
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False),
                coerce=int))
    elif name == 'source':
        setattr(form, 'information_carrier', TableMultiField())


def build_add_reference_form(class_name: str) -> FlaskForm:
    class Form(FlaskForm):  # type: ignore
        pass

    setattr(Form, class_name, TableField(_(class_name), [InputRequired()]))
    setattr(Form, 'page', StringField(_('page')))
    setattr(Form, 'save', SubmitField(uc_first(_('insert'))))
    return Form()


def build_table_form(class_name: str, linked_entities: List[Entity]) -> str:
    """ Returns a form with a list of entities with checkboxes."""
    if class_name == 'file':
        entities = Entity.get_by_system_type('file', nodes=True)
    elif class_name == 'place':
        entities = Entity.get_by_system_type('place', nodes=True, aliases=True)
    else:
        entities = Entity.get_by_menu_item(class_name)

    linked_ids = [entity.id for entity in linked_entities]
    table = Table([''] + Table.HEADERS[class_name], order=[[1, 'asc']])
    file_stats = get_file_stats() if class_name == 'file' else None
    for entity in entities:
        if entity.id in linked_ids:
            continue  # Don't show already linked entries
        input_ = '<input id="selection-{id}" name="values" type="checkbox" value="{id}">'.format(
            id=entity.id)
        table.rows.append([input_] + get_base_table_data(entity, file_stats))
    if not table.rows:
        return uc_first(_('no entries'))
    return """
        <form class="table" id="checkbox-form" method="post">
            <input id="csrf_token" name="csrf_token" type="hidden" value="{token}">
            <input id="checkbox_values" name="checkbox_values" type="hidden">
            {table}
            <input id="save" class="{class_}" name="save" type="submit" value="{link}">
        </form>""".format(link=uc_first(_('link')),
                          token=generate_csrf(),
                          class_=app.config['CSS']['button']['primary'],
                          table=table.display(class_name))


def build_move_form(node: Node) -> FlaskForm:
    class Form(FlaskForm):  # type: ignore
        is_node_form = HiddenField()
        checkbox_values = HiddenField()
        selection = SelectMultipleField('',
                                        [InputRequired()],
                                        coerce=int,
                                        option_widget=widgets.CheckboxInput(),
                                        widget=widgets.ListWidget(prefix_label=False))
        save = SubmitField(uc_first(_('move')))

    root = g.nodes[node.root[-1]]
    setattr(Form, str(root.id), TreeField(str(root.id)))
    form = Form(obj=node)
    choices = []
    if root.class_.code == 'E53':
        for entity in node.get_linked_entities('P89', True):
            place = entity.get_linked_entity('P53', True)
            if place:
                choices.append((entity.id, place.name))
    elif root.name in app.config['PROPERTY_TYPES']:
        for row in Link.get_entities_by_node(node):
            domain = Entity.get_by_id(row.domain_id)
            range_ = Entity.get_by_id(row.range_id)
            choices.append((row.id, domain.name + ' - ' + range_.name))
    else:
        for entity in node.get_linked_entities('P2', True):
            choices.append((entity.id, entity.name))
    form.selection.choices = choices
    return form
