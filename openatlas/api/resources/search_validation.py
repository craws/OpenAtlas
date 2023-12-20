from typing import Any, Union

from openatlas.api.resources.error import (
    SearchCategoriesError, LogicalOperatorError, OperatorError,
    NoSearchStringError, ValueNotIntegerError)

from openatlas import app


def iterate_validation(parameters: list[dict[str, Any]]) -> list[list[bool]]:
    return [[call_validation(search_key, values) for values in value_list]
            for parameter in parameters
            for search_key, value_list in parameter.items()]


def call_validation(search_key: str, values: dict[str, Any]) -> bool:
    return parameter_validation(
        categories=search_key,
        operator_=values['operator'],
        search_values=values["values"],
        logical_operator=values[
            'logicalOperator'] if 'logicalOperator' in values else 'or')


def parameter_validation(
        categories: Any,
        operator_: str,
        search_values: list[Any],
        logical_operator: str) -> bool:
    if logical_operator not in app.config['LOGICAL_OPERATOR']:
        raise LogicalOperatorError
    if categories not in app.config['VALID_CATEGORIES']:
        raise SearchCategoriesError
    if operator_ not in app.config['COMPARE_OPERATORS']:
        raise OperatorError
    if not search_values:
        raise NoSearchStringError
    if categories in app.config['INT_CATEGORIES']:
        if not bool(any(isinstance(value, int) for value in search_values)):
            raise ValueNotIntegerError
    return True


def check_if_date_search(k: str) -> bool:
    return bool(k in ["beginFrom", "beginTo", "endFrom", "endTo"])


def check_if_date(value: str) -> Union[str, bool]:
    return False if value == "None" else value
