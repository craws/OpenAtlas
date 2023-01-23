from typing import Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.image_processing import check_processed_image
from openatlas.display.table import Table
from openatlas.display.util import (
    button, format_date, get_base_table_data, get_file_path, is_authorized,
    link, manual, required_group)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.reference_system import ReferenceSystem


@app.route('/index/<view>')
@app.route('/index/<view>/<int:delete_id>')
@required_group('readonly')
def index(view: str, delete_id: Optional[int] = None) -> Union[str, Response]:
    if delete_id:  # Delete before showing index to prevent redirects
        if url := delete_entity(delete_id):
            return redirect(url)
    return render_template(
        'entity/index.html',
        class_=view,
        table=get_table(view),
        buttons=[manual(f'entity/{view}')] + get_buttons(view),
        gis_data=Gis.get_all() if view == 'place' else None,
        title=_(view.replace('_', ' ')),
        crumbs=[[_('admin'), url_for('admin_index')], _('file')]
        if view == 'file' else [_(view).replace('_', ' ')])


def get_buttons(view: str) -> list[str]:
    buttons = []
    for name in g.view_class_mapping[view] if view != 'place' else ['place']:
        if is_authorized(g.classes[name].write_access):
            buttons.append(
                button(g.classes[name].label, url_for('insert', class_=name)))
    return buttons


def get_table(view: str) -> Table:
    table = Table(g.table_headers[view])
    if view == 'file':
        table.order = [[0, 'desc']]
        table.header = ['date'] + table.header
        if g.settings['image_processing'] \
                and current_user.settings['table_show_icons']:
            table.header.insert(1, _('icon'))
        for entity in Entity.get_by_class('file', types=True):
            data = [
                format_date(entity.created),
                link(entity),
                link(entity.standard_type),
                g.file_stats[entity.id]['size']
                if entity.id in g.file_stats else 'N/A',
                g.file_stats[entity.id]['ext']
                if entity.id in g.file_stats else 'N/A',
                entity.description]
            if g.settings['image_processing'] \
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
    parameter = f"loading='lazy' alt='image' width='{size}'"
    if icon_path := get_file_path(
            entity_id,
            app.config['IMAGE_SIZE']['table']):
        url = url_for('display_file', filename=icon_path.name, size=size)
        return f"<img src='{url}' {parameter}>"
    path = get_file_path(entity_id)
    if path and check_processed_image(path.name):
        if icon := get_file_path(entity_id, app.config['IMAGE_SIZE']['table']):
            url = url_for('display_file', filename=icon.name, size=size)
            return f"<img src='{url}' {parameter}>"
    return ''


def delete_entity(id_: int) -> Optional[str]:
    if current_user.group == 'contributor':
        info = g.logger.get_log_info(id_)
        if not info['creator'] or info['creator'].id != current_user.id:
            abort(403)
    entity = Entity.get_by_id(id_)
    if not is_authorized(entity.class_.write_access):
        abort(403)
    url = None
    if isinstance(entity, ReferenceSystem):
        if entity.system:
            abort(403)
        if entity.classes:
            flash(_('Deletion not possible if classes are attached'), 'error')
            return url_for('view', id_=id_)
        url = url_for('index', view='reference_system')
    elif entity.class_.view in ['artifact', 'place']:
        if entity.get_linked_entities('P46'):
            flash(_('Deletion not possible if subunits exists'), 'error')
            return url_for('view', id_=id_)
        if entity.class_.name != 'place':
            if parent := entity.get_linked_entity('P46', True):
                url = \
                    f"{url_for('view', id_=parent.id)}" \
                    f"#tab-{entity.class_.name.replace('_', '-')}"
    elif entity.class_.name == 'source_translation':
        source = entity.get_linked_entity_safe('P73', inverse=True)
        url = f"{url_for('view', id_=source.id)}#tab-text"
    elif entity.class_.name == 'file':
        try:
            delete_files(id_)
        except Exception as e:  # pragma: no cover
            g.logger.log('error', 'file', 'file deletion failed', e)
            flash(_('error file delete'), 'error')
            return url_for('view', id_=id_)
    entity.delete()
    g.logger.log_user(id_, 'delete')
    flash(_('entity deleted'), 'info')
    return url


def delete_files(id_: int) -> None:
    if path := get_file_path(id_):  # Prevent missing file warning
        path.unlink()
    for resized_path in app.config['RESIZED_IMAGES'].glob(f'**/{id_}.*'):
        resized_path.unlink()
