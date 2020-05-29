from flask import Response, json, request, jsonify
from flask import render_template
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.models.api import Api
from openatlas.util.util import api_access


# Todo: unit tests and Mypy checks


@app.route('/api/0.1/entity/<int:id_>')
@api_access()  # type: ignore
def api_entity(id_: int) -> Response:
    return jsonify(Api.get_entity(id_=id_))


@app.route('/api/0.1/entity/download/<int:id_>')
@api_access()  # type: ignore
def api_download_entity(id_: int) -> Response:
    # flash(_('Download successful'), 'info')
    return Response(json.dumps(Api.get_entity(id_=id_)),
                    mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})


@app.route('/api/0.1')
@api_access()  # type: ignore
def api_get_multiple_entities() -> Response:  # pragma: no cover
    entity = request.args.getlist('entity')
    return jsonify(Api.get_entities_by_id(ids=entity))


@app.route('/api/0.1/code/<code>')
@api_access()  # type: ignore
def api_get_by_code(code: str) -> Response:
    return jsonify(Api.get_entities_by_code(code_=code))


@app.route('/api/0.1/class/<class_code>')
@api_access()  # type: ignore
def api_get_by_class(class_code: str) -> Response:
    return jsonify(Api.get_entities_by_class(class_code_=class_code))


@app.route('/api/0.1/latest/<int:limit>')
@api_access()  # type: ignore
def api_get_latest(limit: int) -> Response:
    return jsonify(Api.get_entities_get_latest(limit_=limit))


@app.route('/api')
@api_access()  # type: ignore
def api_index() -> str:
    return render_template('api/index.html')
