from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
import re
import time
from typing import Any, Dict, List, Optional as Optional_Type, Union

from flask import Request, g, session
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import generate_csrf
from wtforms import FloatField, HiddenField
from wtforms.validators import Optional
from wtforms.widgets import HiddenInput

from openatlas import app
from openatlas.forms.admin_forms import ProfileForm
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.util.table import Table
from openatlas.util.util import get_base_table_data, get_file_stats, uc_first


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


class TreeSelect(HiddenInput):  # type: ignore

    def __call__(self, field: TreeField, **kwargs: Any) -> TreeSelect:
        from openatlas.models.node import Node
        selection = ''
        selected_ids = []
        if field.data:
            field.data = field.data[0] if type(field.data) is list else field.data
            selection = g.nodes[int(field.data)].name
            selected_ids.append(g.nodes[int(field.data)].id)
        html = """
            <input id="{name}-button" name="{name}-button" type="text"
                class="table-select {required}"
                onfocus="this.blur()"
                onclick="$('#{name}-modal').modal('show')"
                readonly="readonly"
                value="{selection}"
                placeholder="{change_label}">
            <a href="#" id="{name}-clear" {clear_style} class="{button_class}"
                onclick="clearSelect('{name}');">{clear_label}</a>
            <div id="{name}-modal" class="modal fade" tabindex="-1" role="dialog"
                aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">{title}</h5>
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <input class="tree-filter" id="{name}-tree-search"
                                placeholder="{filter}" type="text">
                            <div id="{name}-tree" style="text-align: left!important;"></div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal">{close_label}</button>
                        </div>
                    </div>
                </div>
            </div>
            <script>
                $(document).ready(function () {{
                    $("#{name}-tree").jstree({{
                        "core" : {{"check_callback": true, "data": {tree_data}}},
                        "search": {{"case_insensitive": true, "show_only_matches": true, "show_only_matches_children": true}},
                        "plugins" : ["search"],
                    }});
                    $("#{name}-tree").on("select_node.jstree", function (e, data) {{
                        selectFromTree("{name}", data.node.id, data.node.text);
                    }});
                    $("#{name}-tree-search").keyup(function() {{
                        if (this.value.length >= {min_chars}) {{
                            $("#{name}-tree").jstree("search", $(this).val());
                        }}
                        else if (this.value.length == 0) {{
                            $("#{name}-tree").jstree("search", $(this).val());
                            $("#{name}-tree").jstree(true).show_all();
                        }}
                    }});
                }});
            </script>""".format(filter=uc_first(_('type to search')),
                                min_chars=session['settings']['minimum_jstree_search'],
                                name=field.id,
                                button_class=app.config['CSS']['button']['secondary'],
                                title=uc_first(g.nodes[int(field.id)].name),
                                change_label=uc_first(_('change')),
                                clear_label=uc_first(_('clear')),
                                close_label=uc_first(_('close')),
                                selection=selection,
                                tree_data=Node.get_tree_data(int(field.id), selected_ids),
                                clear_style='' if selection else ' style="display: none;" ',
                                required=' required' if field.flags.required else '')
        return super(TreeSelect, self).__call__(field, **kwargs) + html


class TreeField(HiddenField):  # type: ignore
    widget = TreeSelect()


class TreeMultiSelect(HiddenInput):  # type: ignore

    def __call__(self, field: TreeField, **kwargs: Any) -> TreeMultiSelect:
        selection = ''
        selected_ids = []
        root = g.nodes[int(field.id)]
        if field.data:
            # Somehow field.data can be a string after a failed form validation, so fix that below
            field.data = ast.literal_eval(field.data) if type(field.data) is str else field.data
            for entity_id in field.data:
                selected_ids.append(entity_id)
                selection += g.nodes[entity_id].name + '<br>'
        html = """
            <span id="{name}-button" class="{button_class}"
                onclick="$('#{name}-modal').modal('show')">{change_label}</span>
            <div id="{name}-selection" style="text-align:left;">{selection}</div>
            <div id="{name}-modal" class="modal fade" tabindex="-1" role="dialog"
                aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">{title}</h5>
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <input class="tree-filter" id="{name}-tree-search"
                                placeholder="{filter}" type="text">
                            <div id="{name}-tree" style="text-align: left!important;"></div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal"
                                onclick="selectFromTreeMulti({name})">{close_label}</button>
                        </div>
                    </div>
                </div>
            </div>
            <script>
                $("#{name}-tree").jstree({{
                    "core" : {{ "check_callback": true, "data": {tree_data} }},
                    "search": {{"case_insensitive": true, "show_only_matches": true, "show_only_matches_children": true}},
                    "plugins": ["search", "checkbox"],
                    "checkbox": {{"three_state": false}}
                }});
                $("#{name}-tree-search").keyup(function(){{
                    if (this.value.length >= {min_chars}) {{
                        $("#{name}-tree").jstree("search", $(this).val());
                    }}
                    else if (this.value.length == 0) {{
                        $("#{name}-tree").jstree("search", $(this).val());
                        $("#{name}-tree").jstree(true).show_all();
                    }}
                }});
            </script>""".format(filter=uc_first(_('type to search')),
                                min_chars=session['settings']['minimum_jstree_search'],
                                name=field.id,
                                button_class=app.config['CSS']['button']['secondary'],
                                title=uc_first(root.name),
                                selection=selection,
                                change_label=uc_first(_('change')),
                                close_label=uc_first(_('close')),
                                tree_data=Node.get_tree_data(int(field.id), selected_ids))
        return super(TreeMultiSelect, self).__call__(field, **kwargs) + html


