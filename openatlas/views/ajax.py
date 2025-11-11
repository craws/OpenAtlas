from typing import Optional

from flask import Response, abort, g, jsonify, request
from flask_babel import lazy_gettext as _

from openatlas import app
from openatlas.api.external.geonames import fetch_geonames
from openatlas.api.external.gnd import fetch_gnd
from openatlas.api.external.wikidata import fetch_wikidata
from openatlas.database.connect import Transaction
from openatlas.display.util import display_info, required_group
from openatlas.display.util2 import uc_first
from openatlas.models.entity import Entity, insert
from openatlas.models.user import User


@app.route('/ajax/bookmark', methods=['POST'])
@required_group('readonly')
def ajax_bookmark() -> Response:
    label = User.toggle_bookmark(int(request.form['entity_id']))
    label = _('bookmark') if label == 'bookmark' else _('bookmark remove')
    return jsonify(uc_first(label))


@app.route('/ajax/addtype', methods=['POST'])
@required_group('editor')
def ajax_add_type() -> str:
    root: Entity = g.types[int(request.form['superType'])]
    link = {'E55': 'P127', 'E53': 'P89'}
    Transaction.begin()
    try:
        entity = insert(
            data={
                'name': request.form['name'],
                'openatlas_class_name': root.class_.name,
                'cidoc_class_code': root.cidoc_class.code,
                'description': request.form['description']})
        entity.link(link[root.cidoc_class.code], root)
        g.logger.log_user(entity.id, 'insert')
        Transaction.commit()
    except Exception as _e:  # pragma: no cover
        Transaction.rollback()
        g.logger.log('error', 'ajax', _e)
        abort(400)
    return str(entity.id)


@app.route('/ajax/get_type_tree/<int:root_id>')
@required_group('readonly')
def ajax_get_type_tree(root_id: Optional[int] = None) -> str:
    return str(Entity.get_tree_data(root_id, []))


@app.route('/ajax/add_entity', methods=['POST'])
@required_group('editor')
def ajax_create_entity() -> str:
    Transaction.begin()
    try:
        entity = insert({
            'name': request.form['name'],
            'openatlas_class_name': request.form['entityName'],
            'description': request.form['description']})
        if 'standardType' in request.form and request.form['standardType']:
            entity.link('P2', g.types[int(request.form['standardType'])])
        g.logger.log_user(entity.id, 'insert')
        Transaction.commit()
    except Exception as _e:  # pragma: no cover
        Transaction.rollback()
        g.logger.log('error', 'ajax', _e)
        abort(400)
    return str(entity.id)


@app.route('/ajax/wikidata_info', methods=['POST'])
@required_group('readonly')
def ajax_wikidata_info() -> str:
    return display_info(fetch_wikidata(request.form['id_']))


@app.route('/ajax/geonames_info', methods=['POST'])
@required_group('readonly')
def ajax_geonames_info() -> str:
    return display_info(fetch_geonames(request.form['id_']))


@app.route('/ajax/gnd_info', methods=['POST'])
@required_group('readonly')
def ajax_gnd_info() -> str:
    return display_info(fetch_gnd(request.form['id_']))
