from typing import Any

from flask import json, jsonify, render_template, request, send_file, send_from_directory
from flask_cors import cross_origin
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.api.api import Api
from openatlas.api.error import APIError
from openatlas.api.node import APINode
from openatlas.api.parameter import Validation
from openatlas.api.path import Path
from openatlas.models.entity import Entity
from openatlas.models.node import Node
from openatlas.util.util import api_access


@app.route('/api/0.1/entity/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_entity(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['download']:
        return Response(json.dumps(Api.get_entity(Api.get_entity_by_id(id_=id_), meta=validation)),
                        mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})
    return jsonify(Api.get_entity(Api.get_entity_by_id(id_=id_), meta=validation))


@app.route('/api/0.1/entity/download/<int:id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_download_entity(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    return Response(json.dumps(Api.get_entity(Api.get_entity_by_id(id_=id_), meta=validation)),
                    mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=' + str(id_) + '.json'})


@app.route('/api/0.1/code/<code>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_by_menu_item(code: str) -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['count']:
        return jsonify(len(Path.get_entities_by_menu_item(code_=code, validation=validation)))
    if validation['download']:
        return Response(json.dumps(
            Path.pagination(
                Path.get_entities_by_menu_item(code_=code, validation=validation),
                validation=validation)),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=' + str(code) + '.json'})
    return jsonify(
        Path.pagination(Path.get_entities_by_menu_item(code_=code, validation=validation),
                        validation=validation))


@app.route('/api/0.1/class/<class_code>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_by_class(class_code: str) -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['count']:
        return jsonify(
            len(Path.get_entities_by_class(class_code=class_code, validation=validation)))
    if validation['download']:
        return Response(json.dumps(
            Path.pagination(
                Path.get_entities_by_class(class_code=class_code, validation=validation),
                validation=validation)),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=' + str(class_code) + '.json'})
    return jsonify(
        Path.pagination(Path.get_entities_by_class(class_code=class_code, validation=validation),
                        validation=validation))


@app.route('/api/0.1/latest/<limit>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_latest(limit: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['download']:
        return Response(json.dumps(
            Path.get_entities_get_latest(limit_=limit, validation=validation)),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=latest_' + str(limit) + '.json'})
    return jsonify(Path.get_entities_get_latest(limit_=limit, validation=validation))


@app.route('/api/0.1/query', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_get_query() -> Response:
    validation = Validation.validate_url_query(request.args)
    if request.args:
        out = []
        count = 0
        if request.args.getlist('entities'):
            entities = request.args.getlist('entities')
            for e in entities:
                out.append(Api.get_entity_by_id(e))
            count += len(out)
        if request.args.getlist('items'):
            items = request.args.getlist('items')
            for i in items:
                if validation['count']:
                    count += len(
                        Path.get_entities_by_menu_item(code_=i, validation=validation))
                else:
                    out.extend(Path.get_entities_by_menu_item(code_=i, validation=validation))
        if request.args.getlist('classes'):
            classes = request.args.getlist('classes')
            for class_code in classes:
                if validation['count']:
                    count += len(
                        Path.get_entities_by_class(class_code=class_code, validation=validation))
                else:
                    out.extend(Path.get_entities_by_class(class_code=class_code, validation=validation))
        if validation['count']:
            return jsonify(count)
        if validation['download']:
            return Response(json.dumps(Path.pagination(out, validation=validation)),
                            mimetype='application/json',
                            headers={'Content-Disposition': 'attachment;filename=query.json'})
        return jsonify(Path.pagination(out, validation=validation))
    else:
        raise APIError('Not input given.', status_code=404, payload="404h")


@app.route('/api/0.1/node_entities/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_node_entities(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['count']:
        return jsonify(len(APINode.get_node(id_)))
    if validation['download']:
        return Response(json.dumps(APINode.get_node(id_)),
                        mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=node_entities_' + str(
                                id_) + '.json'})
    return jsonify(APINode.get_node(id_))


@app.route('/api/0.1/node_entities_all/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_node_entities_all(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['count']:
        return jsonify(len(APINode.get_node_all(id_)))
    if validation['download']:
        return Response(json.dumps(APINode.get_node_all(id_)),
                        mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=node_entities_all_' + str(
                                id_) + '.json'})
    return jsonify(APINode.get_node_all(id_))


@app.route('/api/0.1/subunit/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_subunit(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['count']:
        return jsonify(len(APINode.get_subunits(id_)))
    if validation['download']:
        return Response(json.dumps(APINode.get_subunits(id_)),
                        mimetype='application/json',
                        headers={'Content-Disposition': 'attachment;filename=subunit_' + str(id_)
                                                        + '.json'})
    return jsonify(APINode.get_subunits(id_))


@app.route('/api/0.1/subunit_hierarchy/<id_>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_subunit_hierarchy(id_: int) -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['count']:
        return jsonify(len(APINode.get_subunit_hierarchy(id_)))
    if validation['download']:
        return Response(json.dumps(APINode.get_subunit_hierarchy(id_)),
                        mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=subunit_hierarchy_' + str(
                                id_) + '.json'})
    return jsonify(APINode.get_subunit_hierarchy(id_))


@app.route('/api/display/<path:filename>', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def display_file_api(filename: str) -> Any:  # pragma: no cover
    validation = Validation.validate_url_query(request.args)
    from pathlib import Path as Pathlib_path
    entity = Entity.get_by_id(int(Pathlib_path(filename).stem), nodes=True)
    license_ = None
    # If img has no license, it will not displayed
    for node in entity.nodes:
        if node.root and node.root[-1] == Node.get_hierarchy('License').id:
            license_ = node.name
    if license_:
        if validation['download']:
            return send_file(str(app.config['UPLOAD_DIR']) + '/' + filename, as_attachment=True)
        return send_from_directory(app.config['UPLOAD_DIR'], filename)
    raise APIError('Access denied.', status_code=403, payload="403")


@app.route('/api/0.1/content/', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_content() -> Response:
    validation = Validation.validate_url_query(request.args)
    if validation['download']:
        return Response(json.dumps(Path.get_content(validation=validation)),
                        mimetype='application/json',
                        headers={'Content-Disposition': 'attachment;filename=content.json'})
    return jsonify(Path.get_content(validation=validation))


@app.route('/api', strict_slashes=False)
@api_access()  # type: ignore
@cross_origin(origins=app.config['CORS_ALLOWANCE'], methods=['GET'])
def api_index() -> str:
    return render_template('api/index.html')
