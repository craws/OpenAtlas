# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Optional
from flask import json


class Table:
    HEADERS = {'source': ['name', 'type', 'description'],
               'event': ['name', 'class', 'type', 'begin', 'end'],
               'actor': ['name', 'class', 'begin', 'end'],
               'group': ['name', 'class', 'begin', 'end'],
               'place': ['name', 'type', 'begin', 'end'],
               'feature': ['name', 'type', 'begin', 'end'],
               'stratigraphic-unit': ['name', 'type', 'begin', 'end'],
               'find': ['name', 'type', 'begin', 'end'],
               'reference': ['name', 'class', 'type'],
               'file': ['name', 'license', 'size', 'extension', 'description']}

    def __init__(self,
                 header: Optional[list] = None,  # A list of column header labels
                 rows: Optional[list] = None,  # rows containing the data
                 order: Optional[str] = None,  # Column order option
                 defs: Optional[str] = None,  # Additional definitions for DataTables
                 paging: Optional[bool] = True) -> None:  # Whether to show pager
        self.header = header if header else []
        self.rows = rows if rows else []
        self.paging = 'true' if paging else 'false'
        self.order = order if order else ''
        self.defs = defs if defs else ''

    def display(self, name: Optional[str] = 'table') -> str:
        if not self.rows:
            return '<p>N/A</p>'

        columns = ''
        for item in self.header:
            columns += "{title:'" + item.capitalize() + "'},"
        columns += "{title:''}," * (len(self.rows[0]) - len(self.header))  # Add emtpy headers

        html = """
            <table id="{name}_table" class="compact stripe cell-border hover" width="100%"></table>
            <script>
                $(document).ready(function() {{
                    $('#{name}_table').DataTable( {{
                        data: {data},
                        stateSave: true,
                        columns: [{columns}],
                        {order}
                        {defs}
                        paging: {paging},
                        pageLength: 25,
                        autoWidth: false,
                    }});
                }});
            </script>""".format(name=name,
                                data=json.dumps(self.rows),
                                columns=columns,
                                order='order: ' + self.order + ',' if self.order else '',
                                defs='columnDefs: ' + self.defs + ',' if self.defs else '',
                                paging=self.paging)

        # Toggle header and footer HTML
        css_header = '#{name}_table_wrapper table thead {{ display:none; }}'.format(name=name)
        css_toolbar = '#{name}_table_wrapper .fg-toolbar {{ display:none; }}'.format(name=name)
        html += '<style type="text/css">{header} {toolbar}</style>'.format(
            header=css_header if not self.header else '',
            toolbar=css_toolbar if len(self.rows) < 26 else '')
        return html



    # def display(self, name: Optional[str] = 'table', remove_rows: Optional[bool] = True) -> str:
    #     """ Display a HTML table, setting a name is important if there are multiple on one page."""
    #     from openatlas.util.util import uc_first
    #     if not self.rows:
    #         return '<p>' + uc_first(_('no entries')) + '</p>'
    #     html = ''
    #     table_rows = session['settings']['default_table_rows']
    #     if hasattr(current_user, 'settings'):
    #         table_rows = current_user.settings['table_rows']
    #     if self.pager:
    #         options = ''
    #         for amount in app.config['DEFAULT_TABLE_ROWS']:
    #             options += '<option value="{amount}"{selected}>{amount}</option>'.format(
    #                 amount=amount, selected=' selected="selected"' if amount == table_rows else '')
    #         placeholder = uc_first(_('type to search'))
    #         if int(session['settings']['minimum_tablesorter_search']) > 1:  # pragma: no cover
    #             placeholder += ' (' + _('min %(limit)s chars',
    #                                     limit=session['settings'][
    #                                         'minimum_tablesorter_search']) + ')'
    #         html += """
    #             <div id="{name}-pager" class="pager">
    #                 <div class="navigation first"></div>
    #                 <div class="navigation prev"></div>
    #                 <div class="pagedisplay">
    #                     <input class="pagedisplay" type="text" disabled="disabled">
    #                 </div>
    #                 <div class="navigation next"></div>
    #                 <div class="navigation last"></div>
    #                 <div><select class="pagesize">{options}</select></div>
    #                 <input id="{name}-search" class="search" type="text" data-column="all"
    #                     placeholder="{placeholder}">
    #             </div>
    #             <div style="clear:both;"></div>
    #             """.format(name=name, options=options, placeholder=placeholder)
    #     html += '<table id="{name}-table" class="tablesorter"><thead><tr>'.format(name=name)
    #
    #     for header in self.header:
    #         if header:
    #             html += '<th>' + uc_first(_(header)) + '</th>'
    #         else:
    #             html += '<th class=sorter-false></th>'
    #     # Append missing headers
    #     html += '<th class=sorter-false></th>' * (len(self.rows[0]) - len(self.header))
    #     html += '</tr></thead>'
    #
    #     html += '<tbody>'
    #     for row in self.rows:
    #         html += '<tr>'
    #         for entry in row:
    #             entry = str(entry) if (entry and entry != 'None') or entry == 0 else ''
    #             try:
    #                 float(entry.replace(',', ''))
    #                 style = ' style="text-align:right;"'  # pragma: no cover
    #             except ValueError:
    #                 style = ''
    #             html += '<td' + style + '>' + entry + '</td>'
    #         html += '</tr>'
    #     html += '</tbody></table>'
    #
    #     if not self.pager:
    #         return html + """
    #             <script>
    #                 $("#{name}-table").tablesorter({{
    #                     {sort}
    #                     widgets: ["filter", "zebra"],
    #                     widgetOptions: {{
    #                         filter_liveSearch: {filter_liveSearch},
    #                         filter_external: "#{name}-search",
    #                         filter_columnFilters: false
    #                     }}
    #                 }});
    #             </script>""".format(name=name, sort=self.sort,
    #                                 filter_liveSearch=session['settings']['minimum_jstree_search'])
    #
    #     return html + """
    #         <script>
    #             $("#{name}-table").tablesorter({{
    #                 {headers}
    #                 {sort}
    #                 dateFormat: "ddmmyyyy",
    #                 widgets: ["filter", "zebra"],
    #                 widgetOptions: {{
    #                     filter_liveSearch: {filter_liveSearch},
    #                     filter_external: "#{name}-search",
    #                     filter_columnFilters: false
    #                 }}}})
    #             .tablesorterPager({{
    #                 delayInit: true,
    #                 {remove_rows}
    #                 positionFixed: false,
    #                 container: $("#{name}-pager"),
    #                 size:{size}}});
    #         </script>""".format(name=name, sort=self.sort, size=table_rows,
    #                             remove_rows='removeRows: true,' if remove_rows else '',
    #                             filter_liveSearch=session['settings']['minimum_tablesorter_search'],
    #                             headers=self.headers)
