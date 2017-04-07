# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
# -*- coding: utf-8 -*-
import jinja2
import flask
import re

from openatlas.util import util
from jinja2 import evalcontextfilter, Markup, escape

blueprint = flask.Blueprint('filters', __name__)
paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


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
    for item in data:
        key, value = item.popitem()
        if value or value == 0:
            html += '<div><div>' + util.uc_first(key) + '</div><div class="table-cell">' + str(value) + '</div></div>'
    html += '</div>'
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def pager(self, data):
    # To do: remove no cover when more content to test
    if not data['data']:  # pragma: no cover
        return ''
    html = ''
    name = data['name']
    if 'hide_pager' not in data:  # pragma: no cover
        html += '<div id="' + name + '-pager" class="pager">'
        html += """
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
                </div>"""
        html += '<input id="' + name + '-search" class="search" type="text" data-column="all" placeholder="Filter">'
        html += '</div>'
    html += '<table id="' + name + '-table" class="tablesorter">'
    html += '<thead><tr>'
    for header in data['header']:
        style = '' if header else 'class=sorter-false '
        html += '<th ' + style + '>' + header.capitalize() + '</th>'
    html += '</tr></thead><tbody>'
    for row in data['data']:
        html += '<tr>'
        for entry in row:
            entry = str(entry) if entry and entry != 'None' else ''
            try:
                float(entry.replace(',', ''))
                style = ' style="text-align:right;"'  # pragma: no cover
            except ValueError:
                style = ''
            html += '<td' + style + '>' + entry + '</td>'
        html += '</tr>'
    html += '</tbody>'
    html += '</table>'
    sort = 'sortList: [[0, 0]]' if 'sort' not in data else data['sort']
    headers = 'headers: { 1: { sorter: "digit" } },' if 'headers' in data else ''
    text_extractions = "textExtraction: function(node){return $(node).text().replace(/[,€]/g,'');}"
    html += '<script type="text/javascript">'
    if 'hide_pager' in data:
        html += '$("#' + name + '-table").tablesorter({' + sort + ', widgets: [\'zebra\'],'
        html += text_extractions + '});'
    else:  # pragma: no cover
        html += '$("#' + name + '-table")'
        html += '.tablesorter({ ' + headers + ' ' + sort + ', dateFormat: "ddmmyyyy" '
        html += ' , widgets: [\'zebra\', \'filter\'],  ' + text_extractions + ','
        html += 'widgetOptions: {filter_external: \'#' + name + '-search\', filter_columnFilters: false}})'
        html += '.tablesorterPager({positionFixed: false, container: $("#' + name + '-pager"), size: 20});'
    html += '</script>'
    return html
