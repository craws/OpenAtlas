from typing import Any, Optional

from flask import g, json, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas.display.util import (
    edit_link, format_name_and_aliases, link, profile_image_table_link,
    remove_link)
from openatlas.display.util2 import uc_first
from openatlas.models.entity import Entity, Link

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
                'title':
                    uc_first(_(name)) if name and name
                    not in ['update', 'remove'] else '',
                'className':
                    'dt-body-right' if name in ['count', 'size'] else ''}
                    for name in self.header] + [
                    {'title': '', 'className': ''} for _item in
                    range(len(self.rows[0]) - len(self.header))],
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
        items: list[Entity] | list[Link],
        entity: Optional[Entity] = None,
        columns: Optional[list[str]] = None,
        additional_columns: Optional[list[str]] = None,
        inverse: Optional[bool] = False,
        table_field_id: Optional[str] = None) -> Table:
    if not columns:
        columns = (g.table_headers[g.classes[class_].view] + (
            additional_columns if additional_columns else []))
    table = Table(columns)
    for item in items:
        e = item
        range_ = None
        if isinstance(item, Link):
            e = item.domain if inverse else item.range
            range_ = item.range if inverse else item.domain
        data = []
        for name in columns:
            html: str | list[str] = 'no table function'
            match name:
                case 'activity':
                    html = item.property.name_inverse
                case 'begin':
                    html = e.first
                case 'class':
                    html = e.class_.label
                case 'creator':
                    html = g.file_info[e.id]['creator']
                case 'description' | 'content':
                    html = item.description or ''
                case 'end':
                    html = e.last
                case 'extension':
                    html = e.get_file_ext()
                case 'first':
                    html = item.first or \
                        f'<span class="text-muted">{range_.first}</span>' \
                        if range_.first else ''
                case 'involvement':
                    html = item.type.name if item.type else ''
                case 'last':
                    html = item.last or \
                        f'<span class="text-muted">{range_.last}</span>' \
                        if range_.last else ''
                case 'license holder':
                    html = g.file_info[e.id]['license_holder']
                case 'main image':
                    html = \
                        profile_image_table_link(e, e, e.get_file_ext())
                # case name if name in g.classes[class_].relations:
                #    html = display_relations(
                #        e,
                #        g.classes[class_].relations[name])
                case 'name':
                    html = format_name_and_aliases_for_form(
                        e,
                        table_field_id) if table_field_id \
                        else format_name_and_aliases(e, True)
                case 'page':
                    html = item.description
                case 'profile' if e and e.image_id:
                    html = 'Profile' if e.id == entity.image_id else link(
                        'profile',
                        url_for('file_profile', id_=e.id, entity_id=entity.id))
                case 'public':
                    html = _('yes') if g.file_info[e.id]['public'] else None
                case 'remove':
                    html = remove_link(e.name, item, e, e.class_.view)
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
                    html = e.get_file_size()
                case 'type' | 'license':
                    html = e.standard_type.name if e.standard_type else ''
                case 'update':
                    html = edit_link(
                        url_for(
                            'link_update',
                            id_=item.id,
                            origin_id=entity.id))
            data.append(html)
        table.rows.append(data)
    return table


def format_name_and_aliases_for_form(entity: Entity, field_id: str) -> str:
    link_ = \
        f"""<a value="{entity.name}"  href='#' onclick="selectFromTable(this,
        '{field_id}', {entity.id})">{entity.name}</a>"""
    if entity.aliases:
        html = f'<p>{link_}</p>'
        for i, alias in enumerate(entity.aliases.values()):
            html += alias if i else f'<p>{alias}</p>'
        return html
    return link_
