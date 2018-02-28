# Created 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import jsonify, request
from flask_login import current_user

from openatlas import app
from openatlas.models.user import UserMapper
from openatlas.util.util import required_group, uc_first


@app.route('/ajax/bookmark', methods=['POST'])
@required_group('readonly')
def ajax_bookmark():
    label = UserMapper.toggle_bookmark(request.form['entity_id'], current_user)
    return jsonify(uc_first(label))
