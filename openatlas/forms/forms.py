# Created by Alexander Watzinger and others. Please see README.md for licensing information
import ast
import re
import time
from typing import Optional as Optional_Type

from flask import g, session
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import Form
from wtforms import FloatField, HiddenField
from wtforms.validators import Optional
from wtforms.widgets import HiddenInput

from openatlas import app
from openatlas.forms.date import DateForm
from openatlas.models.entity import Entity, EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.models.node import NodeMapper
from openatlas.util.table import Table
from openatlas.util.util import get_base_table_data, get_file_stats, truncate_string, uc_first


def get_link_type(form) -> Optional_Type[Entity]:
    """ Returns the link type provided by a link form, e.g. involvement between actor and event."""
    for field in form:
        if type(field) is TreeField and field.data:
            return g.nodes[int(field.data)]


def build_form(form, form_name, entity=None, request_origin=None, entity2=None) -> Form:
    """ The entity parameter can also be a link."""
    # Add custom fields
    custom_list = []

    def add_value_type_fields(subs) -> None:
        for sub_id in subs:
            sub = g.nodes[sub_id]
            setattr(form, str(sub.id), ValueFloatField(sub.name, [Optional()]))
            add_value_type_fields(sub.subs)

    for id_, node in NodeMapper.get_nodes_for_form(form_name).items():
        custom_list.append(id_)
        setattr(form, str(id_), TreeMultiField(str(id_)) if node.multiple else TreeField(str(id_)))
        if node.value_type:
            add_value_type_fields(node.subs)

    form_instance = form(obj=entity)

    # Delete custom fields except the ones specified for the form
    delete_list = []  # Can't delete fields in the loop so creating a list for later deletion
    for field in form_instance:
        if type(field) in (TreeField, TreeMultiField) and int(field.id) not in custom_list:
            delete_list.append(field.id)
    for item in delete_list:
        delattr(form_instance, item)

    # Set field data if available and only if it's a GET request
    if entity and request_origin and request_origin.method == 'GET':
        # Important to use isinstance instead type check, because can be a sub type (e.g. ActorForm)
        if isinstance(form_instance, DateForm):
            form_instance.populate_dates(entity)
        nodes = entity.nodes
        if entity2:
            nodes.update(entity2.nodes)
        if hasattr(form, 'opened'):
            form_instance.opened.data = time.time()
        node_data = {}  # type: dict
        for node, node_value in nodes.items():
            root = g.nodes[node.root[-1]] if node.root else node
            if root.id not in node_data:
                node_data[root.id] = []
            node_data[root.id].append(node.id)
            if root.value_type:
                getattr(form_instance, str(node.id)).data = node_value
        for root_id, nodes in node_data.items():
            if hasattr(form_instance, str(root_id)):
                getattr(form_instance, str(root_id)).data = nodes
    return form_instance


def build_move_form(form, node) -> Form:
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
        for row in LinkMapper.get_entities_by_node(node):
            domain = EntityMapper.get_by_id(row.domain_id)
            range_ = EntityMapper.get_by_id(row.range_id)
            choices.append((row.id, domain.name + ' - ' + range_.name))
    else:
        for entity in node.get_linked_entities('P2', True):
            choices.append((entity.id, entity.name))

    form_instance.selection.choices = choices
    return form_instance


def build_node_form(form, node, request_origin=None):
    if not request_origin:
        root = node
        node = None
    else:
        root = g.nodes[node.root[-1]]
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


