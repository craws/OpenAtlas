# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import jsonify, request

from openatlas import app
from openatlas.models.user import UserMapper
from openatlas.util.util import required_group, uc_first


@app.route('/ajax/bookmark', methods=['POST'])
@required_group('readonly')
def ajax_bookmark() -> str:
    label = UserMapper.toggle_bookmark(request.form['entity_id'])
    return jsonify(uc_first(label))
