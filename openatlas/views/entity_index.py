import datetime
from typing import Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.util.display import (convert_size, external_url, format_date, get_base_table_data,
                                    get_file_path, link)
from openatlas.util.table import Table
from openatlas.util.util import get_file_stats, is_authorized, required_group


@app.route('/index/<class_>')
@app.route('/index/<class_>/<int:delete_id>')
@required_group('readonly')
def index(class_: str, delete_id: Optional[int] = None) -> Union[str, Response]:
    if delete_id:
        url = delete_entity(class_, delete_id)
        if url:
            return redirect(url)
    return render_template('entity/index.html',
                           table=get_table(class_),
                           class_=class_,
                           gis_data=Gis.get_all() if class_ == 'place' else None)


def get_table(class_: str) -> Table:
    table = Table(Table.HEADERS[class_])
    if class_ == 'file':
        table = Table(['date'] + Table.HEADERS['file'])
        file_stats = get_file_stats()
        for entity in Entity.get_by_system_type('file', nodes=True):
            date = 'N/A'
            if entity.id in file_stats:
                date = format_date(
                    datetime.datetime.utcfromtimestamp(file_stats[entity.id]['date']))
            table.rows.append([
                date,
                link(entity),
                entity.print_base_type(),
                convert_size(file_stats[entity.id]['size']) if entity.id in file_stats else 'N/A',
                file_stats[entity.id]['ext'] if entity.id in file_stats else 'N/A',
                entity.description])
    elif class_ == 'reference_system':
        for entity in g.reference_systems.values():
            table.rows.append([
                link(entity),
                entity.count if entity.count else '',
                external_url(entity.website_url),
                external_url(entity.resolver_url),
                entity.placeholder,
                link(g.nodes[entity.precision_default_id]) if entity.precision_default_id else '',
                entity.description])
    else:
        if class_ == 'place':
            entities = Entity.get_by_system_type(
                'place',
                nodes=True,
                aliases=current_user.settings['table_show_aliases'])
        else:
            entities = Entity.get_by_menu_item(class_)
        table.rows = [get_base_table_data(item) for item in entities]
    return table


def delete_entity(class_: str, id_: int) -> Optional[str]:
    url = None
    if class_ == 'reference_system':
        entity = g.reference_systems[id_]
        if entity.system or not is_authorized('manager'):
            abort(403)
        if entity.forms:
            flash(_('Deletion not possible if forms are attached'), 'error')
            url = url_for('entity_view', id_=id_)

    if class_ == 'place':
        entity = Entity.get_by_id(id_)
        parent = None if entity.system_type == 'place' else entity.get_linked_entity('P46', True)
        if entity.get_linked_entities(['P46']):
            flash(_('Deletion not possible if subunits exists'), 'error')
            url = url_for('entity_view', id_=id_)
        entity.delete()
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
        if parent:
            tab = '#tab-' + entity.system_type.replace(' ', '-')
            url = url_for('entity_view', id_=parent.id) + tab
    else:
        Entity.delete_(id_)
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
        if class_ == 'file':
            try:
                path = get_file_path(id_)
                if path:  # Only delete file on disk if it exists to prevent a missing file error
                    path.unlink()
            except Exception as e:  # pragma: no cover
                logger.log('error', 'file', 'file deletion failed', e)
                flash(_('error file delete'), 'error')
    return url
