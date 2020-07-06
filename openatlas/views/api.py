from flask import json, jsonify, render_template, request
from werkzeug.wrappers import Response  # type: ignore

from openatlas import app
from openatlas.models.api import Api
from openatlas.models.api_helpers.api_error import APIError
from openatlas.util.util import api_access
from openatlas.models.api_helpers.api_pagination import Pagination


# Todo: unit test


@app.route('/api/0.1/entity/<id_>')
@api_access()  # type: ignore
def api_entity(id_: int) -> Response:
    try:
        int(id_)
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
    return jsonify(Api.get_entity(id_=id_))


@app.route('/api/0.1/entity/download/<int:id_>')
@api_access()  # type: ignore
def api_download_entity(id_: int) -> Response:
    # flash(_('Download successful'), 'info')
    return Response(json.dumps(Api.get_entity(id_=id_)),
                    mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})


@app.route('/api/0.1/', methods=['GET', 'VIEW'])
@api_access()  # type: ignore
def api_get_entities_by_json() -> Response:  # pragma: nocover
    out = []
    req_data = request.get_json()
    if 'id' in req_data:
        entity = req_data['id']
        for e in entity:
            if type(e) is int:
                out.append(Api.get_entity(id_=e))
            else:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
    if 'item' in req_data:
        item = req_data['item']
        for i in item:
            try:
                out.extend(Api.get_entities_by_menu_item(code_=i))
            except Exception:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404c")
    if 'class_code' in req_data:
        class_code = req_data['class_code']
        for c in class_code:
            if len(Api.get_entities_by_class(class_code_=c)) == 0:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404d")
            out.extend(Api.get_entities_by_class(class_code_=c))
    if 'latest' in req_data:
        latest = req_data['latest'][0]
        if type(latest) is int:
            if 0 < latest < 101:
                print(latest)
                out.extend(Api.get_entities_get_latest(limit_=latest))
            else:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404e")
        else:
            raise APIError('Syntax is incorrect!', status_code=404, payload="404")

    return jsonify(out)


@app.route('/api/0.1/code/<code>')
@api_access()  # type: ignore
def api_get_by_menu_item(code: str) -> Response:
    try:
        Api.get_entities_by_menu_item(code_=code)
        return jsonify(Api.get_entities_by_menu_item(code_=code))
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404c")


@app.route('/api/0.1/class/<class_code>')
@api_access()  # type: ignore
def api_get_by_class(class_code: str) -> Response:
    if len(Api.get_entities_by_class(class_code_=class_code)) == 0:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404d")
    return jsonify(Api.get_entities_by_class(class_code_=class_code))


@app.route('/api/0.1/latest/<int:limit>')
@api_access()  # type: ignore
def api_get_latest(limit: int) -> Response:
    if 0 < limit < 100:
        return jsonify(Api.get_entities_get_latest(limit_=limit))
    raise APIError('Syntax is incorrect!', status_code=404, payload="404e")


@app.route('/api/0.1/query')
@api_access()  # type: ignore
def api_get_query() -> Response:
    if request.args:
        out = []
        if request.args.getlist('entities[]'):
            entities = request.args.getlist('entities[]')
            for e in entities:
                try:
                    int(e)
                except Exception:
                    raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
                out.append(Api.get_entity(id_=e))
        if request.args.getlist('items[]'):
            items = request.args.getlist('items[]')
            for i in items:
                try:
                    out.extend(Api.get_entities_by_menu_item(code_=i))
                except Exception:
                    raise APIError('Syntax is incorrect!', status_code=404, payload="404c")
        if request.args.getlist('classes[]'):
            classes = request.args.getlist('classes[]')
            for c in classes:
                if len(Api.get_entities_by_class(class_code_=c)) == 0:
                    raise APIError('Syntax is incorrect!', status_code=404, payload="404d")
                out.extend(Api.get_entities_by_class(class_code_=c))
        return jsonify(out)
    else:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404")


@app.route('/api/0.1/test')
@api_access()  # type: ignore
def api_get_test() -> Response:
    return jsonify(Pagination.get_pagination())


@app.route('/api')
@api_access()  # type: ignore
def api_index() -> str:
    return render_template('api/index.html')
