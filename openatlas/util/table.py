# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Optional

from flask import json
from flask_babel import lazy_gettext as _


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
        from openatlas.util.util import uc_first
        if not self.rows:
            return '<p>' + uc_first(_('no entries')) + '</p>'

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
