from flask import Response, json, jsonify, request
from flask import render_template
from werkzeug.wrappers import Response  # type: ignore

from openatlas import app
from openatlas.models.api import Api
from openatlas.models.api_error import APIError
from openatlas.util.util import api_access


# Todo: unit tests and mypy checks


@app.route('/api/0.1/entity/<int:id_>', methods=['GET'])
@api_access()  # type: ignore
def api_entity(id_: int) -> Response:
    if type(id_) is int:
        return jsonify(Api.get_entity(id_=id_))
    else:
        raise APIError('Syntax is incorrect!', status_code="404b")


@app.route('/api/0.1/entity/download/<int:id_>', methods=['GET'])
@api_access()  # type: ignore
def api_download_entity(id_: int) -> Response:
    # flash(_('Download successful'), 'info')
    return Response(json.dumps(Api.get_entity(id_=id_)),
                    mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})


@app.route('/api/0.1', methods=['GET'])
@api_access()  # type: ignore
def api_get_multiple_entities() -> Response:  # pragma: no cover
    entity = request.args.getlist('entity')
    return jsonify(Api.get_entities_by_id(ids=entity))


@app.route('/api/0.1/code/<code>', methods=['GET'])
@api_access()  # type: ignore
def api_get_by_menu_item(code: str) -> Response:
    try:
        Api.get_entities_by_menu_item(code_=code)
        return jsonify(Api.get_entities_by_menu_item(code_=code))
    except Exception:
        raise APIError('Syntax is incorrect!', status_code="404c")


@app.route('/api/0.1/class/<class_code>', methods=['GET'])
@api_access()  # type: ignore
def api_get_by_class(class_code: str) -> Response:
    if len(Api.get_entities_by_class(class_code_=class_code)) == 0:
        raise APIError('Syntax is incorrect!', status_code="404d")
    return jsonify(Api.get_entities_by_class(class_code_=class_code))


@app.route('/api/0.1/latest/<int:limit>', methods=['GET'])
@api_access()  # type: ignore
def api_get_latest(limit: int) -> Response:
    if 0 < limit < 100:
        return jsonify(Api.get_entities_get_latest(limit_=limit))
    else:
        raise APIError('Syntax is incorrect!', status_code="404e")


@app.route('/api')
@api_access()  # type: ignore
def api_index() -> str:
    return render_template('api/index.html')
