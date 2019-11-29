from flask import flash, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.models.link import LinkMapper
from openatlas.util.util import required_group


@app.route('/link/delete/<int:id_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def link_delete(id_: int, origin_id: int) -> Response:
    LinkMapper.delete(id_)
    flash(_('link removed'), 'info')
    return redirect(url_for('entity_view', id_=origin_id))
