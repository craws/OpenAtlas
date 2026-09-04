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


def handle_file_not_found_exception(e):
    return jsonify({
        "status": e.code,
        "title": e.name,
        "message": e.description
    }), e.code


def register_error_handlers(api_v1) -> None:
    api_v1.register_error_handler(psycopg2.Error, handle_db_error)
    api_v1.register_error_handler(HTTPException, handle_http_exception)


def abort_not_found(uuid: UUID | str | int) -> NoReturn:
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
        'message': f"The requested entity class '{class_name}' "
                   f"is not a valid system class.",
        'details': {
            'provided_class': str(class_name),
            'hint': 'Check if the class name is spelled '
                    'correctly and exists in the system.'},
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': 404}
    abort(make_response(jsonify(error_payload), 404))


def abort_id_not_a_file(id_: int) -> NoReturn:
    error_payload = {
        'title': 'ID is not a file',
        'message': f"The requested entity id {id_} is not a file. ",
        'details': {
            'provided_id': str(id_),
            'hint': ''}, # Todo
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': 404}
    abort(make_response(jsonify(error_payload), 404))

def abort_id_does_not_exist(id_: int) -> NoReturn:
    error_payload = {
        'title': 'ID does not exist',
        'message': f"The requested entity id {id_} is not in the database.",
        'details': {
            'provided_id': str(id_),
            'hint': ''}, # Todo
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': 404}
    abort(make_response(jsonify(error_payload), 404))


def abort_file_without_license(id_: int) -> NoReturn:
    error_payload = {
        'title': 'No Licenser',
        'message': "The requested file has no license and can't be displayed.",
        'details': {
            'provided_id': str(id_),
            'hint': ''}, # Todo
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': 403}
    abort(make_response(jsonify(error_payload), 403))


def abort_file_not_public(id_: int) -> NoReturn:
    error_payload = {
        'title': 'Not shareable',
        'message': "This file is not public shareable.",
        'details': {
            'provided_id': str(id_),
            'hint': ''}, # Todo
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': 403}
    abort(make_response(jsonify(error_payload), 403))

def abort_file_not_found(id_: int) -> NoReturn:
    error_payload = {
        'title': 'File not found',
        'message': f"No file was found for the requested ID {id_}.",
        'details': {
            'provided_id': str(id_),
            'hint': ''}, # Todo
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': 404}
    abort(make_response(jsonify(error_payload), 404))


def abort_unsupported_iiif_version(version: str) -> NoReturn:
    error_payload = {
        'title': 'Unsupported IIIF version',
        'message': f"The requested IIIF version '{version}' is not supported.",
        'details': {
            'provided_version': str(version),
            'hint': 'Only IIIF versions 2 and 3 are supported.'},
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': 400}
    abort(make_response(jsonify(error_payload), 400))
