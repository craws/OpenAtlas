from datetime import UTC, datetime
from typing import Any, NoReturn
from uuid import UUID

import psycopg2
from flask import Response, abort, jsonify, make_response, request
from flask_openapi3 import APIBlueprint
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
        'timestamp': datetime.now(UTC).isoformat(),
        'status': status}
    return make_response(jsonify(error_payload), status)


def abort_with_error(
        status: int,
        title: str,
        message: str,
        details: dict[str, Any] | None = None) -> NoReturn:
    abort(error_response(status, title, message, details))


def handle_db_error(_e: Any = None) -> Response:
    return error_response(  # pragma: no cover
        500,
        'Internal Server Error',
        'An unexpected database error occurred.',
        {'hint': 'Please try again later or contact the project members.'})


def handle_db_data_error(_e: Any = None) -> Response:
    return error_response(  # pragma: no cover
        400,
        'Bad Request',
        'Invalid value in request parameters, e.g. a date '
        'out of range or with an invalid format.',
        {'hint': 'Check the request parameters in the API documentation.'})


def handle_http_exception(e: HTTPException) -> Response:
    return error_response(  # pragma: no cover
        e.code or 500,
        e.name,
        e.description or 'An HTTP error occurred.')


def register_error_handlers(api_v1: APIBlueprint) -> None:
    api_v1.register_error_handler(psycopg2.DataError, handle_db_data_error)
    api_v1.register_error_handler(psycopg2.Error, handle_db_error)
    api_v1.register_error_handler(HTTPException, handle_http_exception)


def abort_not_found(identifier: UUID | str | int) -> NoReturn:
    details = {
        'provided_id': str(identifier),
        'hint': 'Check if the UUID or ID is correct '
                'and the entity has not been deleted.'}
    abort_with_error(
        404,
        'Entity does not exist',
        'The requested entity could not be found in the database.',
        details)


def abort_id_not_a_file(id_: int) -> NoReturn:
    details = {
        'provided_id': str(id_),
        'hint': 'Find more details about this entity via an /entity endpoint.'}
    abort_with_error(
        404,
        'Entity is not a file',
        f'The requested entity ID {id_} exists, '
        'but is not a file entity.',
        details)


def abort_file_without_license(id_: int) -> NoReturn:
    details = {
        'provided_id': str(id_),
        'hint': 'Please contact the project members for more details.'}
    abort_with_error(
        403,
        'No license',
        'The requested file has no open license and cannot be displayed.',
        details)


def abort_file_not_public(id_: int) -> NoReturn:
    details = {
        'provided_id': str(id_),
        'hint': 'Please contact the project members for more details.'}
    abort_with_error(
        403,
        'Not publicly shareable',
        'This file is not marked as publicly shareable.',
        details)


def abort_file_not_found(id_: int) -> NoReturn:
    details = {
        'provided_id': str(id_),
        'hint': 'The entity metadata exists, '
                'but the physical file is missing. '
                'See /entity endpoint for metadata.'}
    abort_with_error(
        404,
        'File not found on disk',
        f'No physical file was found for the requested ID {id_}.',
        details)
