import ast
from typing import Any, Dict, List

from openatlas.api.resources.error import FilterColumnError, \
    FilterLogicalOperatorError, FilterOperatorError, NoSearchStringError
from openatlas.models.entity import Entity

logical_operators: List[str] = [
    'and',
    'or',
    'onot',
    'anot']

entity_categories: List[str] = [
    "entityName", "entityDescription", "entityAliases", "entityCidocClass",
    "entitySystemClass", "entityID", "typeID", "typeName", "typeDescription"]

compare_operators: List[str] = [
    'like', 'equal', 'notEqual', 'lesser', 'lesserEqual', 'greater',
    'greaterEqual']


def search_str_to_dict(parser: List[str]) -> List[Dict[str, Any]]:
    return [ast.literal_eval(p) for p in parser]


def search_iterate_entities(
        entities: List[Entity],
        parser: List[Dict[str, Any]]) -> List[Entity]:
    return [e for e in entities if (iterate_through_parameters(e, parser))]


def iterate_through_parameters(
        entity: Entity,
        parameters: List[Dict[str, Any]]) -> bool:
    for p in parameters:
        if prepare_parameters(entity, p):
            return True
    return False


def prepare_parameters(entity: Entity, parameter: Dict[str, Any]) -> bool:
    for k, v in parameter.items():
        for i in v:
            logical_o = i['logicalOperator'] if 'logicalOperator' in i else 'or'
            parameter_validation(
                category=k,
                operator_=i['operator'],
                values=i["values"],
                logical_operator=logical_o)
            if search_entity(
                    category=value_to_be_searched(entity, k),
                    operator_=i['operator'],
                    values=i["values"],
                    logical_operator=logical_o):
                return True
    return False


def search_entity(
        category: Any,
        operator_: str,
        values: List[Any],
        logical_operator: str) -> bool:
    return_value = []
    for v in values:
        for ele in category:
            if search_operator(v, ele, operator_):
                return_value.append(True)
            else:
                return_value.append(False)
    return logical_operation(logical_operator, return_value)


def logical_operation(operator_: str, return_value: List[bool]) -> bool:
    if operator_ == 'or':
        return True if any(return_value) else False
    if operator_ == 'and':
        return True if all(return_value) else False


def search_operator(value: Any, element: Any, operator_: str):
    if operator_ == 'like' and element in value:
        return True
    if operator_ == 'equal' and element == value:
        return True
    if operator_ == 'notEqual' and element != value:
        return True
    if operator_ == 'greater' and element > value:
        return True
    if operator_ == 'greaterEqual' and element >= value:
        return True
    if operator_ == 'lesser' and element < value:
        return True
    if operator_ == 'lesserEqual' and element <= value:
        return True
    return False


def value_to_be_searched(entity: Entity, k: str) -> Any:
    if k == "entityID":
        return [entity.id]
    if k == "entityName":
        return entity.name
    if k == "entityDescription":
        return [entity.description]
    if k == "entityAliases":
        return [entity.aliases]
    if k == "entityCidocClass":
        return [entity.cidoc_class]
    if k == "entitySystemClass":
        return [entity.class_]
    if k == "typeName":
        return [node.name for node in entity.nodes]
    if k == "typeID":
        return [node.id for node in entity.nodes]
    if k == "typeDescription":
        return [node.description for node in entity.nodes]


def parameter_validation(
        category: Any,
        operator_: str,
        values: List[Any],
        logical_operator: str) -> None:
    if logical_operator not in logical_operators:
        raise FilterLogicalOperatorError
    if category not in entity_categories:
        raise FilterColumnError
    if operator_ not in compare_operators:
        raise FilterOperatorError
    if values is None:
        raise NoSearchStringError
