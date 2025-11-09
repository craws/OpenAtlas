from __future__ import annotations

from typing import Any, Optional

from flask import g, json, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user

from openatlas import app
from openatlas.display.image_processing import check_processed_image
from openatlas.display.util import (
    check_iiif_file_exist, edit_link, get_file_path, link,
    profile_image_table_link, remove_link)
from openatlas.display.util2 import (
    display_bool, is_authorized, sanitize, uc_first)
from openatlas.models.dates import format_date
from openatlas.models.entity import Entity, Link
from openatlas.models.openatlas_class import Relation, get_reverse_relation
from openatlas.models.overlay import Overlay

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
        no_title = ['checkbox', 'remove', 'set logo', 'update']
        data = {
            'data': self.rows,
            'stateSave': 'true',
            'columns': [{
                'title':
                    uc_first(_(name.replace('_', ' ')))
                    if name and name not in no_title else '',
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
        relation: Optional[Relation] = None,
        table_id: Optional[str] = None,
        forms: Optional[dict[str, Any]] = None) -> Table:
    if not items:
        return Table()
    inverse = relation and relation.inverse
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

    if relation and relation.mode.startswith('tab'):
        if relation.additional_fields:
            columns.append('update')
        reverse_relation = get_reverse_relation(
            origin.class_,
            relation,
            item_class)
        if not reverse_relation or not reverse_relation.required:
            columns.append('remove')

    overlays = Overlay.get_by_object(origin) \
        if origin and 'overlay' in columns else {}
    table = Table(columns, order=order, defs=defs)
    for item in items:
        e = item
        range_ = None
        if isinstance(item, Link):
            e = item.domain if inverse else item.range
            range_ = item.range if inverse else item.domain
            if e.class_.name == 'object_location':
                e = e.get_linked_entity_safe('P53', inverse=False, types=True)
        data = []
        for name in columns:
            html = 'no table function'
            match name:
                case 'activity':
                    html = item.property.name_inverse
                case 'begin':
                    html = table_date('first', e, range_, item)
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
                    html = e.class_.label
                case 'created':
                    html = format_date(e.created)
                case 'creator':
                    html = ''
                    if g.file_info.get(e.id):
                        html = g.file_info[e.id]['creator']
                case 'content' | 'description':
                    html = e.description
                    if relation and name in relation.additional_fields:
                        html = item.description
                case 'count':
                    html = format_number(e.count)
                case 'domain':
                    html = link(e)
                case 'default_precision':
                    html = link(next(iter(e.types), None))
                case 'end':
                    html = table_date('last', e, range_, item)
                case 'example_id':
                    html = e.example_id
                case 'extension':
                    html = e.get_file_ext()
                case 'external_reference_match':
                    html = item.description
                    if url := origin.resolver_url:
                        html = link(
                            item.description,
                            url + item.description,
                            external=True)
                case 'icon':
                    html = f'<a href="{url_for("view", id_=e.id)}">' \
                        f'{file_preview(e.id)}</a>'
                case 'involvement' | 'function' | 'relation':
                    html = item.type.name if item.type else ''
                case 'license_holder':
                    html = ''
                    if g.file_info.get(e.id):
                        html = g.file_info[e.id]['license_holder']
                case 'main_image':
                    html = profile_image_table_link(
                        origin,
                        e,
                        e.get_file_ext())
                case 'name':
                    html = format_name_and_aliases(e, table_id, forms)
                case 'page':
                    html = item.description
                case 'precision':
                    html = item.type.name
                case 'profile' if e and e.image_id:
                    html = 'Profile' if e.id == origin.image_id else link(
                        'profile',
                        url_for('file_profile', id_=e.id, entity_id=origin.id))
                case 'overlay':
                    html = ''
                    if is_authorized('editor') \
                            and current_user.settings['module_map_overlay'] \
                            and e.get_file_ext() \
                            in app.config['DISPLAY_FILE_EXT']:
                        if e.id in overlays:
                            html = edit_link(
                                url_for(
                                    'overlay_update',
                                    place_id=origin.id,
                                    overlay_id=overlays[e.id].id))
                        else:
                            html = link(
                                _('link'),
                                url_for(
                                    'overlay_insert',
                                    image_id=e.id,
                                    place_id=origin.id))
                case 'public':
                    html = ''
                    if g.file_info.get(e.id):
                        html = display_bool(g.file_info[e.id]['public'], False)
                case 'range':
                    html = link(range_)
                case 'remove':
                    tab_id = e.class_.group['name']
                    if relation and relation.mode == 'tab':
                        tab_id = relation.name
                    html = ''
                    if not origin.root or not g.types[origin.root[0]].required:
                        html = remove_link(e.name, item, origin, tab_id)
                case 'set logo':
                    html = link(_('set'), url_for('logo', id_=e.id))
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
                            relation=relation.name))
                case 'resolver_url' | 'website_url':
                    url = getattr(e, name)
                    html = link(url, url, external=True) if url else ''
                case 'value':
                    html = format_number(item.description)
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


def file_preview(entity_id: int) -> str:
    size = app.config['IMAGE_SIZE']['table']
    param = "loading='lazy' alt='image' max-width='100px' max-height='100px'"
    if g.settings['iiif'] and check_iiif_file_exist(entity_id):
        ext = '.tiff' if g.settings['iiif_conversion'] \
            else g.files[entity_id].suffix
        url =\
            f"{g.settings['iiif_url']}{entity_id}{ext}" \
            f"/full/!100,100/0/default.jpg"
        return f"<img src='{url}' {param}>"
    if icon := get_file_path(entity_id, app.config['IMAGE_SIZE']['table']):
        url = url_for('display_file', filename=icon.name, size=size)
        return f"<img src='{url}' {param}>"
    if g.settings['image_processing']:
        path = get_file_path(entity_id)
        if path and check_processed_image(path.name):
            if icon := get_file_path(
                    entity_id,
                    app.config['IMAGE_SIZE']['table']):
                url = url_for('display_file', filename=icon.name, size=size)
                return f"<img src='{url}' {param}>"
    return ''


def table_date(
        mode: str,
        e: Entity,
        range_: Entity | None,
        item: Link | Entity | None) -> str:
    html = getattr(e.dates, mode)
    if range_ \
            and range_.class_.group \
            and not (html := getattr(item.dates, mode)):
        if e.class_.group['name'] == 'actor' \
                and range_.class_.group['name'] == 'event' \
                and getattr(range_.dates, mode):
            html = getattr(range_.dates, mode)
        elif e.class_.group['name'] == 'event' \
                and range_.class_.group['name'] == 'actor' \
                and getattr(e.dates, mode):
            html = getattr(e.dates, mode)
        html = f'<span class="text-muted">{html}</span>' if html else ''
    return html
