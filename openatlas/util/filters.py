# Created 2017 by Alexander Watzinger and others. Please see README.md for licensing information
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
from openatlas.util import util

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
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') for p in paragraph_re.split(escape(value)))
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
            '<a onclick="selectFromTable(this, \'' + name + '\', \'' + str(id_) + '\')">' + entities[id_].code + '</a>',
            '<a onclick="selectFromTable(this, \'' + name + '\', \'' + str(id_) + '\')">' + entities[id_].name + '</a>'])
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
    html = """
        <p class="description-title">{label}</p>
        <div class="description more">
            {description}
        </div>""".format(label=util.uc_first(_('description')), description=text)
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def page_buttons(self, entity):
    view = app.config['CODE_CLASS'][entity.class_.code]
    codes = app.config['CLASS_CODES'][view]
    html = ''
    pager_ids = EntityMapper.get_page_ids(entity, codes)
    if pager_ids.first_id and pager_ids.first_id != entity.id:
        html += """
            <a href="{url_first}"><div class="navigation first disabled"></div></a>
            <a href="{url_prev}"><div class="navigation prev disabled"></div></a>""".format(
                url_first=url_for(view + '_view', id_=pager_ids.first_id),
                url_prev=url_for(view + '_view', id_=pager_ids.previous_id))
    if pager_ids.last_id and pager_ids.last_id != entity.id:
        html += """
            <a href="{url_next}"><div class="navigation next"></div></a>
            <a href="{url_last}"><div class="navigation last"></div></a>""".format(
                url_next=url_for(view + '_view', id_=pager_ids.next_id),
                url_last=url_for(view + '_view', id_=pager_ids.last_id))
    if html:
        html = '<div class="pager">' + html + '</div>'
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_form(self, form, form_id=None, for_persons=False):
    if hasattr(form, 'name') and form.name.data:  # if name.data exists it's an update
        if hasattr(form, 'save') and hasattr(form.save, 'label'):
            form.save.label.text = _('save')
        if hasattr(form, 'insert_and_continue'):
            del form.insert_and_continue
    id_attribute = ' id="' + form_id + '" ' if form_id else ''
    html = {'main': '', 'types': '', 'header': '', 'footer': ''}
    for field in form:
        class_ = "required" if field.flags.required else ''
        errors = ''
        for error in field.errors:
            errors += util.uc_first(error)
        if field.type in ['TreeField', 'TreeMultiField']:
            try:
                hierarchy_id = int(field.id)
            except ValueError:
                hierarchy_id = NodeMapper.get_hierarchy_by_name(util.uc_first(field.id)).id
            node = g.nodes[hierarchy_id]
            if node.name in app.config['BASE_TYPES']:
                base_type = '<div class="table-row"><div><label>' + util.uc_first(_('type')) + '</label>'
                base_type += ' <span class="tooltip" title="' + _('tooltip type') + '">i</span></div>'
                base_type += '<div class="table-cell">' + str(field(class_=class_)) + errors + '</div></div>'
                html['types'] = base_type + html['types']
                continue
            html['types'] += '<div class="table-row"><div><label>' + node.name + '</label>'
            html['types'] += ' <span class="tooltip" title="' + _('tooltip type') + '">i</span></div>'
            html['types'] += '<div class="table-cell">' + str(field(class_=class_)) + errors + '</div></div>'
            continue
        if field.type in ['CSRFTokenField', 'HiddenField']:
            html['header'] += str(field)
            continue
        field.label.text = util.uc_first(field.label.text)
        field.label.text += ' *' if field.flags.required and form_id != 'login-form' else ''
        if field.id == 'description':
            html['footer'] += '<br />' + str(field.label) + '<br />' + str(field(class_=class_)) + '<br />'
            continue
        if field.type == 'SubmitField':
            html['footer'] += str(field)
            continue
        if field.id.split('_', 1)[0] == 'date':  # if it's a date field use a function to add dates
            if field.id == 'date_begin_year':
                html['footer'] += util.add_dates_to_form(form, for_persons)
            continue
        if field.description:
            field.label.text += ' <span class="tooltip" title="' + field.description + '">i</span>'
        errors = ' <span class="error">' + errors + ' </span>' if errors else ''
        if field.id == 'name':
            html['header'] += '<div class="table-row"><div>' + str(field.label) + '</div>'
            html['header'] += '<div class="table-cell">' + str(field(class_=class_)) + errors + '</div></div>'
            continue
        html['main'] += '<div class="table-row"><div>' + str(field.label) + '</div>'
        html['main'] += '<div class="table-cell">' + str(field(class_=class_)).replace('> ', '>') + errors + '</div></div>'

    html_all = '<form method="post"' + id_attribute + '>' + '<div class="data-table">'
    html_all += html['header'] + html['types'] + html['main'] + html['footer'] + '</div></form>'
    return html_all


@jinja2.contextfilter
@blueprint.app_template_filter()
def test_file(self, file_name):
    if os.path.isfile(app.root_path + '/static/' + file_name):
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
def build_delete_link(self, entity):
    """ Build a link to delete an entity with a JavaScript confirmation dialog."""
    name = entity.name.replace('\'', '')
    confirm = 'onclick="return confirm(\'' + _('Delete %(name)s?', name=name) + '\')"'
    url = url_for(app.config['CODE_CLASS'][entity.class_.code] + '_delete', id_=entity.id)
    return '<a ' + confirm + ' href="' + url + '">' + util.uc_first(_('delete')) + '</a>'


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_menu(self, origin):
    """ Returns html with the menu and mark appropriate item as selected."""
    html = ''
    if current_user.is_authenticated:
        selected = ''
        if origin:
            selected = app.config['CODE_CLASS'][origin.class_.code]
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
