# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict

import jinja2
import flask
import re

import os

from flask import session, render_template_string
from flask_login import current_user
from jinja2 import evalcontextfilter, Markup, escape
from flask_babel import lazy_gettext as _

import openatlas
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
    return Markup(result)


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
    return Markup(html)


@jinja2.contextfilter
@blueprint.app_template_filter()
def format_date(self, value, text_format='%Y-%m-%d'):
    return util.format_date(value, text_format)


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
            '<a onclick="selectFromTable(this, \'' + name + '\', ' + str(id_) + ')">' + entities[id_].name + '</a>'
        ])
    value = selected.code + ' ' + selected.name if selected else ''
    html = '''
        <input id="{name}-button" value="{value}" class="table-select" type="text" onfocus="this.blur()"
            readonly="readonly" />
        <div id="{name}-overlay" class="overlay">
            <div id="{name}-dialog" class="overlay-container">
                {pager}
            </div>
        </div>
        <script>$(document).ready(function () {{createOverlay("{name}");}});</script>
    '''.format(name=name, value=value, pager=render_template_string(pager(None, table)))

    return Markup(html)


@jinja2.contextfilter
@blueprint.app_template_filter()
def pager(self, table):
    if not table['data']:
        return Markup('<p>' + util.uc_first(_('no entries')) + '</p>')
    html = ''
    table_rows = session['settings']['default_table_rows']
    if hasattr(current_user, 'table_rows'):
        table_rows = current_user.settings['table_rows']
    show_pager = False if len(table['data']) < table_rows else True
    if show_pager:
        html += '''
            <div id="{name}-pager" class="pager">
                <div class="navigation first"></div>
                <div class="navigation prev"></div>
                <div class="pagedisplay"><input class="pagedisplay" type="text" disabled="disabled"></div>
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
                <input id="{name}-search" class="search" type="text" data-column="all" placeholder="{filter}">
            </div>
            '''.format(name=table['name'], filter=util.uc_first(_('filter')))
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
                widgetOptions: {{filter_external: \'#{name}-search\', filter_columnFilters: false}}}})
            .tablesorterPager({{positionFixed: false, container: $("#{name}-pager"), size: 20}});
        """.format(name=table['name'], sort=sort)
    else:
        html += '$("#' + table['name'] + '-table").tablesorter({' + sort + ',widgets:[\'zebra\']});'
    html += '</script>'
    return Markup(html)


@jinja2.contextfilter
@blueprint.app_template_filter()
def description(self, entity):
    if not entity.description:
        return ''
    html = '<div class="description"><p class="description-title">' + util.uc_first(_('description')) + '</p>'
    html += '<p>' + entity.description.replace('\r\n', '<br />') + '</p></div>'
    return Markup(html)


@jinja2.contextfilter
@blueprint.app_template_filter()
def get_class_name(self, code):
    return ClassMapper.get_by_code(code).name


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_form(self, form, form_id=None):
    id_attribute = ' id="' + form_id + '" ' if form_id else ''
    html = '<form method="post"' + id_attribute + '>' + '<div class="data-table">'
    info = ''
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField']:
            html += str(field)
            continue
        field.label.text = util.uc_first(field.label.text)
        if field.type == 'SubmitField':
            html += str(field)
            continue
        if field.id.split('_', 1)[0] == 'date':  # if it's a date field use a function to add dates
            if field.id == 'date_begin_year':
                html += util.add_dates_to_form(form)
            continue
        field.label.text += ' *' if field.flags.required and form_id != 'login-form' else ''
        errors = ''
        for error in field.errors:
            errors += util.uc_first(error)
        errors = ' <span class="error">' + errors + ' </span>' if errors else ''
        class_ = "required" if field.flags.required else ''
        html += '<div class="table-row"><div>' + str(field.label) + '</div>'
        html += '<div class="table-cell">' + str(field(class_=class_)) + errors + '</div></div>'
    html += info + '</div></form>'
    return Markup(html)


@jinja2.contextfilter
@blueprint.app_template_filter()
def test_file(self, file_name):
    if os.path.isfile(openatlas.app.root_path + '/static/' + file_name):
        return file_name
    return False


@jinja2.contextfilter
@blueprint.app_template_filter()
def sanitize(self, string):
    return util.sanitize(string)


@jinja2.contextfilter
@blueprint.app_template_filter()
def print_entity_dates(self, entity):
    date_types = OrderedDict([
        ('OA1', _('first')),
        ('OA3', _('birth')),
        ('OA2', _('last')),
        ('OA4', _('death')),
        ('OA5', _('begin')),
        ('OA6', _('end')),
    ])
    html = ''
    for code, label in date_types.items():
        if code in entity.dates:
            if 'Exact date value' in entity.dates[code]:
                html += util.uc_first(label) + ': '
                html += util.format_date(entity.dates[code]['Exact date value']['timestamp'])
                if entity.dates[code]['Exact date value']['info']:
                    html += ' ' + entity.dates[code]['Exact date value']['info']
                html += '<br />'
            else:
                html += util.uc_first(label) + ': ' + util.uc_first(_('between')) + ' '
                html += util.format_date(entity.dates[code]['From date value']['timestamp'])
                html += ' and ' + util.format_date(entity.dates[code]['To date value']['timestamp'])
                if entity.dates[code]['From date value']['info']:
                    html += ' ' + entity.dates[code]['From date value']['info']
                html += '<br />'
    return Markup(html)
