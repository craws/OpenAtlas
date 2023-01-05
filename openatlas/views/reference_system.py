from flask import flash, g, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.util.util import required_group


@app.route(
    '/reference_system/remove_class/<int:system_id>/<class_name>',
    methods=['POST', 'GET'])
@required_group('manager')
def reference_system_remove_class(system_id: int, class_name: str) -> Response:
    try:
        g.reference_systems[system_id].remove_class(class_name)
        flash(_('info update'), 'info')
    except Exception as e:
        g.logger.log('error', 'database', 'remove form failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('view', id_=system_id))
