from flask import json, jsonify, render_template, request
from flask_cors import cross_origin
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.models.api import Api
from openatlas.models.api_helpers.api_error import APIError
from openatlas.models.api_helpers.api_validation import Validation
from openatlas.util.util import api_access


# Todo: unit test


@app.route('/api/0.1/entity/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_entity(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    try:
        int(id_)
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
    return jsonify(Api.get_entity(id_=id_, meta=validation))


@app.route('/api/0.1/entity/download/<int:id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_download_entity(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    return Response(json.dumps(Api.get_entity(id_=id_, meta=validation)),
                    mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})


@app.route('/api/0.1/', methods=['GET', 'POST', 'VIEW', 'PUT'], strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET', 'POST', 'VIEW', 'PUT'])
def api_get_entities_by_json() -> Response:  # pragma: nocover
    validation = Validation.validate_url_query(request.args)
    out = []
    req_data = request.get_json()
    if 'id' in req_data:
        entity = req_data['id']
        ids = []
        for e in entity:
            try:
                ids.append(int(e))
            except Exception:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
            result = Api.pagination(ids, meta=validation)
            out.append({'entities': result})
    if 'item' in req_data:
        item = req_data['item']
        for i in item:
            try:
                out.append({'result': Api.pagination(
                    Api.get_entities_by_menu_item(code_=i, meta=validation), meta=validation),
                    'code': i})
            except Exception:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404c")
    if 'class_code' in req_data:
        classes = req_data['class_code']
        for class_code in classes:
            if len(Api.get_entities_by_class(class_code_=class_code, meta=validation)) == 0:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404d")
            out.append({'result': Api.pagination(
                Api.get_entities_by_class(class_code_=class_code, meta=validation),
                meta=validation), 'class': class_code})
    if 'latest' in req_data:
        latest = req_data['latest'][0]
        if type(latest) is int:
            if 0 < latest < 101:
                out.extend(Api.get_entities_get_latest(limit_=latest, meta=validation))
            else:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404e")
        else:
            raise APIError('Syntax is incorrect!', status_code=404, payload="404")

    return jsonify(out)


@app.route('/api/0.1/code/<code>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_by_menu_item(code: str) -> Response:
    validation = Validation.validate_url_query(request.args)
    try:
        Api.get_entities_by_menu_item(code_=code, meta=validation)
        return jsonify(Api.pagination(Api.get_entities_by_menu_item(code_=code, meta=validation),
                                      meta=validation))
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404c")


@app.route('/api/0.1/class/<class_code>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_by_class(class_code: str) -> Response:
    validation = Validation.validate_url_query(request.args)
    if len(Api.get_entities_by_class(class_code_=class_code, meta=validation)) == 0:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404d")
    return jsonify(
        Api.pagination(Api.get_entities_by_class(class_code_=class_code, meta=validation),
                       meta=validation))


@app.route('/api/0.1/latest/<int:limit>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_latest(limit: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    if 0 < limit < 100:
        return jsonify(Api.get_entities_get_latest(limit_=limit, meta=validation))
    raise APIError('Syntax is incorrect!', status_code=404, payload="404e")


@app.route('/api/0.1/query', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_query() -> Response:  # pragma: nocover
    validation = Validation.validate_url_query(request.args)
    if request.args:
        out = []
        if request.args.getlist('entities[]'):
            entities = request.args.getlist('entities[]')
            ids = []
            for e in entities:
                try:
                    ids.append(int(e))
                except Exception:
                    raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
            result = Api.pagination(ids, meta=validation)
            out.append({'entities': result})
        if request.args.getlist('items[]'):
            items = request.args.getlist('items[]')
            for i in items:
                try:
                    out.append({'result': Api.pagination(
                        Api.get_entities_by_menu_item(code_=i, meta=validation), meta=validation),
                                'code': i})
                except Exception:
                    raise APIError('Syntax is incorrect!', status_code=404, payload="404c")
        if request.args.getlist('classes[]'):
            classes = request.args.getlist('classes[]')
            for class_code in classes:
                if len(Api.get_entities_by_class(class_code_=class_code, meta=validation)) == 0:
                    raise APIError('Syntax is incorrect!', status_code=404, payload="404d")
                out.append({'result': Api.pagination(
                    Api.get_entities_by_class(class_code_=class_code, meta=validation),
                    meta=validation), 'class': class_code})
        return jsonify(out)
    else:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404")


@app.route('/api', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_index() -> str:
    return render_template('api/index.html')
