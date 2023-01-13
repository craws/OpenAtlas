from typing import Any, Optional, Union

from flask import json, render_template
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas.display.util import uc_first

# Needed for translations
_('previous')
_('next')
_('show')
_('entries')
_('showing %(first)s to %(last)s of %(all)s entries', first=1, last=25, all=38)


class Table:

    def __init__(
            self,
            header: Optional[list[str]] = None,
            rows: Optional[list[Any]] = None,
            order: Optional[list[list[Union[int, str]]]] = None,
            defs: Optional[list[dict[str, Any]]] = None,
            paging: bool = True) -> None:
        self.header = header or []
        self.rows = rows or []
        self.paging = paging
        self.order = order or ''
        self.defs = defs or []

    def display(self, name: str = 'default') -> str:
        if not self.rows:
            return '<p>' + uc_first(_('no entries')) + '</p>'
        self.defs.append({
            'className': 'dt-body-right',
            'targets': [
                i for i, name in enumerate(self.header)
                if name in ['begin', 'end', 'count', 'size']]})
        data = {
            'data': self.rows,
            'stateSave': 'true',
            'columns':
                [{'title': uc_first(_(item)) if item else ''}
                 for item in self.header] +
                [{'title': ''}  # Add empty
                 for _item in range(len(self.rows[0]) - len(self.header))],
            'paging': self.paging,
            'pageLength': current_user.settings['table_rows'],
            'autoWidth': 'false'}
        if self.order:
            data['order'] = self.order
        if self.defs:
            data['columnDefs'] = self.defs
        return render_template(
            'util/table.html',
            table=self,
            name=name,
            data=json.dumps(data))
