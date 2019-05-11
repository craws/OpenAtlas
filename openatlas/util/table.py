# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Optional

from flask import session
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas import app


class Table:

    def __init__(self,
                 header: Optional[list] = None,  # A list of column header labels
                 headers: Optional[str] = None,  # Extra headers information for tablesorter
                 sort: Optional[str] = None,  # Column sort option for tablesorter
                 pager: Optional[bool] = True,  # Whether to show pager and search
                 rows: Optional[list] = None) -> None:
        self.header = header if header else []
        self.headers = 'headers:' + headers + ',' if headers else ''
        self.sort = 'sortList:' + sort + ',' if sort else ''
        self.rows = rows if rows else []
        self.pager = pager

    def display(self, name: Optional[str] = 'table', remove_rows: Optional[bool] = True) -> str:
        """ Display a HTML table, setting a name is important if there are multiple on one page."""
        from openatlas.util.util import uc_first
        if not self.rows:
            return '<p>' + uc_first(_('no entries')) + '</p>'
        html = ''
        table_rows = session['settings']['default_table_rows']
        if hasattr(current_user, 'settings'):
            table_rows = current_user.settings['table_rows']
        if self.pager:
            options = ''
            for amount in app.config['DEFAULT_TABLE_ROWS']:
                options += '<option value="{amount}"{selected}>{amount}</option>'.format(
                    amount=amount, selected=' selected="selected"' if amount == table_rows else '')
            placeholder = uc_first(_('type to search'))
            if int(session['settings']['minimum_tablesorter_search']) > 1:  # pragma: no cover
                placeholder += ' (' + _('min %(limit)s chars',
                                        limit=session['settings'][
                                            'minimum_tablesorter_search']) + ')'
            html += """
                <div id="{name}-pager" class="pager">
                    <div class="navigation first"></div>
                    <div class="navigation prev"></div>
                    <div class="pagedisplay">
                        <input class="pagedisplay" type="text" disabled="disabled">
                    </div>
                    <div class="navigation next"></div>
                    <div class="navigation last"></div>
                    <div><select class="pagesize">{options}</select></div>
                    <input id="{name}-search" class="search" type="text" data-column="all"
                        placeholder="{placeholder}">
                </div>
                <div style="clear:both;"></div>
                """.format(name=name, options=options, placeholder=placeholder)
        html += '<table id="{name}-table" class="tablesorter"><thead><tr>'.format(name=name)

        for header in self.header:
            if header:
                html += '<th>' + uc_first(_(header)) + '</th>'
            else:
                html += '<th class=sorter-false></th>'
        # Append missing headers
        html += '<th class=sorter-false></th>' * (len(self.rows[0]) - len(self.header))
        html += '</tr></thead>'

        html += '<tbody>'
        for row in self.rows:
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
        html += '</tbody></table>'

        if not self.pager:
            return html + """
                <script>
                    $("#{name}-table").tablesorter({{
                        {sort}
                        widgets: ["filter", "zebra"],
                        widgetOptions: {{
                            filter_liveSearch: {filter_liveSearch},
                            filter_external: "#{name}-search",
                            filter_columnFilters: false
                        }}
                    }});
                </script>""".format(name=name, sort=self.sort,
                                    filter_liveSearch=session['settings']['minimum_jstree_search'])

        return html + """
            <script>
                $("#{name}-table").tablesorter({{
                    {headers}
                    {sort}
                    dateFormat: "ddmmyyyy",
                    widgets: ["filter", "zebra"],
                    widgetOptions: {{
                        filter_liveSearch: {filter_liveSearch},
                        filter_external: "#{name}-search",
                        filter_columnFilters: false
                    }}}})
                .tablesorterPager({{
                    delayInit: true,
                    {remove_rows}
                    positionFixed: false,
                    container: $("#{name}-pager"),
                    size:{size}}});
            </script>""".format(name=name, sort=self.sort, size=table_rows,
                                remove_rows='removeRows: true,' if remove_rows else '',
                                filter_liveSearch=session['settings']['minimum_tablesorter_search'],
                                headers=self.headers)
