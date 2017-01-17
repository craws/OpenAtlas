# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
# -*- coding: utf-8 -*-
import jinja2
import flask

from openatlas.util import util

blueprint = flask.Blueprint('filters', __name__)


@jinja2.contextfilter
@blueprint.app_template_filter()
def uc_first(self, string):
    return util.uc_first(string)


@jinja2.contextfilter
@blueprint.app_template_filter()
def pager(self, data):
    if not data['data']:
        return ''
    html = ''
    name = data['name']
    if 'hide_pager' not in data:
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
                style = ' style="text-align:right;"'
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
    else:
        html += '$("#' + name + '-table")'
        html += '.tablesorter({ ' + headers + ' ' + sort + ', dateFormat: "ddmmyyyy" '
        html += ' , widgets: [\'zebra\', \'filter\'],  ' + text_extractions + ','
        html += 'widgetOptions: {filter_external: \'#' + name + '-search\', filter_columnFilters: false}})'
        html += '.tablesorterPager({positionFixed: false, container: $("#' + name + '-pager"), size: 20});'
    html += '</script>'
    return html
