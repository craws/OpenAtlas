from typing import Any, Dict, List

from openatlas.models.entity import Entity


def search(
        entities: List[Entity],
        parser: List[Dict[str, Any]]) -> List[Entity]:
    return [e for e in entities if (iterate_through_entities(e, parser))]


def iterate_through_entities(
        entity: Entity,
        parser: List[Dict[str, Any]]) -> bool:
    return True if [p for p in parser if search_result(entity, p)] else False


def search_result(entity: Entity, parameter: Dict[str, Any]) -> bool:
    check = []
    for k, v in parameter.items():
        for i in v:
            logical_o = i['logicalOperator'] if 'logicalOperator' in i else 'or'
            check.append(True if search_entity(
                entity_values=value_to_be_searched(entity, k),
                operator_=i['operator'],
                search_values=i["values"],
                logical_operator=logical_o) else False)
    return True if all(check) else False


def search_entity(
        entity_values: Any,
        operator_: str,
        search_values: List[Any],
        logical_operator: str) -> bool:
    if operator_ == 'equal':
        if logical_operator == 'or':
            return True if any(item in entity_values for item in
                               search_values) else False
        if logical_operator == 'and':
            return True if all(item in entity_values for item in
                               search_values) else False

    if operator_ == 'notEqual':
        if logical_operator == 'or':
            return False if any(item in entity_values for item in
                                search_values) else True
        if logical_operator == 'and':
            return False if all(item in entity_values for item in
                                search_values) else True

    if operator_ == 'like':
        if logical_operator == 'or':
            return True if [item for item in entity_values if any(
                values in item for values in search_values)] else False
        if logical_operator == 'and':
            return True if len(search_values) == len(
                [item for item in entity_values if
                 any(values in item for values in search_values)]) else False

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