class TreeSelect(HiddenInput):

    def __call__(self, field, **kwargs):
        from openatlas.models.node import NodeMapper
        selection = ''
        selected_ids = []
        if field.data:
            field.data = field.data[0] if type(field.data) is list else field.data
            selection = g.nodes[int(field.data)].name
            selected_ids.append(g.nodes[int(field.data)].id)
        html = """
            <input id="{name}-button" name="{name}-button" type="text"
                class="table-select {required}" onfocus="this.blur()"
                readonly="readonly" value="{selection}" placeholder="{change_label}" />
            <a id="{name}-clear" {clear_style} class="button"
                onclick="clearSelect('{name}');">{clear_label}</a>
            <div id="{name}-overlay" class="overlay">
                <div id="{name}-dialog" class="overlay-container">
                    <input class="tree-filter" id="{name}-tree-search" placeholder="{filter}" />
                    <div id="{name}-tree"></div>
                </div>
            </div>
            <script>
                $(document).ready(function () {{
                    createOverlay("{name}","{title}",false,);
                    $("#{name}-tree").jstree({{
                        "core" : {{"check_callback" : true, 'data':[{tree_data}]}},
                        "search": {{"case_insensitive": true, "show_only_matches": true}},
                        "plugins" : ["search"],
                    }});
                    $("#{name}-tree").on("select_node.jstree", function (e, data) {{
                        selectFromTree("{name}", data.node.id, data.node.text);
                    }});
                    $("#{name}-tree-search").keyup(function() {{
                        if (this.value.length >= {min_chars}) {{
                            $("#{name}-tree").jstree("search", $(this).val());
                        }}
                    }});
                }});
            </script>""".format(filter=uc_first(_('type to search')),
                                min_chars=session['settings']['minimum_jstree_search'],
                                name=field.id,
                                title=g.nodes[int(field.id)].name,
                                change_label=uc_first(_('change')),
                                clear_label=uc_first(_('clear')),
                                selection=selection,
                                tree_data=NodeMapper.get_tree_data(int(field.id), selected_ids),
                                clear_style='' if selection else ' style="display: none;" ',
                                required=' required' if field.flags.required else '')
        return super(TreeSelect, self).__call__(field, **kwargs) + html


class TreeField(HiddenField):
    widget = TreeSelect()


class TreeMultiSelect(HiddenInput):

    def __call__(self, field, **kwargs):
        selection = ''
        selected_ids = []
        root = g.nodes[int(field.id)]
        if field.data:
            # Somehow field.data can be a string after a failed form validation, so fix that below
            field.data = ast.literal_eval(field.data) if type(field.data) is str else field.data
            for entity_id in field.data:
                selected_ids.append(entity_id)
                selection += g.nodes[entity_id].name + '<br />'
        html = """
            <span id="{name}-button" class="button">{change_label}</span>
            <div id="{name}-selection" style="text-align:left;">{selection}</div>
            <div id="{name}-overlay" class="overlay">
               <div id="{name}-dialog" class="overlay-container">
                   <input class="tree-filter" id="{name}-tree-search" placeholder="{filter}" />
                   <div id="{name}-tree"></div>
               </div>
            </div>
            <script>
                createOverlay("{name}", "{title}", true, "tree");
                $("#{name}-tree").jstree({{
                    "core" : {{ "check_callback" : true, 'data':[{tree_data}] }},
                    "search": {{"case_insensitive": true, "show_only_matches": true}},
                    "plugins": ["search", "checkbox"],
                    "checkbox": {{"three_state": false}}
                }});
                $("#{name}-tree-search").keyup(function(){{
                    if (this.value.length >= {min_chars}) {{
                        $("#{name}-tree").jstree("search", $(this).val());
                    }}
                }});
            </script>""".format(filter=uc_first(_('type to search')),
                                min_chars=session['settings']['minimum_jstree_search'],
                                name=field.id,
                                title=root.name,
                                selection=selection,
                                change_label=uc_first(_('change')),
                                tree_data=NodeMapper.get_tree_data(int(field.id), selected_ids))
        return super(TreeMultiSelect, self).__call__(field, **kwargs) + html


class TreeMultiField(HiddenField):
    widget = TreeMultiSelect()


