from datetime import datetime
from typing import NoReturn
from uuid import UUID

from flask import abort, jsonify, make_response, request
from werkzeug.exceptions import HTTPException
import psycopg2

def handle_db_error():
    return jsonify({
        "status": 500,
        "title": "Internal Server Error",
        "message": "Unsuspected database error occurred."
    }), 500


def handle_http_exception(e):
    return jsonify({
        "status": e.code,
        "title": e.name,
        "message": e.description
    }), e.code


def register_error_handlers(api_v1) -> None:
    api_v1.register_error_handler(psycopg2.Error, handle_db_error)
    api_v1.register_error_handler(HTTPException, handle_http_exception)


def abort_not_found(uuid: UUID | str) -> NoReturn:
    error_payload = {
        'title': 'Entity does not exist',
        'message': 'The requested entity could not be found in the database.',
        'details': {
            'provided_uuid': str(uuid),
            'hint': 'Check if the UUID is correct '
                    'and the entity has not been deleted.'},
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': 404}
    abort(make_response(jsonify(error_payload), 404))


def abort_invalid_class(class_name: str) -> NoReturn:
    error_payload = {
        'title': 'Invalid system class',
        'message': f"The requested entity class '{class_name}' is not a valid system class.",
        'details': {
            'provided_class': str(class_name),
            'hint': 'Check if the class name is spelled correctly and exists in the system.'},
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': 404}
    abort(make_response(jsonify(error_payload), 404))
