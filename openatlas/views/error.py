import datetime
from typing import Any

from flask import jsonify, render_template, request

from openatlas import app, AccessDeniedError, NoLicenseError


@app.errorhandler(400)
def bad_request(e: Exception) -> tuple[str, int]:
    return render_template(  # pragma: no cover
        'error/400.html',
        crumbs=['400 - Bad Request'],
        e=e), 400


@app.errorhandler(403)
def forbidden(e: Exception) -> tuple[str, int]:
    return render_template(
        'error/403.html',
        crumbs=['403 - Forbidden'],
        e=e), 403


@app.errorhandler(404)
def page_not_found(e: Exception) -> tuple[Any, int]:
    if request.path.startswith('/api/'):
        return jsonify({
            'message': 'Endpoint not found',
            "url": request.url,
            "timestamp": datetime.datetime.now(),
            'status': 404}), 404
    return render_template(
        'error/404.html',
        crumbs=['404 - File not found'],
        e=e), 404


@app.errorhandler(418)
def invalid_id(e: Exception) -> tuple[str, int]:
    return render_template(
        'error/418.html',
        crumbs=["418 - I’m a teapot"],
        e=e), 418


@app.errorhandler(422)
def unprocessable_entity(e: Exception) -> tuple[str, int]:
    return render_template(
        'error/422.html',
        crumbs=['422 - Unprocessable entity'],
        e=e), 422


@app.errorhandler(Exception)
def internal_server_error(e):
    return jsonify({'msg': 'General Error'}), 500


@app.errorhandler(AccessDeniedError)
def access_denied_error(e):
    return jsonify({
        "title": "Access Denied",
        "message": "You do not have access to the API. "
                   "Please ask the data provider for permission.",
        "timestamp": datetime.datetime.now(),
        "status": 403}), 403


@app.errorhandler(NoLicenseError)
def no_license_error(e):
    return jsonify({
        "title": "Access Denied",
        "message": "You do not have access to the API. "
                   "Please ask the data provider for permission.",
        "timestamp": datetime.datetime.now(),
        "status": 409}), 409

# @app.errorhandler(500)
# def internal_server_error_500(e):
#     return jsonify({'msg': 'Internal server error'}), 500
