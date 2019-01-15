# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os
import re

import flask
import jinja2
from flask import g, render_template_string, request, session, url_for
from flask_babel import format_number as babel_format_number, lazy_gettext as _
from flask_login import current_user
from jinja2 import escape, evalcontextfilter
from wtforms import IntegerField
from wtforms.validators import Email

from openatlas import app
from openatlas.forms.forms import TreeField, ValueFloatField
from openatlas.models.content import ContentMapper
from openatlas.util import util
from openatlas.util.util import display_tooltip, get_file_path, print_file_extension

blueprint = flask.Blueprint('filters', __name__)
paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@jinja2.contextfilter
@blueprint.app_template_filter()
def link(self, entity):
    return util.link(entity)


@jinja2.contextfilter
@blueprint.app_template_filter()
def format_number(self, number):
    return babel_format_number(number)


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
def display_move_form(self, form, root_name):
    html = ''
    for field in form:
        if type(field) is TreeField:
            html += '<p>' + root_name + ' ' + str(field) + '</p>'
    html += '<p><a class="button" id="select-all">' + util.uc_first(_('select all')) + '</a>'
    html += '<a class="button" id="select-none">' + util.uc_first(_('deselect all')) + '</a></p>'
    table = {'id': 'move', 'header': ['#', util.uc_first(_('selection'))], 'data': []}
    for item in form.selection:
        table['data'].append([item, item.label.text])
    return html + util.pager(table)


@jinja2.contextfilter
@blueprint.app_template_filter()
def table_select_model(self, name, selected=None):
    if name in ['domain', 'range']:
        entities = g.classes
        sorter = 'sortList: [[0, 0]], headers: {0: { sorter: "class_code" }}'
    else:
        entities = g.properties
        sorter = 'sortList: [[0, 0]], headers: {0: { sorter: "property_code" }}'
    table = {'id': name, 'header': ['code', 'name'], 'sort': sorter, 'data': []}
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
    html = """<p class="description-title">{label}</p>
        <div class="description more">{description}</div>""".format(label=label, description=text)
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_profile_image(self, image_id):
    if not image_id:
        return ''
    src = url_for('display_file', filename=os.path.basename(get_file_path(image_id)))
    return """
        <div id="profile_image_div">
            <a href="/file/view/{id}">
                <img style="max-width:{width}px;" alt="profile image" src="{src}" />
            </a>
        </div>""".format(id=image_id, src=src, width=session['settings']['profile_image_width'])


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_content_translation(self, text):
    return ContentMapper.get_translation(text)


@jinja2.contextfilter
@blueprint.app_template_filter()
def manual_link(self, wiki_site):
    # Creates a link to a manual page
    html = """
        <p class="manual">
            <a class="manual" href="{url}" rel="noopener" target="_blank">
                <img style="height:14px;" src="/static/images/icons/book.png" alt='' /> 
                {label}
            </a>
        </p>""".format(url='https://redmine.openatlas.eu/projects/uni/wiki/' + wiki_site,
                       label=util.uc_first(_('manual')))
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_logo(self, file_id):
    src = '/static/images/layout/logo.png'
    if file_id:
        extension = print_file_extension(int(file_id))
        if extension != 'N/A':
            src = url_for('display_logo', filename=file_id + extension)
    return '<img src="{src}" alt="Logo" />'.format(src=src)


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
            field_ = getattr(form, str(sub_id))
            html_ += """
                <div class="table-row value-type-switch">
                    <div><label>{label}</label></div>
                    <div class="table-cell">{field} {unit}</div>
                </div>
            """.format(label=sub.name, unit=sub.description, field=field_(class_='value-type'))
            html_ += display_value_type_fields(sub.subs)
        return html_

    for field in form:
        if type(field) is ValueFloatField:
            continue
        class_ = 'required' if field.flags.required else ''
        class_ += ' integer' if type(field) is IntegerField else ''
        for validator in field.validators:
            class_ += ' email' if type(validator) is Email else ''
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
                    """.format(label=label, tooltip=display_tooltip(node.description))
                html['value_types'] += display_value_type_fields(node.subs)
                continue
            else:
                type_field = """
                    <div class="table-row">
                        <div><label>{label}</label> {info}</div>
                        <div class="table-cell">{field}</div>
                    </div>
                """.format(label=label, field=str(field(class_=class_)) + errors,
                           info='' if 'is_node_form' in form else display_tooltip(node.description))
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
            html['footer'] += '<br />{label}<br />{text}<br />'.format(
                label=field.label, text=field(class_=class_))
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
        values_html = """
            <div class="table-row">
                <div>
                    <label>{values}</label>
                </div>
                <div class="table-cell value-type-switcher">
                    <span id="value-type-switcher" class="button">{show}</span>
                </div>
            </div>""".format(values=util.uc_first(_('values')), show=util.uc_first(_('show')))
        html['value_types'] = values_html + html['value_types']
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
def display_delete_link(self, entity):
    """ Build a link to delete an entity with a JavaScript confirmation dialog."""
    name = entity.name.replace('\'', '')
    confirm = 'onclick="return confirm(\'' + _('Delete %(name)s?', name=name) + '\')"'
    url = url_for(entity.view_name + '_delete', id_=entity.id)
    return '<a ' + confirm + ' href="' + url + '">' + util.uc_first(_('delete')) + '</a>'


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_menu(self, origin):
    """ Returns html with the menu and mark appropriate item as selected."""
    html = ''
    if current_user.is_authenticated:
        selected = origin.view_name if origin else ''
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
        if name not in ['by codes', 'by id', 'link sql', 'user', 'div sql']:
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
