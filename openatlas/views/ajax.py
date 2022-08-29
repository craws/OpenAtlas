from typing import Optional

from flask import abort, g, jsonify, request
from flask_babel import lazy_gettext as _
import json

from openatlas import app
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

@app.route('/ajax/add_entity', methods=['POST'])
@required_group('editor')
def ajax_create_entity() -> str:
    try:
        entity = Entity.insert(
            request.form['entityName'],
            request.form['name'],
            request.form['description'])
        if request.form['entityName'] in ['artifact', 'feature', 'place', 'stratigraphic_unit']:
            entity.link(
                'P53',
                Entity.insert('object_location', f'Location of {request.form["name"]}'))
        if 'standardType' in request.form and request.form['standardType']:
            entity.link('P2',
                        g.types[int(request.form['standardType'])])
    except Exception as _e:
        g.logger.log('error', 'ajax',  _e)
        abort(400)
    return str(entity.id)


@app.route('/ajax/get_entity_table/<string:content_domain>', methods=['POST'])
@required_group('readonly')
def ajax_get_entity_table(content_domain: str) -> str:
    try:
        filter_ids = json.loads(request.form['filterIds']) or []
        table,selection = get_table_content(content_domain, None, filter_ids)
    except Exception as _e:  # pragma: no cover
        g.logger.log('error', 'ajax', _e)
        abort(400)
    return table.display(content_domain)


def format_name_and_aliases(entity: Entity, field_id: str) -> str:
   link = f"""<a href='#' onclick="selectFromTable(this,
       '{field_id}', {entity.id})">{entity.name}</a>"""
   if not entity.aliases:
       return link
   html = f'<p>{link}</p>'
   for i, alias in enumerate(entity.aliases.values()):
       html += alias if i else f'<p>{alias}</p>'
   return html
