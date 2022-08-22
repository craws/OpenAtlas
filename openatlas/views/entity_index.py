import datetime
from typing import Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.image_processing import check_processed_image
from openatlas.util.table import Table
from openatlas.util.util import (
    button, external_url, format_date, get_base_table_data, get_file_path,
    is_authorized, link, required_group)


@app.route('/index/<view>')
@app.route('/index/<view>/<int:delete_id>')
@required_group('readonly')
def index(view: str, delete_id: Optional[int] = None) -> Union[str, Response]:
    if delete_id:  # Delete before showing index to prevent additional redirect
        if current_user.group == 'contributor':  # pragma: no cover
            info = g.logger.get_log_info(delete_id)
            if not info['creator'] or info['creator'].id != current_user.id:
                abort(403)
        if url := delete_entity(delete_id):
            return redirect(url)
    return render_template(
        'entity/index.html',
        class_=view,
        table=get_table(view),
        buttons=get_buttons(view),
        gis_data=Gis.get_all() if view == 'place' else None,
        title=_(view.replace('_', ' ')),
        crumbs=[[_('admin'), url_for('admin_index')], _('file')]
        if view == 'file' else [_(view).replace('_', ' ')])


def get_buttons(view: str) -> list[str]:
    buttons = []
    for name in [view] if view in ['artifact', 'place'] \
            else g.view_class_mapping[view]:
        if is_authorized(g.classes[name].write_access):
            buttons.append(
                button(g.classes[name].label, url_for('insert', class_=name)))
    return buttons


def get_table(view: str) -> Table:
    header = g.table_headers[view]
    if view == 'file':
        header = ['date'] + header
        if g.settings['image_processing'] \
                and current_user.settings['table_show_icons']:
            header.insert(1, _('icon'))
    table = Table(header)
    if view == 'file':
        for entity in Entity.get_by_class('file', types=True):
            date = 'N/A'
            if entity.id in g.file_stats:
                date = format_date(
                    datetime.datetime.utcfromtimestamp(
                        g.file_stats[entity.id]['date']))
            data = [
                date,
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
                external_url(system.website_url),
                external_url(system.resolver_url),
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
    url = None
    entity = Entity.get_by_id(id_)
    if not is_authorized(entity.class_.write_access):
        abort(403)  # pragma: no cover
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
