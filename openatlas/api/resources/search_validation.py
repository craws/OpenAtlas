import ast
from typing import Any

from openatlas import app
from openatlas.api.resources.error import (
    InvalidSearchSyntax, LogicalOperatorError, NoSearchStringError,
    OperatorError,
    SearchCategoriesError, ValueNotIntegerError)


def iterate_validation(param: list[str]) -> list[list[bool]]:
    try:
        parameters = [ast.literal_eval(item) for item in param]
    except Exception as e:
        raise InvalidSearchSyntax from e
    for parameter in parameters:
        for search_key, value_list in parameter.items():
            for values in value_list:
                parameter_validation(
                    search_key,
                    values['operator'],
                    values["values"],
                    values.get('logicalOperator') or 'or')
    return parameters


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


def check_if_date(value: str) -> str | bool:
    return False if value == "None" else value
