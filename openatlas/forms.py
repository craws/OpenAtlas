# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import IntegerField, StringField, BooleanField, HiddenField
from wtforms.validators import NumberRange, Optional
from wtforms.widgets import HiddenInput

import openatlas
from openatlas.util import util
from openatlas.util.filters import pager
from openatlas.util.util import uc_first


def add_form_fields(form, form_name):
    for id_, node in openatlas.models.node.NodeMapper.get_nodes_for_form(form_name).items():
        if node.multiple:
            field = TreeMultiField(str(id_))
            setattr(form, str(id_), field)
        else:
            field = TreeField(str(id_))
            setattr(form, str(id_), field)


class TreeSelect(HiddenInput):

    def __call__(self, field, **kwargs):
        selection = openatlas.nodes[int(field.data)].name if field.data else ''
        html = """
            <input id="{name}-button" name="{name}-button" type="text" class="table-select {required}"
                onfocus="this.blur()" readonly="readonly" value="{selection}" placeholder="Select" />
            <a id="{name}-clear" {clear_style} class="button" onclick="clearSelect('{name}');">Clear</a>
            <div id="{name}-overlay" class="overlay">
                <div id="{name}-dialog" class="overlay-container">
                    <input class="tree-filter" id="{name}-tree-search" placeholder="Filter" />
                    <div id="{name}-tree"></div>
                </div>
            </div>
            <script>
                $(document).ready(function () {{
                    createOverlay("{name}","{title}");
                    $("#{name}-tree").jstree({{
                        "search": {{"case_insensitive": true, "show_only_matches": true}},
                        "plugins" : ["search"],{tree}
                    }});
                    $("#{name}-tree").on("select_node.jstree", function (e, data) {{
                        selectFromTree("{name}", data.node.id, data.node.text);
                    }});
                    $("#{name}-tree-search").keyup(function() {{
                        $("#{name}-tree").jstree("search", $(this).val());
                    }});
                }});
            </script>
        """.format(
            name=field.id,
            title=openatlas.nodes[int(field.id)].name,
            selection=selection,
            tree=openatlas.models.node.NodeMapper.get_tree_data(int(field.id)),
            clear_style='' if selection else ' style="display: none;" ',
            required=' required' if field.flags.required else '')
        return super(TreeSelect, self).__call__(field, **kwargs) + html


class TreeField(HiddenField):
    widget = TreeSelect()


class TreeMultiSelect(HiddenInput):

    def __call__(self, field, **kwargs):
        selection = ''
        if field.data:
            for entity_id in field.data:
                selection += openatlas.nodes[entity_id].name + '<br />'
        html = """
            <span id="{name}-button" class="button">Change</span>
            <div id="{name}-selection" style="text-align:left;">{selection}</div>
            <div id="{name}-overlay" class="overlay">
               <div id="{name}-dialog" class="overlay-container">
                   <input class="tree-filter" id="{name}-tree-search" placeholder="Filter" />
                   <div id="{name}-tree"></div>
               </div>
            </div>
            <script>
                createOverlay("{name}", "{title}", true, "tree");
                $("#{name}-tree").jstree({{
                    "search": {{"case_insensitive": true, "show_only_matches": true}},
                    "plugins": ["search", "checkbox"],
                    "checkbox": {{"three_state": false}},{tree}
                }});
                $("#{name}-tree-search").keyup(function(){{
                    $("#{name}-tree").jstree("search", $(this).val());
                }});
            </script>
        """.format(
            name=field.id,
            title=openatlas.nodes[int(field.id)].name,
            selection=selection,
            tree=openatlas.models.node.NodeMapper.get_tree_data(int(field.id)))
        return super(TreeMultiSelect, self).__call__(field, **kwargs) + html


class TreeMultiField(HiddenField):
    widget = TreeMultiSelect()