class TreeMultiField(HiddenField):  # type: ignore
    widget = TreeMultiSelect()


class TableSelect(HiddenInput):  # type: ignore

    def __call__(self, field: TableField, **kwargs: Any) -> TableSelect:
        file_stats = None
        place_fields = ['residence', 'begins_in', 'ends_in', 'place_to', 'place_from']
        class_ = 'place' if field.id in place_fields else field.id
        if class_ == 'place':
            aliases = current_user.settings['table_show_aliases']
            entities = Entity.get_by_system_type('place', nodes=True, aliases=aliases)
        elif class_ == 'reference':
            entities = Entity.get_by_system_type('bibliography') + \
                       Entity.get_by_system_type('edition') + \
                       Entity.get_by_system_type('external reference')
        elif class_ == 'file':
            entities = Entity.get_by_system_type('file')
        else:
            entities = Entity.get_by_menu_item(class_)
        table = Table(Table.HEADERS[class_])

        # Table definitions (aligning)
        if class_ == 'event':
            table.defs = [{'className': 'dt-body-right', 'targets': [3, 4]}]
        elif class_ in ['actor', 'group', 'feature', 'place']:
            table.defs = [{'className': 'dt-body-right', 'targets': [2, 3]}]

        selection = ''
        for entity in entities:
            # Todo: don't show self e.g. at source
            if field.data and entity.id == int(field.data):
                selection = entity.name
            data = get_base_table_data(entity, file_stats)
            if len(entity.aliases) > 0:
                data[0] = """
                    <p>
                        <a onclick="selectFromTable(this,'{name}', {entity_id}, '{entity_name}')"
                            href="#">{entity_name}</a>
                    </p>""".format(name=field.id, entity_id=entity.id, entity_name=entity.name)
            else:
                data[0] = """
                    <a
                        onclick="selectFromTable(this,'{name}', {entity_id}, '{entity_name}')"
                        href="#">{entity_name}</a>
                    """.format(name=field.id, entity_id=entity.id, entity_name=entity.name)
            for i, (id_, alias) in enumerate(entity.aliases.items()):
                if i == len(entity.aliases) - 1:
                    data[0] = ''.join([data[0]] + [alias])
                else:
                    data[0] = ''.join([data[0]] + ['<p>' + alias + '</p>'])
            data.insert(0, """
                <div style="position: relative; top: 10px;" >
                    <div
                        class="btn btn-outline-primary btn-sm"
                        style="position: absolute; top: -30px; height: 27px"
                        onclick="selectFromTable(this,'{name}', {entity_id}, '{entity_name}')">
                            {label}
                    </div>
                </div>
                """.format(name=field.id,
                           entity_id=entity.id,
                           entity_name=entity.name,
                           label=uc_first(_('select'))))
            table.rows.append(data)
        html = """
            <input id="{name}-button" name="{name}-button" class="table-select {required}"
                type="text" placeholder="{change_label}" onfocus="this.blur()" readonly="readonly"
                value="{selection}" onclick="$('#{name}-modal').modal('show');">
            <a href="#" id="{name}-clear" class="{button_class}" {clear_style}
                onclick="clearSelect('{name}');">{clear_label}</a>
            <div id="{name}-modal" class="modal fade" tabindex="-1" role="dialog"
                aria-hidden="true">
                <div class="modal-dialog" role="document" style="max-width: 100%!important;">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">{title}</h5>
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">{table}</div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal">{close_label}</button>
                        </div>
                    </div>
                </div>
            </div>
            <script>
                $('#{name}-modal').on('shown.bs.modal', function () {{
                    $('#{name}_table_filter input').focus();
                }});
            </script>
            """.format(name=field.id,
                       title=uc_first(_(field.id.replace('_', ' '))),
                       button_class=app.config['CSS']['button']['secondary'],
                       change_label=uc_first(_('change')),
                       clear_label=uc_first(_('clear')),
                       close_label=uc_first(_('close')),
                       table=table.display(field.id),
                       selection=selection,
                       clear_style='' if selection else ' style="display: none;" ',
                       required=' required' if field.flags.required else '')
        return super(TableSelect, self).__call__(field, **kwargs) + html


