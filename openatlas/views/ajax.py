from typing import Optional

from flask import abort, g, jsonify, request
from flask_babel import lazy_gettext as _

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.models.user import User
from openatlas.util.util import required_group, uc_first


@app.route('/ajax/bookmark', methods=['POST'])
@required_group('readonly')
def ajax_bookmark() -> str:
    label = User.toggle_bookmark(request.form['entity_id'])
    label = _('bookmark') if label == 'bookmark' else _('bookmark remove')
    return jsonify(uc_first(label))


@app.route('/ajax/addtype', methods=['POST'])
@required_group('editor')
def ajax_add_type() -> str:
    link = {'E55': 'P127', 'E53': 'P89'}
    cidoc_name = {'E55': 'type', 'E53': 'administrative_unit'}
    cidoc_code = g.types[int(request.form['superType'])].cidoc_class.code
    entity = Entity.insert(
        cidoc_name[cidoc_code],
        request.form['name'],
        request.form['description'])
    try:
        entity.link(link[cidoc_code], g.types[int(request.form['superType'])])
    except Exception as _e:  # pragma: no cover
        entity.delete()
        abort(400)
    return str(entity.id)


@app.route('/ajax/get_type_tree/<int:root_id>')
@required_group('readonly')
def ajax_get_type_tree(root_id: Optional[int] = None) -> str:
    return str(Type.get_tree_data(root_id, []))
