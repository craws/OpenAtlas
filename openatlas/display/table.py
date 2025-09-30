from __future__ import annotations

from typing import Any, Optional

from flask import g, json, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas.display.util import (
    edit_link, link, profile_image_table_link, remove_link)
from openatlas.display.util2 import sanitize, uc_first
from openatlas.models.dates import format_date
from openatlas.models.entity import Entity, Link
from openatlas.models.openatlas_class import get_reverse_relation

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
                                         not in ['checkbox', 'remove',
                                                 'update'] else '',
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
        origin: Optional[Entity] = None,
        columns: Optional[list[str]] = None,
        additional_columns: Optional[list[str]] = None,
        relation: Optional[dict[Any, str]] = None,
        table_id: Optional[str] = None,
        forms: Optional[dict[str, Any]] = None) -> Table | None:
    from openatlas.views.entity_index import file_preview
    if not items:
        return Table()
    inverse = relation and relation['inverse']

    item = items[0]
    if isinstance(item, Link):
        if inverse:
            item_class = item.domain.class_
            default_columns = item.domain.class_.group['table_columns']
        else:
            item_class = item.range.class_
            default_columns = item.range.class_.group['table_columns']
    else:
        item_class = item.class_
        default_columns = item.class_.group['table_columns']

    order = None
    defs = None
    forms = forms or {}
    columns = (columns or default_columns) + (additional_columns or [])
    if forms.get('checkbox'):
        columns.insert(0, 'checkbox')
        order = [[0, "desc"], [1, "asc"]]
        defs = [{"orderDataType": "dom-checkbox", "targets": 0}]
    elif columns[0] == 'created':
        order = [[0, "desc"]]

    # Todo: implement file column
    # if classes[0] == 'file' and show_table_icons():
    #    table.columns.insert(1, _('icon'))

    if relation and relation['mode'].startswith('tab'):
        if relation['additional_fields']:
            columns.append('update')
        reverse_relation = get_reverse_relation(
            origin.class_,
            relation,
            item_class)
        if reverse_relation and not reverse_relation.get("required", True):
            columns.append("remove")

    table = Table(columns, order=order, defs=defs)
    for item in items:
        e = item
        range_ = None
        if isinstance(item, Link):
            e = item.domain if inverse else item.range
            range_ = item.range if inverse else item.domain
        data = []
        for name in columns:
            html = 'no table function'
            match name:
                case 'activity':
                    html = item.property.name_inverse
                case 'begin':
                    html = e.dates.first
                    if relation and 'dates' in relation['additional_fields']:
                        html = item.dates.first
                case 'checkbox':
                    html = f"""
                        <input
                            id="{e.id}"
                            name="values"
                            type="checkbox"
                            data-entity-name="{sanitize(e.name)}"
                            value="{e.id}" {
                    "checked" if e.id in forms.get('selection_ids', [])
                    else ""}>"""
                case 'class':
                    html = uc_first(e.class_.label)
                case 'created':
                    html = format_date(e.created)
                case 'creator':
                    if g.file_info.get(e.id):
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
                case 'icon':
                    html = f'<a href="{url_for("view", id_=e.id)}">' \
                        f'{file_preview(e.id)}</a>'
                case 'involvement' | 'function' | 'relation':
                    html = item.type.name if item.type else ''
                case 'last':
                    html = item.dates.last or \
                        '<span class="text-muted">' \
                        f'{range_.dates.last}</span>' \
                        if range_.dates.last else ''
                case 'license holder':
                    if g.file_info.get(e.id):
                        html = g.file_info[e.id]['license_holder']
                case 'main image':
                    html = profile_image_table_link(
                        origin,
                        e,
                        e.get_file_ext())
                # case name if name in g.classes[class_].relations:
                #    html = display_relations(
                #        e,
                #        g.classes[class_].relations[name])
                case 'name':
                    html = format_name_and_aliases(e, table_id, forms)
                case 'profile' if e and e.image_id:
                    html = 'Profile' if e.id == origin.image_id else link(
                        'profile',
                        url_for('file_profile', id_=e.id, entity_id=origin.id))
                case 'public':
                    if g.file_info.get(e.id):
                        html = _('yes') if g.file_info[e.id][
                            'public'] else None
                case 'remove':
                    tab_id = e.class_.group['name']
                    if relation and relation['mode'] == 'tab':
                        tab_id = relation['name']
                    html = ''
                    if not origin.root or not g.types[origin.root[0]].required:
                        html = remove_link(e.name, item, origin, tab_id)
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
                    html = link(e.standard_type)
                    if forms:
                        html = e.standard_type.name if e.standard_type else ''
                case 'update':
                    html = edit_link(
                        url_for(
                            'link_update',
                            id_=item.id,
                            origin_id=origin.id,
                            relation=relation['name']))
            data.append(html)
        table.rows.append(data)
    return table


def format_name_and_aliases(
        entity: Entity,
        table_id: str,
        forms: dict[str, Any]) -> str:
    if forms.get('mode') == 'single':
        link_ = f"""
            <a value="{entity.name}"
                href="#"
                onclick="selectFromTable(this,'{table_id}', {entity.id})"
            >{entity.name}</a>"""
        if not entity.aliases:
            return link_
        html = f'<p>{link_}</p>'
        for i, alias in enumerate(entity.aliases.values()):
            html += alias if i else f'<p>{alias}</p>'
        return html
    name = entity.name if forms else link(entity)
    if not entity.aliases or not current_user.settings['table_show_aliases']:
        return name
    return \
        f'{name}' \
        f'{"".join(f"<p>{alias}</p>" for alias in entity.aliases.values())}'