class TableField(HiddenField):  # type: ignore
    widget = TableSelect()


class TableMultiSelect(HiddenInput):  # type: ignore
    """ Table with checkboxes used in a popup for forms."""

    def __call__(self, field: TableField, **kwargs: Any) -> TableMultiSelect:
        if field.data and type(field.data) is str:
            field.data = ast.literal_eval(field.data)
        class_ = field.id if field.id != 'given_place' else 'place'

        # Make checkbox column sortable and show selected on top
        table = Table([''] + Table.HEADERS[class_], order=[[0, 'desc'], [1, 'asc']])

        # Table definitions (ordering and aligning)
        table.defs = [{'orderDataType': 'dom-checkbox', 'targets': 0}]
        if class_ == 'event':
            table.defs.append({'className': 'dt-body-right', 'targets': [4, 5]})
        elif class_ in ['actor', 'group', 'feature', 'place']:
            table.defs.append({'className': 'dt-body-right', 'targets': [3, 4]})

        if class_ == 'place':
            aliases = current_user.settings['table_show_aliases']
            entities = Entity.get_by_system_type('place', nodes=True, aliases=aliases)
        else:
            entities = Entity.get_by_menu_item(class_)

        for entity in entities:
            data = get_base_table_data(entity)
            data[0] = re.sub(re.compile('<a.*?>'), '', data[0])  # Remove links
            data.insert(0, """<input type="checkbox" id="{id}" {checked} value="{name}"
                class="multi-table-select">""".format(
                id=str(entity.id),
                name=entity.name,
                checked='checked = "checked"' if field.data and entity.id in field.data else ''))
            table.rows.append(data)
        selection = [entity.name for entity in entities if field.data and entity.id in field.data]
        html = """
            <span id="{name}-button" class="{button_class}"
                onclick="$('#{name}-modal').modal('show')">{change_label}</span><br>
            <div id="{name}-selection" class="selection" style="text-align:left;">{selection}</div>
            <div id="{name}-modal" class="modal fade" tabindex="-1" role="dialog"
                aria-hidden="true">
                <div class="modal-dialog" role="document" style="max-width: 100%!important;">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">{title}</h5>
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">{table}</div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal"
                                onclick="selectFromTableMulti('{name}')">{close_label}</button>
                        </div>
                    </div>
                </div>
            </div>
            <script>
            </script>""".format(name=field.id,
                                button_class=app.config['CSS']['button']['secondary'],
                                change_label=uc_first(_('change')),
                                close_label=uc_first(_('close')),
                                title=uc_first(_(field.id.replace('_', ' '))),
                                selection='<br>'.join(selection),
                                table=table.display(field.id))
        return super(TableMultiSelect, self).__call__(field, **kwargs) + html


class TableMultiField(HiddenField):  # type: ignore
    widget = TableMultiSelect()


class ValueFloatField(FloatField):  # type: ignore
    pass


def build_move_form(form: Any, node: Node) -> FlaskForm:
    root = g.nodes[node.root[-1]]
    setattr(form, str(root.id), TreeField(str(root.id)))
    form_instance = form(obj=node)

    # Delete custom fields except the ones specified for the form
    delete_list = []  # Can't delete fields in the loop so creating a list for later deletion
    for field in form_instance:
        if type(field) is TreeField and int(field.id) != root.id:
            delete_list.append(field.id)
    for item in delete_list:
        delattr(form_instance, item)

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

    form_instance.selection.choices = choices
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
        return {'name': current_user.real_name,
                'email': current_user.email,
                'show_email': _('on') if current_user.settings['show_email'] else _('off'),
                'newsletter': _('on') if current_user.settings['newsletter'] else _('off')}
    settings = {}
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue
        label = uc_first(field.label.text)
        value = current_user.settings[field.name] if profile else session['settings'][field.name]
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


def set_form_settings(form: Any, profile: Optional[bool] = False) -> None:
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue
        if profile and field.name == 'name':
            field.data = current_user.real_name
            continue
        if profile and field.name == 'email':
            field.data = current_user.email
            continue
        if profile:
            field.data = current_user.settings[field.name]
            continue
        if field.name in ['log_level']:
            field.data = int(session['settings'][field.name])
            continue
        if field.name in ['mail_recipients_feedback', 'file_upload_allowed_extension']:
            field.data = ' '.join(session['settings'][field.name])
            continue
        field.data = session['settings'][field.name]
