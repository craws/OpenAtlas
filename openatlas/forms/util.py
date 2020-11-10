from __future__ import annotations  # Needed for Python 4.0 type annotations

import time
from typing import Any, Dict, List, Optional as Optional_Type, Union

from flask import Request, g, session
from flask_babel import lazy_gettext as _
from flask_login import current_user
from wtforms.validators import Optional

from openatlas.forms.field import TreeField, TreeMultiField, ValueFloatField
from openatlas.forms.setting import ProfileForm
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.util.display import uc_first


def get_link_type(form: Any) -> Optional_Type[Entity]:
    """ Returns the base type provided by a link form, e.g. involvement between actor and event."""
    for field in form:
        if type(field) is TreeField and field.data:
            return g.nodes[int(field.data)]
    return None


def build_form2(form: Any,
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

    # External references
    # Todo: remove no cover after form refactor
    for name in g.external:  # pragma: no cover
        if name + '_id' in form_instance and not current_user.settings['module_' + name]:
            del form_instance[name + '_id'], form_instance[name + '_precision']

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
        else:  # pragma: no cover
            value = ''  # In case of a missing setting after an update introducing it
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
        if field.name not in session['settings']:  # pragma: no cover
            field.data = ''  # In case of a missing setting after an update introducing it
            continue
        field.data = session['settings'][field.name]
