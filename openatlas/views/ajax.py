from typing import Optional
import requests
from flask import Response, g, jsonify, render_template, request
from flask_babel import gettext as _

from config.model.class_groups import class_groups
from openatlas import app
# pylint: disable=unused-import
from openatlas.api.external.apis import APIS  # noqa
from openatlas.api.external.cadaster import Cadaster  # noqa
from openatlas.api.external.chronontology import ChronOntology  # noqa
from openatlas.api.external.doi import DOI # noqa
from openatlas.api.external.gettyaat import GettyAAT  # noqa
from openatlas.api.external.geonames import GeoNames  # noqa
from openatlas.api.external.gnd import GND  # noqa
from openatlas.api.external.kulturpool import Kulturpool  # noqa
from openatlas.api.external.openatlas_api import OpenAtlas  # noqa
from openatlas.api.external.orcid import ORCID  # noqa
from openatlas.api.external.ror import ROR  # noqa
from openatlas.api.external.wikidata import Wikidata  # noqa
from openatlas.api.external.viaf import VIAF  # noqa
from openatlas.database.api import get_entities_api
from openatlas.display.util import display_info, required_group
from openatlas.display.util2 import uc_first
from openatlas.models.entity import Entity, insert
from openatlas.models.user import User


@app.route('/ajax/duplicate_check')
@required_group('contributor')
def ajax_duplicate_check() -> str:
    search = request.args.get('search', '').strip()
    class_ = request.args.get('class_', '')
    min_length = 2
    search_classes = {
        cls for group in class_groups.values() for cls in group['classes']}
    if (len(search) < min_length
            or '\x00' in search
            or class_ not in search_classes):
        return ''
    limit = 6
    offset = max(0, request.args.get('offset', 0, type=int))
    exclude_id = request.args.get('exclude_id', type=int)
    rows, total = get_entities_api(
        [class_],
        limit=limit,
        offset=offset,
        search_name=search,
        phonetic=True,
        exclude_id=exclude_id)
    if not rows:
        return ''
    next_offset = offset + len(rows)
    return render_template(
        'forms/duplicate_check.html',
        rows=rows,
        total=total,
        search_lower=search.lower(),
        offset=offset,
        next_offset=next_offset,
        remaining=max(0, total - next_offset))


@app.route('/ajax/bookmark', methods=['POST'])
@required_group('readonly')
def ajax_bookmark() -> Response:
    label = User.toggle_bookmark(int(request.form['entity_id']))
    label = _('bookmark') if label == 'bookmark' else _('bookmark remove')
    return jsonify(uc_first(label))


@app.route('/ajax/type/add', methods=['POST'])
@required_group('editor')
def ajax_add_type() -> str:
    root: Entity = g.types[int(request.form['superType'])]
    link = {'E55': 'P127', 'E53': 'P89'}
    entity = insert(
        data={
            'name': request.form['name'],
            'openatlas_class_name': root.class_.name,
            'description': request.form['description']})
    entity.link(link[root.cidoc_class.code], root)
    g.logger.log_user(entity.id, 'insert')
    return str(entity.id)


@app.route('/ajax/type/tree/<int:root_id>')
@required_group('readonly')
def ajax_type_tree(root_id: Optional[int] = None) -> str:
    return str(Entity.get_tree_data(root_id, []))


@app.route('/ajax/entity/add', methods=['POST'])
@required_group('editor')
def ajax_create_entity() -> str:
    entity = insert({
        'name': request.form['name'],
        'openatlas_class_name': request.form['entityName'],
        'description': request.form['description']})
    if 'standardType' in request.form and request.form['standardType']:
        entity.link('P2', g.types[int(request.form['standardType'])])
    g.logger.log_user(entity.id, 'insert')
    return str(entity.id)


@app.route('/ajax/api/<int:system_id>', methods=['GET', 'POST'])
@required_group('readonly')
def ajax_external_api(system_id: int) -> str:
    system = g.reference_systems[system_id]
    return display_info(globals()[system.api]().get_info(
        request.form['id_'],
        system))


@app.route('/proxy/apis', methods=['GET'])
@required_group('readonly')
def apis_proxy() -> Response | tuple[Response, int]:
    system_url = request.args.get('system_url', '').rstrip('/')
    apis_api_url = f'{system_url}/api/entities/'
    try:
        response = requests.get(
            apis_api_url,
            params={
                'search': request.args.get('search', ''),
                'format': 'json'},
            headers=app.config['USER_AGENT'],
            timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            data = data['results']  # pragma: no cover
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e), 'results': []}), 502


@app.route('/proxy/crossref', methods=['GET'])
@required_group('readonly')
def crossref_proxy() -> Response | tuple[Response, int]:
    try:
        response = requests.get(
            'https://api.crossref.org/works',
            params={
                'query': request.args.get('query', ''),
                'rows': request.args.get('rows', '10')},
            headers=app.config['USER_AGENT'],
            proxies=app.config['PROXIES'],
            timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e), 'message': {'items': []}}), 502


@app.route('/proxy/orcid', methods=['GET'])
@required_group('readonly')
def orcid_proxy() -> Response | tuple[Response, int]:
    try:
        return jsonify({'items': ORCID.search(request.args.get('query', ''))})
    except requests.exceptions.RequestException as e:  # pragma: no cover
        return jsonify({'error': str(e), 'items': []}), 502


@app.route('/proxy/viaf', methods=['GET'])
@required_group('readonly')
def viaf_proxy() -> Response | tuple[Response, int]:
    try:
        response = requests.get(
            'https://viaf.org/viaf/AutoSuggest',
            params={'query': request.args.get('query', '')},
            headers={
                'Accept': 'application/json',
                **app.config['USER_AGENT']},
            proxies=app.config['PROXIES'],
            timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:  # pragma: no cover
        return jsonify({'error': str(e), 'result': []}), 502


@app.route('/proxy/ror', methods=['GET'])
@required_group('readonly')
def ror_proxy() -> Response | tuple[Response, int]:
    try:
        return jsonify({'items': ROR.search(request.args.get('query', ''))})
    except requests.exceptions.RequestException as e:  # pragma: no cover
        return jsonify({'error': str(e), 'items': []}), 502


@app.route('/proxy/chronontology', methods=['GET'])
@required_group('readonly')
def chronontology_proxy() -> Response | tuple[Response, int]:
    try:
        response = requests.get(
            'https://chronontology.dainst.org/data/period/',
            params={
                'q': request.args.get('q', ''),
                'size': request.args.get('size', '40')},
            headers={
                'Accept': 'application/json',
                **app.config['USER_AGENT']},
            proxies=app.config['PROXIES'],
            timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:  # pragma: no cover
        return jsonify({'error': str(e), 'results': []}), 502
