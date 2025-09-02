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
            columns: Optional[list[str]] = None,
            rows: Optional[list[Any]] = None,
            order: Optional[list[list[int | str]]] = None,
            defs: Optional[list[dict[str, Any]]] = None,
            paging: bool = True) -> None:
        self.columns = columns or []
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
                    for name in self.columns] + [
                    {'title': '', 'className': ''} for _item in
                    range(len(self.rows[0]) - len(self.columns))],
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
        items: list[Entity] | list[Link],
        entity_viewed: Optional[Entity] = None,
        columns: Optional[list[str]] = None,
        additional_columns: Optional[list[str]] = None,
        relation: Optional[dict[Any, str]] = None,
        table_id: Optional[str] = None) -> Table | None:
    if not items:
        return None
    inverse = relation and relation['inverse']
    if not columns:
        item = items[0]
        if isinstance(item, Entity):
            columns = item.class_.group['table_columns']
        if isinstance(item, Link):
            if inverse:
                columns = item.domain.class_.group['table_columns']
            else:
                columns = item.range.class_.group['table_columns']
    columns = columns + (additional_columns or [])
    if relation and relation['mode'].startswith('tab'):
        if relation['additional_fields']:
            columns.append('update')
        columns.append('remove')
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
                    html = item.dates.first
                case 'class':
                    html = e.class_.label
                case 'creator':
                    html = g.file_info[e.id]['creator']
                case 'content' | 'description':
                    html = e.description
                    if relation and name in relation['additional_fields']:
                        html = item.description
                case 'page':
                    html = item.description
                case 'end':
                    html = item.dates.last
                case 'extension':
                    html = e.get_file_ext()
                case 'first':
                    html = item.dates.first or \
                        '<span class="text-muted">' \
                        f'{range_.dates.first}</span>' \
                        if range_.dates.first else ''
                case 'involvement' | 'function' | 'relation':
                    html = item.type.name if item.type else ''
                case 'last':
                    html = item.dates.last or \
                        '<span class="text-muted">' \
                        f'{range_.dates.last}</span>' \
                        if range_.dates.last else ''
                case 'license holder':
                    html = g.file_info[e.id]['license_holder']
                case 'main image':
                    html = profile_image_table_link(
                        entity_viewed,
                        e,
                        e.get_file_ext())
                # case name if name in g.classes[class_].relations:
                #    html = display_relations(
                #        e,
                #        g.classes[class_].relations[name])
                case 'name':
                    html = format_name_and_aliases_for_form(e, table_id) \
                        if table_id else format_name_and_aliases(e, True)
                case 'profile' if e and e.image_id:
                    html = 'Profile' if e.id == entity_viewed.image_id \
                        else link(
                            'profile',
                            url_for(
                                'file_profile',
                                id_=e.id,
                                entity_id=entity_viewed.id))
                case 'public':
                    html = _('yes') if g.file_info[e.id]['public'] else None
                case 'remove':
                    tab_id = e.class_.group['name']
                    if relation and relation['mode'] == 'tab':
                        tab_id = relation['name']
                    html = remove_link(
                        e.name,
                        item,
                        entity_viewed,
                        tab_id.replace('_', '-'))
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
                            origin_id=entity_viewed.id,
                            relation=relation['name']))
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
