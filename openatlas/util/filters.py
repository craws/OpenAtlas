# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os
import re

import flask
import jinja2
from flask import g, render_template_string, request, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from jinja2 import escape, evalcontextfilter

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.node import NodeMapper
from openatlas.models.content import ContentMapper
from openatlas.util import util
from openatlas.util.util import display_tooltip

blueprint = flask.Blueprint('filters', __name__)
paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@jinja2.contextfilter
@blueprint.app_template_filter()
def link(self, entity):
    return util.link(entity)


@jinja2.contextfilter
@blueprint.app_template_filter()
def is_authorized(self, group):
    return util.is_authorized(group)


@jinja2.contextfilter
@blueprint.app_template_filter()
def uc_first(self, string):
    return util.uc_first(string)


@jinja2.contextfilter
@blueprint.app_template_filter()
@evalcontextfilter
def nl2br(self, value):
    result = u'\n\n'.join(
        u'<p>%s</p>' % p.replace('\n', '<br>\n') for p in paragraph_re.split(escape(value)))
    return result


@jinja2.contextfilter
@blueprint.app_template_filter()
def data_table(self, data):
    html = '<div class="data-table">'
    for key, value in data:
        if value or value == 0:
            value = util.uc_first(_('no')) if value is False else value
            value = util.uc_first(_('yes')) if value is True else value
            html += '<div class="table-row"><div>' + util.uc_first(key) + '</div>'
            html += '<div class="table-cell">' + str(value) + '</div></div>'
    html += '</div>'
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def bookmark_toggle(self, entity_id):
    return util.bookmark_toggle(entity_id)


@jinja2.contextfilter
@blueprint.app_template_filter()
def table_select_model(self, name, selected=None):
    if name in ['domain', 'range']:
        entities = g.classes
        sorter = 'sortList: [[0, 0]], headers: {0: { sorter: "class_code" }}'
    else:
        entities = g.properties
        sorter = 'sortList: [[0, 0]], headers: {0: { sorter: "property_code" }}'
    table = {
        'id': name,
        'header': ['code', 'name'],
        'sort': sorter,
        'data': []}
    for id_ in entities:
        table['data'].append([
            '<a onclick="selectFromTable(this, \'' + name + '\', \'' + str(id_) + '\')">' +
            entities[id_].code + '</a>',
            '<a onclick="selectFromTable(this, \'' + name + '\', \'' + str(id_) + '\')">' +
            entities[id_].name + '</a>'])
    value = selected.code + ' ' + selected.name if selected else ''
    html = """
        <input id="{name}-button" value="{value}" class="table-select" type="text"
            onfocus="this.blur()" readonly="readonly" />
        <div id="{name}-overlay" class="overlay">
            <div id="{name}-dialog" class="overlay-container">
                {pager}
            </div>
        </div>
        <script>$(document).ready(function () {{createOverlay("{name}");}});</script>
    """.format(name=name, value=value, pager=render_template_string(pager(None, table)))
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def pager(self, table):
    return util.pager(table)


@jinja2.contextfilter
@blueprint.app_template_filter()
def get_class_name(self, code):
    return g.classes[code].name


