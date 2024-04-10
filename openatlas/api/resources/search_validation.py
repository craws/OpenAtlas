import ast
from typing import Any

from openatlas import app
from openatlas.api.resources.error import (
    InvalidSearchSyntax, LogicalOperatorError, NoSearchStringError,
    OperatorError, SearchValueError, ValueNotIntegerError)


def parameter_validation(params: list[str]) -> list[dict[str, Any]]:
    try:
        parameters = [ast.literal_eval(item) for item in params]
    except Exception as e:
        raise InvalidSearchSyntax from e
    for param in parameters:
        for search_key, value_list in param.items():
            for values in value_list:
                values['logicalOperator'] = \
                    values.get('logicalOperator') or 'or'
                if values['logicalOperator'] \
                        not in app.config['LOGICAL_OPERATOR']:
                    raise LogicalOperatorError
                if values['operator'] not in app.config['COMPARE_OPERATORS']:
                    raise OperatorError
                if not values["values"]:
                    raise NoSearchStringError
                if search_key not in app.config['VALID_VALUES']:
                    raise SearchValueError
                if search_key in app.config['INT_VALUES']:
                    for value in values['values']:
                        if not isinstance(value, int):
                            raise ValueNotIntegerError
    return parameters


def check_if_date_search(k: str) -> bool:
    return bool(k in ["beginFrom", "beginTo", "endFrom", "endTo"])


def check_if_date(value: str) -> str | bool:
    return False if value == "None" else value
