from typing import Any, Dict, List

from openatlas.api.v03.resources.error import FilterColumnError, \
    FilterLogicalOperatorError, FilterOperatorError, NoSearchStringError

logical_operators: List[str] = [
    'and',
    'or']
entity_categories: List[str] = [
    "entityName", "entityDescription", "entityAliases", "entityCidocClass",
    "entitySystemClass", "entityID", "typeID", "typeName", "typeDescription",
    "valueTypeID", "valueTypeName"]
compare_operators: List[str] = ['equal', 'notEqual']


def iterate_validation(parameters: List[Dict[str, Any]]) -> List[List[bool]]:
    return [[call_validation(search_key, values) for values in value_list]
            for parameter in parameters
            for search_key, value_list in parameter.items()]


def call_validation(search_key: str, values: Dict[str, Any]) -> bool:
    return parameter_validation(
        entity_values=search_key,
        operator_=values['operator'],
        search_values=values["values"],
        logical_operator=values[
            'logicalOperator'] if 'logicalOperator' in values else 'or')


def parameter_validation(
        entity_values: Any,
        operator_: str,
        search_values: List[Any],
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
