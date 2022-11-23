from typing import Any, Union

from openatlas.api.resources.error import (
    FilterColumnError, FilterLogicalOperatorError, FilterOperatorError,
    NoSearchStringError, ValueNotIntegerError)

logical_operators: list[str] = ['and', 'or']
str_categories: list[str] = [
    "entityName", "entityDescription", "entityAliases", "entityCidocClass",
    "entitySystemClass", "typeName", "typeNameWithSubs",
    "beginFrom", "beginTo", "endFrom", "endTo"]
int_categories: list[str] = [
    "entityID", "typeID", "typeIDWithSubs", "relationToID"]
set_categories: list[str] = ["valueTypeID"]
valid_categories: list[str] = [
    *str_categories, *int_categories, *set_categories]
compare_operators: list[str] = [
    'equal', 'notEqual', 'greaterThan', 'lesserThan', 'greaterThanEqual',
    'lesserThanEqual', 'like']


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
    if logical_operator not in logical_operators:
        raise FilterLogicalOperatorError
    if categories not in valid_categories:
        raise FilterColumnError
    if operator_ not in compare_operators:
        raise FilterOperatorError
    if not search_values:
        raise NoSearchStringError
    if categories in int_categories:
        if not bool(any(isinstance(value, int) for value in search_values)):
            raise ValueNotIntegerError
    return True


def check_if_date_search(k: str) -> bool:
    return bool(k in ["beginFrom", "beginTo", "endFrom", "endTo"])


def check_if_date(value: str) -> Union[str, bool]:
    return False if value == "None" else value
