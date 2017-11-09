# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import jinja2
import flask
import re

import os

from flask import session, render_template_string, url_for
from flask_login import current_user
from jinja2 import evalcontextfilter, escape
from flask_babel import lazy_gettext as _

import openatlas
from openatlas import app, EntityMapper
from openatlas.models.classObject import ClassMapper
from . import util

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
def format_date(self, value):
    return util.format_date(value)


@jinja2.contextfilter
@blueprint.app_template_filter()
def bookmark_toggle(self, entity_id):
    return util.bookmark_toggle(entity_id)


@jinja2.contextfilter
@blueprint.app_template_filter()
def table_select_model(self, name, selected=None):
    if name in ['domain', 'range']:
        entities = openatlas.classes
        sorter = 'sortList: [[0, 0]], headers: {0: { sorter: "class_code" }}'
    else:
        entities = openatlas.properties
        sorter = 'sortList: [[0, 0]], headers: {0: { sorter: "property_code" }}'
    table = {
        'name': name,
        'header': ['code', 'name'],
        'sort': sorter,
        'data': []}
    for id_ in entities:
        table['data'].append([
            '<a onclick="selectFromTable(this, \'' + name + '\', ' + str(id_) + ')">' + entities[id_].code + '</a>',
            '<a onclick="selectFromTable(this, \'' + name + '\', ' + str(id_) + ')">' + entities[id_].name + '</a>'])
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
    if not table['data']:
        return '<p>' + util.uc_first(_('no entries')) + '</p>'
    html = ''
    table_rows = session['settings']['default_table_rows']
    if hasattr(current_user, 'settings'):
        table_rows = current_user.settings['table_rows']
    show_pager = False if len(table['data']) < table_rows else True
    if show_pager:
        html += """
            <div id="{name}-pager" class="pager">
                <div class="navigation first"></div>
                <div class="navigation prev"></div>
                <div class="pagedisplay">
                    <input class="pagedisplay" type="text" disabled="disabled">
                </div>
                <div class="navigation next"></div>
                <div class="navigation last"></div>
                <div>
                    <select class="pagesize">
                        <option value="10">10</option>
                        <option value="20" selected="selected">20</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                    </select>
                </div>
                <input id="{name}-search" class="search" type="text" data-column="all"
                    placeholder="{filter}">
            </div>
            """.format(name=table['name'], filter=util.uc_first(_('filter')))
    html += '<table id="{name}-table" class="tablesorter"><thead><tr>'.format(name=table['name'])
    for header in table['header']:
        style = '' if header else 'class=sorter-false '
        html += '<th ' + style + '>' + header.capitalize() + '</th>'
    html += '</tr></thead><tbody>'
    for row in table['data']:
        html += '<tr>'
        for entry in row:
            entry = str(entry) if (entry and entry != 'None') or entry == 0 else ''
            try:
                float(entry.replace(',', ''))
                style = ' style="text-align:right;"'  # pragma: no cover
            except ValueError:
                style = ''
            html += '<td' + style + '>' + entry + '</td>'
        html += '</tr>'
    html += '</tbody>'
    html += '</table>'
    html += '<script>'
    sort = 'sortList: [[0, 0]]' if 'sort' not in table else table['sort']
    if show_pager:
        html += """
            $("#{name}-table").tablesorter({{ 
                {sort},
                dateFormat: "ddmmyyyy",
                widgets: [\'zebra\', \'filter\'],
                widgetOptions: {{
                    filter_external: \'#{name}-search\',
                    filter_columnFilters: false
                }}}})
            .tablesorterPager({{positionFixed: false, container: $("#{name}-pager"), size:{size}}});
        """.format(name=table['name'], sort=sort, size=table_rows)
    else:
        html += '$("#' + table['name'] + '-table").tablesorter({' + sort + ',widgets:[\'zebra\']});'
    html += '</script>'
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def description(self, entity):
    if not entity.description:
        return ''
    html = """
        <div class="description">
            <p class="description-title">{label}</p>
            <p>{description}</p>
        </div>""".format(
            label=util.uc_first(_('description')),
            description=entity.description.replace('\r\n', '<br />'))
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def page_buttons(self, entity):
        class_codes = {
            'source': ['E33'],
            'event': ['E6', 'E7', 'E8', 'E12'],
            'actor': ['E21', 'E40', 'E74'],
            'place': ['E18'],
            'reference': ['E31', 'E84']}
        code_class = {
            'E33': 'source',
            'E6': 'event',
            'E7': 'event',
            'E8': 'event',
            'E12': 'event',
            'E21': 'actor',
            'E40': 'actor',
            'E74': 'actor',
            'E18': 'place',
            'E31': 'reference',
            'E84': 'reference'}
        view = code_class[entity.class_.code]
        codes = class_codes[view]
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
            html = '<div class="pager" style="float:left;margin:0.1em 0.5em 0 0;"">' + html
            html += '</div>'
        return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def get_class_name(self, code):
    return ClassMapper.get_by_code(code).name


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_form(self, form, form_id=None, for_persons=False):
    if hasattr(form, 'name') and form.name.data:  # if name.data exists it's an update
        if hasattr(form, 'save'):
            form.save.label.text = _('save')
        if hasattr(form, 'insert_and_continue'):
            del form.insert_and_continue
    id_attribute = ' id="' + form_id + '" ' if form_id else ''
    html = '<form method="post"' + id_attribute + '>' + '<div class="data-table">'
    footer = ''
    for field in form:
        class_ = "required" if field.flags.required else ''
        errors = ''
        for error in field.errors:
            errors += util.uc_first(error)
        if field.type in ['TreeField', 'TreeMultiField']:
            node = openatlas.nodes[int(field.id)]
            html += '<div class="table-row"><div><label>' + node.name + '</label>'
            html += ' <span class="tooltip" title="' + _('tooltip type') + '">i</span></div>'
            html += '<div class="table-cell">' + str(field(class_=class_)) + errors + '</div></div>'
            continue
        if field.type in ['CSRFTokenField', 'HiddenField']:
            html += str(field)
            continue
        field.label.text = util.uc_first(field.label.text)
        field.label.text += ' *' if field.flags.required and form_id != 'login-form' else ''
        if field.id == 'description':
            footer += '<br />' + str(field.label) + '<br />' + str(field(class_=class_)) + '<br />'
            continue
        if field.type == 'SubmitField':
            footer += str(field)
            continue
        if field.id.split('_', 1)[0] == 'date':  # if it's a date field use a function to add dates
            if field.id == 'date_begin_year':
                footer += util.add_dates_to_form(form, for_persons)
            continue
        if field.description:
            field.label.text += ' <span class="tooltip" title="' + field.description + '">i</span>'
        errors = ' <span class="error">' + errors + ' </span>' if errors else ''
        html += '<div class="table-row"><div>' + str(field.label) + '</div>'
        html += '<div class="table-cell">' + str(field(class_=class_)) + errors + '</div></div>'
    html += footer + '</div></form>'
    return html


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
