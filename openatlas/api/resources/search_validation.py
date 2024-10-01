from typing import Any

from openatlas import app
from openatlas.api.resources.error import (
    InvalidSearchCategoryError, InvalidSearchValueError, LogicalOperatorError,
    NoSearchStringError, OperatorError, ValueNotIntegerError)


def check_if_date_search(k: str) -> bool:
    return bool(k in ["beginFrom", "beginTo", "endFrom", "endTo"])


def validate_search_parameters(category: str, values: dict[str, Any]) -> None:
    if values['logicalOperator'] not in app.config['LOGICAL_OPERATOR']:
        raise LogicalOperatorError
    if values['operator'] not in app.config['COMPARE_OPERATORS']:
        raise OperatorError
    if not values["values"]:
        raise NoSearchStringError(category)
    if category in ['beginFrom', 'beginTo', 'endFrom', 'endTo']:
        if len(values["values"]) > 1:
            raise InvalidSearchValueError(category, values["values"])
    if category not in app.config['VALID_VALUES']:
        raise InvalidSearchCategoryError
    if category in app.config['INT_VALUES']:
        for value in values['values']:
            if not isinstance(value, int):
                raise ValueNotIntegerError
