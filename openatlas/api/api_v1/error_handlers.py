from datetime import datetime
from typing import Any, NoReturn
from uuid import UUID

import psycopg2
from flask import Response, abort, jsonify, make_response, request
from werkzeug.exceptions import HTTPException


def error_response(
        status: int,
        title: str,
        message: str,
        details: dict[str, Any] | None = None) -> Response:
    error_payload = {
        'title': title,
        'message': message,
        'details': details or {},
        'url': request.url,
        'timestamp': datetime.now().isoformat(),
        'status': status}
    return make_response(jsonify(error_payload), status)


def abort_with_error(
        status: int,
        title: str,
        message: str,
        details: dict[str, Any] | None = None) -> NoReturn:
    abort(error_response(status, title, message, details))


def handle_db_error(_e: Any = None) -> Response:
    return error_response(
        500,
        'Internal Server Error',
        'Unexpected database error occurred',
        {'hint': 'Please try again later or contact the project members.'})


def handle_db_data_error(_e: Any = None) -> Response:
    return error_response(
        400,
        'Bad Request',
        'Invalid value in request parameters, e.g. a date '
        'out of range or with an invalid format.',
        {'hint': 'Check the request parameters in the API documentation.'})


def handle_http_exception(e: HTTPException) -> Response:
    return error_response(e.code, e.name, e.description)


def handle_file_not_found_exception(e: HTTPException) -> Response:
    return error_response(e.code, e.name, e.description)


def register_error_handlers(api_v1) -> None:
    api_v1.register_error_handler(psycopg2.DataError, handle_db_data_error)
    api_v1.register_error_handler(psycopg2.Error, handle_db_error)
    api_v1.register_error_handler(HTTPException, handle_http_exception)


def abort_not_found(uuid: UUID | str | int) -> NoReturn:
    details = {
        'provided_uuid': str(uuid),
        'hint': 'Check if the UUID is correct '
                'and the entity has not been deleted.'}
    abort_with_error(
        404,
        'Entity does not exist',
        'The requested entity could not be found in the database.',
        details)


def abort_invalid_class(class_name: str) -> NoReturn:
    details = {
        'provided_class': str(class_name),
        'hint': 'Check if the class name is spelled '
                'correctly and exists in the system.'}
    abort_with_error(
        404,
        'Invalid system class',
        f"The requested entity class '{class_name}' "
        f"is not a valid system class.",
        details)


def abort_id_not_a_file(id_: int) -> NoReturn:
    details = {
        'provided_id': str(id_),
        'hint': 'Find more details of that entity via an /entity endpoint'}
    abort_with_error(
        404,
        'ID is not a file',
        f"The requested entity id {id_} is not a file. ",
        details)


def abort_id_does_not_exist(id_: int) -> NoReturn:
    details = {
        'provided_id': str(id_),
        'hint': 'Try searching for the entity by its name using a '
                'search endpoint.'}
    abort_with_error(
        404,
        'ID does not exist',
        f"The requested entity id {id_} is not in the database.",
        details)


def abort_file_without_license(id_: int) -> NoReturn:
    details = {
        'provided_id': str(id_),
        'hint': 'Please contact the project members for more details.'}
    abort_with_error(
        403,
        'No Licenser',
        "The requested file has no license and can't be displayed.",
        details)


def abort_file_not_public(id_: int) -> NoReturn:
    details = {
        'provided_id': str(id_),
        'hint': 'Please contact the project members for more details.'}
    abort_with_error(
        403,
        'Not shareable',
        "This file is not public shareable.",
        details)


def abort_file_not_found(id_: int) -> NoReturn:
    details = {
        'provided_id': str(id_),
        'hint': 'Find more details of that entity via an /entity endpoint'}
    abort_with_error(
        404,
        'File not found',
        f"No file was found for the requested ID {id_}.",
        details)