class TableSelect(HiddenInput):

    def __call__(self, field, **kwargs):
        file_stats = None
        class_ = 'place' if field.id in ['residence', 'begins_in', 'ends_in'] else field.id
        if class_ == 'place':
            aliases = current_user.settings['table_show_aliases']
            entities = EntityMapper.get_by_system_type('place', nodes=True, aliases=aliases)
        elif class_ == 'reference':
            entities = EntityMapper.get_by_system_type('bibliography') + \
                       EntityMapper.get_by_system_type('edition') + \
                       EntityMapper.get_by_system_type('external reference')
        elif class_ == 'file':
            entities = EntityMapper.get_display_files()
            file_stats = get_file_stats()
        else:
            entities = EntityMapper.get_by_codes(class_)
        selection = ''
        table = Table(Table.HEADERS[class_])
        for entity in entities:
            # Todo: don't show self e.g. at source
            if field.data and entity.id == int(field.data):
                selection = entity.name
            data = get_base_table_data(entity, file_stats)
            data[0] = """<a onclick="selectFromTable(this,'{name}', {entity_id})">{entity_name}</a>
                        """.format(name=field.id,
                                   entity_id=entity.id,
                                   entity_name=truncate_string(entity.name, span=False))
            data[0] = '<br />'.join([data[0]] + [
                truncate_string(alias) for id_, alias in entity.aliases.items()])
            table.rows.append(data)
        html = """
            <input id="{name}-button" name="{name}-button" class="table-select {required}"
                type="text" placeholder="{change_label}" onfocus="this.blur()" readonly="readonly"
                value="{selection}">
            <a id="{name}-clear" class="button" {clear_style}
                onclick="clearSelect('{name}');">{clear_label}</a>
            <div id="{name}-overlay" class="overlay">
            <div id="{name}-dialog" class="overlay-container">{table}</div></div>
            <script>$(document).ready(function () {{createOverlay("{name}", "{title}");}});</script>
            """.format(name=field.id,
                       title=_(field.id.replace('_', ' ')),
                       change_label=uc_first(_('change')),
                       clear_label=uc_first(_('clear')),
                       table=table.display(field.id),
                       selection=selection,
                       clear_style='' if selection else ' style="display: none;" ',
                       required=' required' if field.flags.required else '')
        return super(TableSelect, self).__call__(field, **kwargs) + html


class TableField(HiddenField):
    widget = TableSelect()


class TableMultiSelect(HiddenInput):
    """ Table with checkboxes used in a popup for forms."""

    def __call__(self, field, **kwargs):
        if field.data and type(field.data) is str:
            field.data = ast.literal_eval(field.data)
        selection = ''
        class_ = field.id if field.id != 'given_place' else 'place'
        headers_len = str(len(Table.HEADERS[class_]))

        # Make checkbox column sortable and show selected on top
        table = Table(Table.HEADERS[class_], order='[[' + headers_len + ', "asc"], [0, "asc"]]',
                      defs='[{"orderDataType": "dom-checkbox", "targets":' + headers_len + '}]')

        if class_ == 'place':
            aliases = current_user.settings['table_show_aliases']
            entities = EntityMapper.get_by_system_type('place', nodes=True, aliases=aliases)
        else:
            entities = EntityMapper.get_by_codes(class_)
        for entity in entities:
            selection += entity.name + '<br/>' if field.data and entity.id in field.data else ''
            data = get_base_table_data(entity)
            data[0] = re.sub(re.compile('<a.*?>'), '', data[0])  # Remove links
            data.append("""<input type="checkbox" id="{id}" {checked} value="{name}"
                class="multi-table-select">""".format(
                id=str(entity.id),
                name=entity.name,
                checked='checked = "checked"' if field.data and entity.id in field.data else ''))
            table.rows.append(data)
        html = """
            <span id="{name}-button" class="button">{change_label}</span><br />
            <div id="{name}-selection" class="selection" style="text-align:left;">{selection}</div>
            <div id="{name}-overlay" class="overlay">
            <div id="{name}-dialog" class="overlay-container">{table}</div></div>
            <script>
                $(document).ready(function () {{createOverlay("{name}", "{title}", true);}});
            </script>""".format(name=field.id,
                                change_label=uc_first(_('change')),
                                title=_(field.id.replace('_', ' ')),
                                selection=selection,
                                table=table.display(field.id))
        return super(TableMultiSelect, self).__call__(field, **kwargs) + html


class TableMultiField(HiddenField):
    widget = TableMultiSelect()


class ValueFloatField(FloatField):
    pass
