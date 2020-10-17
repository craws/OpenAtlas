from __future__ import annotations  # Needed for Python 4.0 type annotations

import time
from typing import Any, Dict, List, Optional as Optional_Type, Union

from flask import Request, g, session
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import generate_csrf
from wtforms.validators import Optional

from openatlas import app
from openatlas.forms.form import ProfileForm
from openatlas.forms.field import TreeField, TreeMultiField, ValueFloatField
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.util.table import Table
from openatlas.util.util import get_file_stats
from openatlas.util.display import get_base_table_data, uc_first


def get_link_type(form: Any) -> Optional_Type[Entity]:
    """ Returns the base type provided by a link form, e.g. involvement between actor and event."""
    for field in form:
        if type(field) is TreeField and field.data:
            return g.nodes[int(field.data)]
    return None


def build_form(form: Any,
               form_name: str,
               selected_object: Union[Entity, Link, None] = None,
               request_origin: Optional_Type[Request] = None,
               entity2: Optional_Type[Entity] = None) -> Any:
    def add_value_type_fields(subs: List[int]) -> None:
        for sub_id in subs:
            sub = g.nodes[sub_id]
            setattr(form, str(sub.id), ValueFloatField(sub.name, [Optional()]))
            add_value_type_fields(sub.subs)

    # Add custom fields
    custom_list = []
    for id_, node in Node.get_nodes_for_form(form_name).items():
        custom_list.append(id_)
        setattr(form, str(id_), TreeMultiField(str(id_)) if node.multiple else TreeField(str(id_)))
        if node.value_type:
            add_value_type_fields(node.subs)
    form_instance = form(obj=selected_object)

    # Delete custom fields except the ones specified for the form
    delete_list = []  # Can't delete fields in the loop so creating a list for later deletion
    for field in form_instance:
        if type(field) in (TreeField, TreeMultiField) and int(field.id) not in custom_list:
            delete_list.append(field.id)
    for item in delete_list:
        delattr(form_instance, item)

    # GeoNames
    if 'geonames_id' in form_instance and not current_user.settings['module_geonames']:
        del form_instance.geonames_id, form_instance.geonames_precision

    # Wikidata
    if 'wikidata_id' in form_instance and not current_user.settings['module_wikidata']:
        delattr(form_instance, 'wikidata_id')

    # Set field data if available and only if it's a GET request
    if selected_object and request_origin and request_origin.method == 'GET':
        from openatlas.forms.date import DateForm
        # Important to use isinstance instead type check, because can be a sub type (e.g. ActorForm)
        if isinstance(form_instance, DateForm):
            form_instance.populate_dates(selected_object)
        nodes = selected_object.nodes
        if isinstance(entity2, Entity):
            nodes.update(entity2.nodes)  # type: ignore
        if hasattr(form, 'opened'):
            form_instance.opened.data = time.time()
        node_data: Dict[int, List[int]] = {}
        for node, node_value in nodes.items():  # type: ignore
            root = g.nodes[node.root[-1]] if node.root else node
            if root.id not in node_data:
                node_data[root.id] = []
            node_data[root.id].append(node.id)
            if root.value_type:
                getattr(form_instance, str(node.id)).data = node_value
        for root_id, nodes_ in node_data.items():
            if hasattr(form_instance, str(root_id)):
                getattr(form_instance, str(root_id)).data = nodes_
    return form_instance


def build_node_form(form: Any,
                    node_: Node,
                    request_origin: Optional_Type[Request] = None) -> FlaskForm:
    if not request_origin:
        root = node_
        node = None
    else:
        node = node_
        root = g.nodes[node_.root[-1]]
    setattr(form, str(root.id), TreeField(str(root.id)))
    form_instance = form(obj=node)
    if not root.directional:
        del form_instance.name_inverse
    if root.value_type:
        del form_instance.description
    else:
        del form_instance.unit

    # Delete custom fields except the one specified for the form
    delete_list = []  # Can't delete fields in the loop so creating a list for later deletion
    for field in form_instance:
        if type(field) is TreeField and int(field.id) != root.id:
            delete_list.append(field.id)
    for item in delete_list:
        delattr(form_instance, item)

    # Set field data if available and only if it's a GET request
    if node and request_origin and request_origin.method == 'GET':
        name_parts = node.name.split(' (')
        form_instance.name.data = name_parts[0]
        if root.directional and len(name_parts) > 1:
            form_instance.name_inverse.data = name_parts[1][:-1]  # remove the ")" from 2nd part
        if root.value_type:
            form_instance.unit.data = node.description
        else:
            form_instance.description.data = node.description
        if root:  # Set super if exists and is not same as root
            super_ = g.nodes[node.root[0]]
            getattr(form_instance, str(root.id)).data = super_.id if super_.id != root.id else None
    return form_instance


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


def get_form_settings(form: Any, profile: bool = False) -> Dict[str, str]:
    if isinstance(form, ProfileForm):
        return {_('name'): current_user.real_name,
                _('email'): current_user.email,
                _('show email'): _('on') if current_user.settings['show_email'] else _('off'),
                _('newsletter'): _('on') if current_user.settings['newsletter'] else _('off')}
    settings = {}
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue
        label = uc_first(field.label.text)
        if profile and field.name in current_user.settings:
            value = current_user.settings[field.name]
        elif field.name in session['settings']:
            value = session['settings'][field.name]
        else:
            value = ''
        if field.type in ['StringField', 'IntegerField']:
            settings[label] = value
        if field.type == 'BooleanField':
            settings[label] = _('on') if value else _('off')
        if field.type == 'SelectField':
            if type(value) is str and value.isdigit():
                value = int(value)
            settings[label] = dict(field.choices).get(value)
        if field.name in ['mail_recipients_feedback', 'file_upload_allowed_extension']:
            settings[label] = ' '.join(value)
    return settings


def set_form_settings(form: Any, profile: bool = False) -> None:
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue
        if profile and field.name == 'name':
            field.data = current_user.real_name
            continue
        if profile and field.name == 'email':
            field.data = current_user.email
            continue
        if profile and field.name in current_user.settings:
            field.data = current_user.settings[field.name]
            continue
        if field.name in ['log_level']:
            field.data = int(session['settings'][field.name])
            continue
        if field.name in ['mail_recipients_feedback', 'file_upload_allowed_extension']:
            field.data = ' '.join(session['settings'][field.name])
            continue
        if field.name not in session['settings']:
            field.data = ''
            continue
        field.data = session['settings'][field.name]
