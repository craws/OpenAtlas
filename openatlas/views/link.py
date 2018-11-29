# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, g, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect

from openatlas import app, logger
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import (get_view_name, required_group)


@app.route('/link/delete/<int:id_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def link_delete(id_, origin_id):
    g.cursor.execute('BEGIN')
    try:
        LinkMapper.delete_by_id(id_)
        g.cursor.execute('COMMIT')
        flash(_('link removed'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    origin = EntityMapper.get_by_id(origin_id)
    return redirect(url_for(get_view_name(origin) + '_view', id_=origin.id))
