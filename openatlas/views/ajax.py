from flask import jsonify, request
from flask_babel import lazy_gettext as _

from openatlas import app
from openatlas.models.user import User
from openatlas.util.util import required_group, uc_first


@app.route('/ajax/bookmark', methods=['POST'])
@required_group('readonly')
def ajax_bookmark() -> str:
    label = User.toggle_bookmark(request.form['entity_id'])
    label = _('bookmark') if label == 'bookmark' else _('bookmark remove')
    return jsonify(uc_first(label))