class TableSelect(HiddenInput):
    def __call__(self, field, **kwargs):
        selection = ''
        table = {'name': field.id, 'header': ['name', 'type', 'info'], 'data': []}
        for entity in openatlas.models.entity.EntityMapper.get_by_class(field.id.split('_')[0]):
            # To do: don't show self e.g. at relations
            if field.data and entity.id == int(field.data):
                selection = entity.name
            table['data'].append([
                """<a onclick="selectFromTable(this,'{name}', {entity_id})">{entity_name}</a>""".format(
                    name=field.id, entity_id=entity.id, entity_name=entity.name),
                ', '.join(map(str, entity.types[field.id])) if field.id in entity.types else '',
                util.truncate_string(entity.info)
            ])
        html = """
            <input id="{name}-button" name="{name}-button" class="table-select {required}" type="text"
                placeholder="Select" onfocus="this.blur()" readonly="readonly" value="{selection}"> 
            <a id="{name}-clear" class="button" {clear_style} onclick="clearSelect('{name}');">Clear</a>
            <div id="{name}-overlay" class="overlay">
            <div id="{name}-dialog" class="overlay-container">{pager}</div></div>
            <script>$(document).ready(function () {{createOverlay("{name}");}});</script>
        """.format(
            name=field.id,
            pager=pager(None, table),
            selection=selection,
            clear_style='' if selection else ' style="display: none;" ',
            required=' required' if field.flags.required else '')
        return super(TableSelect, self).__call__(field, **kwargs) + html


class TableField(HiddenField):
    widget = TableSelect()


class TableMultiSelect(HiddenInput):

    def __call__(self, field, **kwargs):
        field.data = ast.literal_eval(field.data) if field.data and isinstance(field.data, str) else field.data
        selection = ''
        table = {'name': field.id, 'header': ['name', 'x'], 'data': [], 'sort': 'sortList: [[1,0],[0,0]]'}
        for entity in openatlas.models.entity.EntityMapper.get_by_class(field.id.split('_')[0]):
            selection += entity.name + '<br />' if field.data and entity.id in field.data else ''
            table['data'].append([
                entity.name,
                """<input id="{id}" {checked} value="{name}" class="multi-table-select" type="checkbox" />""".format(
                    id=str(entity.id),
                    name=entity.name,
                    checked='checked = "checked"' if field.data and entity.id in field.data else '')])
        html = """
            <span id="{name}-button" class="button">Select</span><br />
            <div id="{name}-selection" class="selection" style="text-align:left;">{selection}</div>
            <div id="{name}-overlay" class="overlay">
            <div id="{name}-dialog" class="overlay-container">{pager}</div></div>
            <script>$(document).ready(function () {{createOverlay("{name}", true);}});</script>
        """.format(name=field.id, selection=selection, pager=pager(None, table, True))
        return super(TableMultiSelect, self).__call__(field, **kwargs) + html


class TableMultiField(HiddenField):
    widget = TableMultiSelect()


class DateForm(Form):

    def populate_dates(self, entity):
        for code, types in entity.dates.items():
            if code in ['OA1', 'OA3', 'OA5']:
                for type_, date in types.items():
                    if type_ in ['Exact date value', 'From date value']:
                        self.date_begin_year.data = date['timestamp'].year
                        self.date_begin_month.data = date['timestamp'].month
                        self.date_begin_day.data = date['timestamp'].day
                        self.date_begin_info.data = date['info']
                    else:
                        self.date_begin_year2.data = date['timestamp'].year
                        self.date_begin_month2.data = date['timestamp'].month
                        self.date_begin_day2.data = date['timestamp'].day
            else:
                for type_, date in types.items():
                    if type_ in ['Exact date value', 'From date value']:
                        self.date_end_year.data = date['timestamp'].year
                        self.date_end_month.data = date['timestamp'].month
                        self.date_end_day.data = date['timestamp'].day
                        self.date_end_info.data = date['info']
                    else:
                        self.date_end_year2.data = date['timestamp'].year
                        self.date_end_month2.data = date['timestamp'].month
                        self.date_end_day2.data = date['timestamp'].day
            if code == 'OA3':
                self.date_birth.data = True
            if code == 'OA4':
                self.date_death.data = True

    date_birth = BooleanField(uc_first(_('birth')))
    date_death = BooleanField(uc_first(_('death')))

    date_begin_year = IntegerField(
        uc_first(_('begin')),
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713)]
    )
    date_begin_month = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)]
    )
    date_begin_day = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)]
    )
    date_begin_year2 = IntegerField(
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713)]
    )
    date_begin_month2 = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)]
    )
    date_begin_day2 = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)]
    )
    date_begin_info = StringField(render_kw={'placeholder': _('comment')},)
    date_end_year = IntegerField(
        uc_first(_('end')),
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713)]
    )
    date_end_month = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)]
    )
    date_end_day = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)]
    )
    date_end_year2 = IntegerField(
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713)]
    )
    date_end_month2 = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)]
    )
    date_end_day2 = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)]
    )
    date_end_info = StringField(render_kw={'placeholder': _('comment')})
