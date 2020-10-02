from flask import json, jsonify, render_template, request
from flask_cors import cross_origin
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.api.api import Api
from openatlas.api.error import APIError
from openatlas.api.model import Model
from openatlas.api.node import APINode
from openatlas.api.validation import Validation
from openatlas.util.util import api_access


# Todo: unit test -> remove # pragma: nocover
# Todo: prevent code duplication


@app.route('/api/0.1/entity/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_entity(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    try:
        int(id_)
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
    if validation['download']:
        return Response(json.dumps(Api.get_entity(id_=id_, meta=validation)), mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})
    return jsonify(Api.get_entity(id_=id_, meta=validation))


@app.route('/api/0.1/entity/download/<int:id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_download_entity(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    return Response(json.dumps(Api.get_entity(id_=id_, meta=validation)),
                    mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})


@app.route('/api/0.1/code/<code>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_by_menu_item(code: str) -> Response:
    validation = Validation.validate_url_query(request.args)
    try:
        if validation['count']:
            return jsonify(len(Model.get_entities_by_menu_item(code_=code, validation=validation)))
        if validation['download']:
            return Response(json.dumps(
                Model.pagination(Model.get_entities_by_menu_item(code_=code, validation=validation),
                                 validation=validation)), mimetype='application/json',
                headers={'Content-Disposition': 'attachment;filename=' + str(code) + '.json'})
        return jsonify(
            Model.pagination(Model.get_entities_by_menu_item(code_=code, validation=validation),
                             validation=validation))
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404c")


@app.route('/api/0.1/class/<class_code>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_by_class(class_code: str) -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['count']:
        return jsonify(
            len(Model.get_entities_by_class(class_code=class_code, validation=validation)))
    if validation['download']:
        return Response(json.dumps(
            Model.pagination(
                Model.get_entities_by_class(class_code=class_code, validation=validation),
                validation=validation)), mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=' + str(class_code) + '.json'})
    return jsonify(
        Model.pagination(Model.get_entities_by_class(class_code=class_code, validation=validation),
                         validation=validation))


@app.route('/api/0.1/latest/<int:limit>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_latest(limit: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    if 0 < limit < 100:
        if validation['download']:
            return Response(json.dumps(
                Model.get_entities_get_latest(limit_=limit, validation=validation)),
                mimetype='application/json',
                headers={
                    'Content-Disposition': 'attachment;filename=latest_' + str(limit) + '.json'})
        return jsonify(Model.get_entities_get_latest(limit_=limit, validation=validation))
    raise APIError('Syntax is incorrect!', status_code=404, payload="404e")


@app.route('/api/0.1/query', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_query() -> Response:  # pragma: nocover
    validation = Validation.validate_url_query(request.args)
    if request.args:
        out = []
        count = 0
        if request.args.getlist('entities'):
            entities = request.args.getlist('entities')
            for e in entities:
                try:
                    out.append(int(e))
                except Exception:
                    raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
            count += len(out)
        if request.args.getlist('items'):
            items = request.args.getlist('items')
            for i in items:
                try:
                    if validation['count']:
                        count += len(
                            Model.get_entities_by_menu_item(code_=i, validation=validation))
                    else:
                        out.extend(Model.get_entities_by_menu_item(code_=i, validation=validation))
                except Exception:
                    raise APIError('Syntax is incorrect!', status_code=404, payload="404c")
        if request.args.getlist('classes'):
            classes = request.args.getlist('classes')
            for class_code in classes:
                if validation['count']:
                    count += len(
                        Model.get_entities_by_class(class_code=class_code, validation=validation))
                else:
                    out.extend(
                        Model.get_entities_by_class(class_code=class_code, validation=validation))

        if validation['count']:
            return jsonify(count)
        if validation['download']:
            return Response(json.dumps(out), mimetype='application/json',
                            headers={'Content-Disposition': 'attachment;filename=query.json'})
        return jsonify(Model.pagination(out, validation=validation))
    else:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404")


@app.route('/api/0.1/node_entities/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_node_entities(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    try:
        id_ = int(id_)
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
    if validation['count']:
        return jsonify(len(APINode.get_node(id_)))
    if validation['download']:
        return Response(json.dumps(APINode.get_node(id_)), mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=node_entities_' + str(
                                id_) + '.json'})
    return jsonify(APINode.get_node(id_))


@app.route('/api/0.1/node_entities_all/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_node_entities_all(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    try:
        id_ = int(id_)
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
    if validation['count']:
        return jsonify(len(APINode.get_node_all(id_)))
    if validation['download']:
        return Response(json.dumps(APINode.get_node_all(id_)), mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=node_entities_all_' + str(
                                id_) + '.json'})
    return jsonify(APINode.get_node_all(id_))


@app.route('/api/0.1/subunit/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_subunit(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    try:
        id_ = int(id_)
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
    if validation['count']:
        return jsonify(len(APINode.get_subunits(id_)))
    if validation['download']:
        return Response(json.dumps(APINode.get_subunits(id_)), mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=subunit_' + str(
                                id_) + '.json'})
    return jsonify(APINode.get_subunits(id_))


@app.route('/api/0.1/subunit_hierarchy/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_subunit_hierarchy(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    try:
        id_ = int(id_)
    except Exception:
        raise APIError('Syntax is incorrect!', status_code=404, payload="404b")
    if validation['count']:
        return jsonify(len(APINode.get_subunit_hierarchy(id_)))
    if validation['download']:
        return Response(json.dumps(APINode.get_subunit_hierarchy(id_)), mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=subunit_hierarchy_' + str(
                                id_) + '.json'})
    return jsonify(APINode.get_subunit_hierarchy(id_))


@app.route('/api', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_index() -> str:
    return render_template('api/index.html')


# Deprecated
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
            result = Model.pagination(ids, validation=validation)
            out.append({'entities': result})
    if 'item' in req_data:
        item = req_data['item']
        for i in item:
            try:
                out.append({'result': Model.pagination(
                    Model.get_entities_by_menu_item(code_=i, validation=validation),
                    validation=validation),
                    'code': i})
            except Exception:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404c")
    if 'class_code' in req_data:
        classes = req_data['class_code']
        for class_code in classes:
            if len(Model.get_entities_by_class(class_code=class_code, validation=validation)) == 0:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404d")
            out.append({'result': Model.pagination(
                Model.get_entities_by_class(class_code=class_code, validation=validation),
                validation=validation), 'class': class_code})
    if 'latest' in req_data:
        latest = req_data['latest'][0]
        if type(latest) is int:
            if 0 < latest < 101:
                out.extend(Model.get_entities_get_latest(limit_=latest, validation=validation))
            else:
                raise APIError('Syntax is incorrect!', status_code=404, payload="404e")
        else:
            raise APIError('Syntax is incorrect!', status_code=404, payload="404")

    return jsonify(out)
