from typing import Optional

from flask import abort, g, jsonify, request
from flask_babel import lazy_gettext as _
import json

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.forms.util import get_table_content
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
    Transaction.begin()
    try:
        entity = Entity.insert(
            cidoc_name[cidoc_code],
            request.form['name'],
            request.form['description'])
        entity.link(link[cidoc_code], g.types[int(request.form['superType'])])
        Transaction.commit()
        return str(entity.id)
    except Exception as _e:  # pragma: no cover
        Transaction.rollback()
        abort(400)


@app.route('/ajax/get_type_tree/<int:root_id>')
@required_group('readonly')
def ajax_get_type_tree(root_id: Optional[int] = None) -> str:
    return str(Type.get_tree_data(root_id, []))

@app.route('/ajax/add_entity', methods=['POST'])
@required_group('editor')
def ajax_create_entity() -> str:
    try:
        entity = Entity.insert(
            request.form['entityName'],
            request.form['name'],
            request.form['description'])
        if request.form['entityName'] in \
                ['artifact', 'feature', 'place', 'stratigraphic_unit']:
            entity.link(
                'P53',
                Entity.insert(
                    'object_location',
                    f'Location of {request.form["name"]}'))
        if 'standardType' in request.form and request.form['standardType']:
            entity.link(
                'P2',
                g.types[int(request.form['standardType'])])
        return str(entity.id)
    except Exception as _e:  # pragma: no cover
        g.logger.log('error', 'ajax', _e)
        abort(400)


@app.route('/ajax/get_entity_table/<string:content_domain>', methods=['POST'])
@required_group('readonly')
def ajax_get_entity_table(content_domain: Optional[str] = None) -> str:
    try:
        filter_ids = json.loads(request.form['filterIds']) or []
        table, selection = get_table_content(content_domain, None, filter_ids)
        return table.display(content_domain)
    except Exception as _e:  # pragma: no cover
        g.logger.log('error', 'ajax', _e)
        abort(400)

