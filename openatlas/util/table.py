from typing import Any, Dict, List, Optional, Union

from flask import json, session
from flask_babel import lazy_gettext as _
from flask_login import current_user


class Table:
    HEADERS = {'actor': ['name', 'class', 'begin', 'end'],
               'event': ['name', 'class', 'type', 'begin', 'end'],
               'feature': ['name', 'type', 'begin', 'end'],
               'find': ['name', 'type', 'begin', 'end'],
               'file': ['name', 'license', 'size', 'extension', 'description'],
               'group': ['name', 'class', 'begin', 'end'],
               'human-remains': ['name', 'type', 'begin', 'end'],
               'information_carrier': ['name', 'type'],
               'object': ['name', 'type'],
               'node': ['name'],
               'person': ['name', 'class', 'begin', 'end'],
               'place': ['name', 'type', 'begin', 'end'],
               'reference': ['name', 'class', 'type'],
               'source': ['name', 'type', 'description'],
               'stratigraphic-unit': ['name', 'type', 'begin', 'end']}

    def __init__(self,
                 header: Optional[List[str]] = None,  # A list of column header labels
                 rows: Optional[List[List[Any]]] = None,  # Rows containing the data
                 order: Optional[List[List[Union[int, str]]]] = None,  # Column order option
                 defs: Optional[List[Any]] = None,  # Definitions
                 paging: bool = True) -> None:  # Whether to show pager
        self.header = header if header else []
        self.rows = rows if rows else []
        self.paging = paging
        self.order = order if order else ''
        self.defs = defs if defs else ''

    def display(self, name: str = 'table') -> str:
        from openatlas.util.util import uc_first
        if not self.rows:
            return '<p>' + uc_first(_('no entries')) + '</p>'
        columns: List[Dict[str, str]] = [{'title': item.capitalize()} for item in self.header]
        columns += [{'title': ''} for i in range(len(self.rows[0]) - len(self.header))]  # Add empty
        table_rows = session['settings']['default_table_rows']
        if hasattr(current_user, 'settings'):
            table_rows = current_user.settings['table_rows']
        data_table = {'data': self.rows,
                      'stateSave': 'false' if session['settings']['debug_mode'] else 'true',
                      'columns': columns,
                      'paging': self.paging,
                      'pageLength': table_rows,
                      'autoWidth': 'false'}
        if self.order:
            data_table['order'] = self.order
        if self.defs:
            data_table['columnDefs'] = self.defs
        html = """
            <table id="{name}_table" class="table table-striped hover" style="width:100%"></table>
            <script>
                $(document).ready(function() {{ $('#{name}_table').DataTable({data_table}); }});
            </script>""".format(name=name, data_table=json.dumps(data_table),)

        # Toggle header and footer HTML
        css_header = '#{name}_table_wrapper table thead {{ display:none; }}'.format(name=name)
        css_toolbar = '#{name}_table_wrapper .fg-toolbar {{ display:none; }}'.format(name=name)
        html += '<style type="text/css">{header} {toolbar}</style>'.format(
            header=css_header if not self.header else '',
            toolbar=css_toolbar if len(self.rows) <= table_rows else '')
        return html
