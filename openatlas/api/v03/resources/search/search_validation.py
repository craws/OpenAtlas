from typing import Any, Union

from openatlas.api.v03.resources.error import FilterColumnError, \
    FilterLogicalOperatorError, FilterOperatorError, NoSearchStringError

logical_operators: list[str] = [
    'and',
    'or']
entity_categories: list[str] = [
    "entityName", "entityDescription", "entityAliases", "entityCidocClass",
    "entitySystemClass", "entityID", "typeID", "typeName",
    "typeIDWithSubs", "typeNameWithSubs",
    "beginFrom", "beginTo", "endFrom", "endTo"]
compare_operators: list[str] = [
    'equal', 'notEqual', 'greaterThan', 'lesserThan', 'greaterThanEqual',
    'lesserThanEqual']


def iterate_validation(parameters: list[dict[str, Any]]) -> list[list[bool]]:
    return [[call_validation(search_key, values) for values in value_list]
            for parameter in parameters
            for search_key, value_list in parameter.items()]


def call_validation(search_key: str, values: dict[str, Any]) -> bool:
    return parameter_validation(
        entity_values=search_key,
        operator_=values['operator'],
        search_values=values["values"],
        logical_operator=values[
            'logicalOperator'] if 'logicalOperator' in values else 'or')


def parameter_validation(
        entity_values: Any,
        operator_: str,
        search_values: list[Any],
        logical_operator: str) -> bool:
    if logical_operator not in logical_operators:
        raise FilterLogicalOperatorError
    if entity_values not in entity_categories:
        raise FilterColumnError
    if operator_ not in compare_operators:
        raise FilterOperatorError
    if not search_values:
        raise NoSearchStringError
    return True


def check_if_date_search(k: str) -> bool:
    return bool(k in ["beginFrom", "beginTo", "endFrom", "endTo"])


def check_if_date(value: str) -> Union[str, bool]:
    return False if value == "None" else value