@jinja2.contextfilter
@blueprint.app_template_filter()
def description(self, entity):
    if not entity.description:
        return ''
    text = entity.description.replace('\r\n', '<br />')
    label = util.uc_first(_('description'))
    if hasattr(entity, 'system_type') and entity.system_type == 'source content':
        label = util.uc_first(_('content'))
    html = """
        <p class="description-title">{label}</p>
        <div class="description more">
            {description}
        </div>""".format(label=label, description=text)
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_content_translation(self, text):
    return ContentMapper.get_translation(text)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_form(self, form, form_id=None, for_persons=False):
    multipart = 'enctype="multipart/form-data"' if hasattr(form, 'file') else ''
    if 'update' in request.path:
        if hasattr(form, 'save') and hasattr(form.save, 'label'):
            form.save.label.text = _('save')
        if hasattr(form, 'insert_and_continue'):
            del form.insert_and_continue
    id_attribute = ' id="' + form_id + '" ' if form_id else ''
    html = {'main': '', 'types': '', 'value_types': '', 'header': '', 'footer': ''}

    def display_value_type_fields(subs, html_=''):
        for sub_id in subs:
            sub = g.nodes[sub_id]
            field_ = getattr(form, 'value_list-' + str(sub_id))
            html_ += """
                <div class="table-row value-type-switch">
                    <div><label>{label}</label> {tooltip}</div>
                    <div class="table-cell">{field}</div>
                </div>
            """.format(
                label=sub.name,
                tooltip=display_tooltip(sub.description),
                field=field_(class_='value-type'))
            html_ += display_value_type_fields(sub.subs)
        return html_

    for field in form:
        if field.id.startswith('value_list-'):
            continue
        class_ = "required" if field.flags.required else ''
        errors = ''
        for error in field.errors:
            errors += util.uc_first(error)
        if field.type in ['TreeField', 'TreeMultiField']:
            hierarchy_id = int(field.id)
            node = g.nodes[hierarchy_id]
            label = node.name
            if node.name in app.config['BASE_TYPES']:
                label = util.uc_first(_('type'))
            if field.label.text == 'super':
                label = util.uc_first(_('super'))
            if node.value_type and 'is_node_form' not in form:
                html['value_types'] += """
                        <div class="table-row value-type-switch">
                            <div></div>
                            <div class="table-cell">
                                <label style="font-weight:bold;">{label}</label> {tooltip}
                            </div>
                        </div>
                    """.format(
                    label=label,
                    tooltip=display_tooltip(node.description))
                html['value_types'] += display_value_type_fields(node.subs)
                continue
            else:
                type_field = """
                    <div class="table-row">
                        <div><label>{label}</label> {tooltip}</div>
                        <div class="table-cell">{field}</div>
                    </div>
                """.format(
                    label=label,
                    tooltip='' if 'is_node_form' in form else display_tooltip(node.description),
                    field=str(field(class_=class_)) + errors)
                if node.name in app.config['BASE_TYPES']:  # base type should be above other fields
                    html['types'] = type_field + html['types']
                else:
                    html['types'] += type_field
                continue
        if field.type in ['CSRFTokenField', 'HiddenField']:
            html['header'] += str(field)
            continue
        field.label.text = util.uc_first(field.label.text)
        field.label.text += ' *' if field.flags.required and form_id != 'login-form' else ''
        if field.id == 'description':
            html['footer'] += '<br />' + str(field.label) + '<br />' + str(field(class_=class_))
            html['footer'] += '<br />'
            continue
        if field.type == 'SubmitField':
            html['footer'] += str(field)
            continue
        if field.id.split('_', 1)[0] == 'date':  # if it's a date field use a function to add dates
            if field.id == 'date_begin_year':
                html['footer'] += util.add_dates_to_form(form, for_persons)
            continue
        field.label.text += display_tooltip(field.description)
        errors = ' <span class="error">' + errors + ' </span>' if errors else ''
        if field.id in ('file', 'name'):
            html['header'] += '<div class="table-row"><div>' + str(field.label) + '</div>'
            html['header'] += '<div class="table-cell">' + str(field(class_=class_)) + errors
            html['header'] += '</div></div>'
            continue
        html['main'] += '<div class="table-row"><div>' + str(field.label) + '</div>'
        html['main'] += '<div class="table-cell">' + str(field(class_=class_)).replace('> ', '>')
        html['main'] += errors + '</div></div>'

    html_all = '<form method="post"' + id_attribute + ' ' + multipart + '>'
    html_all += '<div class="data-table">'
    if html['value_types']:
        html['value_types'] = """
        <div class="table-row">
            <div>
                <label>{values}</label>
            </div>
            <div class="table-cell value-type-switcher">
                <span id="value-type-switcher" class="button">{show}</span>
            </div>
        </div>""".format(
            values=util.uc_first(_('values')), show=util.uc_first(_('show'))) + html['value_types']

    html_all += html['header'] + html['types'] + html['main'] + html['value_types'] + html['footer']
    html_all += '</div></form>'
    return html_all


@jinja2.contextfilter
@blueprint.app_template_filter()
def test_file(self, file_name):
    if os.path.isfile(app.root_path + '/' + file_name):
        return file_name
    return False


@jinja2.contextfilter
@blueprint.app_template_filter()
def sanitize(self, string):
    return util.sanitize(string)


@jinja2.contextfilter
@blueprint.app_template_filter()
def truncate_string(self, string):
    return util.truncate_string(string)


@jinja2.contextfilter
@blueprint.app_template_filter()
def get_view_name(self, entity):
    return util.get_view_name(entity)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_delete_link(self, entity):
    """ Build a link to delete an entity with a JavaScript confirmation dialog."""
    name = entity.name.replace('\'', '')
    confirm = 'onclick="return confirm(\'' + _('Delete %(name)s?', name=name) + '\')"'
    url = url_for(util.get_view_name(entity) + '_delete', id_=entity.id)
    return '<a ' + confirm + ' href="' + url + '">' + util.uc_first(_('delete')) + '</a>'


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_menu(self, origin):
    """ Returns html with the menu and mark appropriate item as selected."""
    html = ''
    if current_user.is_authenticated:
        selected = util.get_view_name(origin) if origin else ''
        items = ['overview', 'source', 'event', 'actor', 'place', 'reference', 'types', 'admin']
        for item in items:
            if selected:
                css = 'active' if item == selected else ''
            else:
                css = 'active' if request.path.startswith('/' + item) or \
                                  (item == 'overview' and request.path == '/') else ''
            html += '<div class="{css}"><a href="/{item}">{label}</a></div>'.format(
                css=css, item=item, label=util.uc_first(_(item)))
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_debug_info(self, debug_model, form):
    """ Returns html with debug information about database queries and form errors."""
    html = ''
    for name, value in debug_model.items():
        if name in ['current']:
            continue  # Don't display current time counter
        if name not in ['by codes', 'by id', 'by ids', 'linked', 'user', 'div sql']:
            value = '{:10.2f}'.format(value)
        html += """
            <div>
                <div>{name}</div>
                <div class="table-cell" style="text-align:right;">
                    {value}
                </div>
            </div>""".format(name=name, value=value)
    if form and hasattr(form, 'errors'):
        for fieldName, errorMessages in form.errors.items():
            html += fieldName + ' - ' + errorMessages[0] + '<br />'
    return html
