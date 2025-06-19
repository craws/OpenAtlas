from typing import Any, Optional

from flask import g, json, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas.display.util import link
from openatlas.display.util2 import convert_size, uc_first
from openatlas.models.entity import Entity

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
            order: Optional[list[list[int | str]]] = None,
            defs: Optional[list[dict[str, Any]]] = None,
            paging: bool = True) -> None:
        self.header = header or []
        self.rows = rows or []
        self.paging = paging
        self.order = order or ''
        self.defs = defs or []

    def display(self, name: str = 'default') -> str:
        if not self.rows:
            return '<p class="uc-first">' + _('no entries') + '</p>'
        data = {
            'data': self.rows,
            'stateSave': 'true',
            'columns': [{
                    'title': uc_first(_(name)) if name else '',
                    'className': 'dt-body-right'
                    if name in ['count', 'size'] else ''}
                for name in self.header] + [
                {'title': '', 'className': ''}
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


def entity_table(
        class_: str,
        entities: list[Entity],
        entity: Optional[Entity] = None,
        additional_columns: Optional[list[str]] = None) -> Table:
    columns = g.table_headers[class_] + (
        additional_columns if additional_columns else [])
    table = Table(columns)
    file_stats = g.file_info
    for e in entities:
        data = []
        for name in columns:
            html: str | list[str] = 'no table function'
            match name:
                case 'begin':
                    html = e.first
                case 'class':
                    html = e.class_.label
                # case 'delete':
                #    html = remove_link(e, entity)
                case 'description' | 'content':
                    html = e.description or ''
                case 'end':
                    html = e.last
                case 'ext':
                    html = file_stats[e.id]['ext'] \
                        if e.id in file_stats else 'N/A'
                # case name if name in g.classes[class_].relations:
                #    html = display_relations(
                #        e,
                #        g.classes[class_].relations[name])
                case 'name':
                    html = link(e)
                case 'profile' if entity and entity.image_id:
                    html = 'Profile' if e.id == entity.image_id else link(
                        'profile',
                        url_for('file_profile', id_=e.id, entity_id=entity.id))
                case 'remove':
                    html = 'Todo'
                # case 'related':
                #    relative = e.get_linked_entity_safe('has relation', True)
                #    if entity and relative.id == entity.id:
                #        relative = e.get_linked_entity_safe('has related')
                #    html = link(relative)
                # case 'relation type' if entity:
                #    html = e.types[0].get_name_directed(
                #        e.get_linked_entity_safe('has relation', True).id
                #        != entity.id)
                case 'size':
                    html = convert_size(file_stats[e.id]['size']) \
                        if e.id in file_stats else 'N/A'
                case 'type':
                    html = e.standard_type.name if e.standard_type else ''
                # case 'update':
                #    html = link_update(e, entity)
            data.append(html)
        table.rows.append(data)
    return table
