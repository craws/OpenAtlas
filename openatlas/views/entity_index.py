from typing import Union

from flask import g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.image_processing import check_processed_image
from openatlas.display.table import Table
from openatlas.display.util import (
    button, format_date, get_base_table_data, get_file_path, is_authorized,
    link, manual, required_group, check_iiif_file_exist)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis


@app.route('/index/<view>')
@required_group('readonly')
def index(view: str) -> Union[str, Response]:
    buttons = [manual(f'entity/{view}')]
    for name in g.view_class_mapping[view] if view != 'place' else ['place']:
        if is_authorized(g.classes[name].write_access):
            buttons.append(
                button(
                    g.classes[name].label,
                    url_for('insert', class_=name),
                    tooltip_text=g.classes[name].get_tooltip()))
    return render_template(
        'entity/index.html',
        class_=view,
        table=get_table(view),
        buttons=buttons,
        gis_data=Gis.get_all() if view == 'place' else None,
        title=_(view.replace('_', ' ')),
        crumbs=[[_('admin'), url_for('admin_index')], _('file')]
        if view == 'file' else [_(view).replace('_', ' ')])


def get_table(view: str) -> Table:
    table = Table(g.table_headers[view])
    if view == 'file':
        table.order = [[0, 'desc']]
        table.header = ['date'] + table.header
        if (g.settings['image_processing'] or app.config['IIIF']['enabled']) \
                and current_user.settings['table_show_icons']:
            table.header.insert(1, _('icon'))
        for entity in Entity.get_by_class('file', types=True):
            data = [
                format_date(entity.created),
                link(entity),
                link(entity.standard_type),
                entity.get_file_size(),
                entity.get_file_ext(),
                entity.description]
            if (g.settings['image_processing']
                or app.config['IIIF']['enabled']) \
                    and current_user.settings['table_show_icons']:
                data.insert(1, file_preview(entity.id))
            table.rows.append(data)
    elif view == 'reference_system':
        for system in g.reference_systems.values():
            table.rows.append([
                link(system),
                system.count or '',
                link(system.website_url, system.website_url, external=True),
                link(system.resolver_url, system.resolver_url, external=True),
                system.placeholder,
                link(g.types[system.precision_default_id])
                if system.precision_default_id else '',
                system.description])
    else:
        classes = 'place' if view == 'place' else g.view_class_mapping[view]
        entities = Entity.get_by_class(classes, types=True, aliases=True)
        table.rows = [get_base_table_data(entity) for entity in entities]
    return table


def file_preview(entity_id: int) -> str:
    size = app.config['IMAGE_SIZE']['table']
    param = "loading='lazy' alt='image' max-width='100px' max-height='100px'"
    if app.config['IIIF']['enabled'] and check_iiif_file_exist(entity_id):
        ext = '.tiff' if app.config['IIIF']['conversion'] \
            else g.files[entity_id].suffix
        url = (f"{app.config['IIIF']['url']}{entity_id}{ext}"
               f"/full/!100,100/0/default.jpg")
        return f"<img src='{url}' {param}>" \
            if ext in g.display_file_ext else ''
    if icon_path := get_file_path(
            entity_id,
            app.config['IMAGE_SIZE']['table']):
        url = url_for('display_file', filename=icon_path.name, size=size)
        return f"<img src='{url}' {param}>"
    path = get_file_path(entity_id)
    if path and check_processed_image(path.name):
        if icon := get_file_path(entity_id, app.config['IMAGE_SIZE']['table']):
            url = url_for('display_file', filename=icon.name, size=size)
            return f"<img src='{url}' {param}>"
    return ''
