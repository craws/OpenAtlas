import datetime
from typing import Any

from flask import jsonify, render_template, request, g

from openatlas import app
from openatlas.api.resources.error import (
    AccessDeniedError, NoLicenseError, EntityDoesNotExistError, OperatorError,
    LogicalOperatorError, SearchValueError, InvalidCidocClassCodeError,
    InvalidSystemClassError, InvalidViewClassError, InvalidLimitError,
    InvalidSearchSyntax, ValueNotIntegerError, NoSearchStringError,
    NotAPlaceError, QueryEmptyError, NotATypeError, LastEntityError,
    DisplayFileNotFoundError)


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
            'title': 'Endpoint not found',
            'message':
                'The requested endpoint does not exist. '
                'Please consult the manual or the Swagger documentation: '
                f'{request.url_root}swagger',
            'url': request.url,
            'timestamp': datetime.datetime.now(),
            'status': 404}), 404
    if request.path.startswith('/static'):
        return jsonify({
            'title': 'Site not found',
            'message': 'The site does not exist.',
            'url': request.url,
            'timestamp': datetime.datetime.now(),
            'status': 404}), 404
    return render_template(
        'error/404.html',
        crumbs=['404 - File not found'],
        e=e), 404


@app.errorhandler(418)
def invalid_id(e: Exception) -> tuple[str, int]:
    return render_template(
        'error/418.html',
        crumbs=['418 - I’m a teapot'],
        e=e), 418


@app.errorhandler(422)
def unprocessable_entity(e: Exception) -> tuple[str, int]:
    return render_template(
        'error/422.html',
        crumbs=['422 - Unprocessable entity'],
        e=e), 422


@app.errorhandler(AccessDeniedError)
def access_denied(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Access denied',
        'message': 'You do not have access to the API. '
                   'Please ask the data provider for permission.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 403}), 403


@app.errorhandler(DisplayFileNotFoundError)
def file_not_found(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'File not found',
        'message': 'No file was found for the requested ID.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 404}), 404


@app.errorhandler(EntityDoesNotExistError)
def entity_does_not_exist(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Entity does not exist',
        'message': 'The requested entity does not exist in the database.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 404}), 404


@app.errorhandler(InvalidCidocClassCodeError)
def invalid_cidoc_class_code(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Invalid cidoc_classes value',
        'message':
            'The CIDOC class value is invalid, use "all" or '
            + str(list(g.cidoc_classes)),
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(InvalidLimitError)
def invalid_limit(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Invalid limit value',
        'message':
            'Only integers between 1 and 100 are allowed for the limit.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(InvalidSearchSyntax)
def invalid_search_syntax(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Invalid search syntax',
        'message':
            'The search request contains major errors. '
            'Please confer the manual.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(InvalidSystemClassError)
def invalid_system_class(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Invalid system_classes value',
        'message':
            'The system_classes value is invalid, use "all" or '
            + str(list(g.classes)),
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(InvalidViewClassError)
def invalid_view_class(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Invalid view_classes value',
        'message':
            'The view_classes value is invalid, use "all" or '
            + str(list(g.view_class_mapping)),
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(LastEntityError)
def last_entity_error(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'ID is last entity',
        'message':
            'The requested ID is the last entity, please choose another ID.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(LogicalOperatorError)
def invalid_logical_operator(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Invalid logical operator',
        'message':
            'The logical operator is invalid. Please use: '
            f'{app.config["LOGICAL_OPERATOR"]}',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(NoLicenseError)
def no_license(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'No license',
        'message':
            'The requested file has no license and cannot be displayed.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 409}), 409


@app.errorhandler(NoSearchStringError)
def no_search_string(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'No search values',
        'message': 'Search values are empty.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(NotATypeError)
def not_a_type(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Entity is not a type',
        'message': 'Requested ID either does not exist or is not a Type.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(NotAPlaceError)
def not_a_place(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'ID is not a valid place',
        'message': 'This endpoint requires a valid ID of a place entity.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(OperatorError)
def invalid_operator(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Invalid compare operator',
        'message':
            'The compare operator is invalid. '
            f'Please use: {app.config["COMPARE_OPERATORS"]}',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(QueryEmptyError)
def empty_query(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'No query parameters given',
        'message':
            'The /query endpoint requires at least one of the following '
            'parameters: entities, cidoc_classes, view_classes, '
            'system_classes.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(SearchValueError)
def invalid_search_category(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Invalid search category',
        'message':
            'The search category is invalid. Please use: '
            f'{app.config["VALID_VALUES"]}',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400


@app.errorhandler(ValueNotIntegerError)
def value_not_an_integer(_e: Exception) -> tuple[Any, int]:
    return jsonify({
        'title': 'Invalid search value',
        'message':
            'The search values need to be an integer for the chosen category.',
        'url': request.url,
        'timestamp': datetime.datetime.now(),
        'status': 400}), 400
