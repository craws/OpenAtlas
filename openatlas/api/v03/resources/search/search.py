from typing import Any, Dict, List

from openatlas.models.entity import Entity


def search(
        entities: List[Entity],
        parser: List[Dict[str, Any]]) -> List[Entity]:
    return [e for e in entities if iterate_through_entities(e, parser)]


def iterate_through_entities(
        entity: Entity,
        parser: List[Dict[str, Any]]) -> bool:
    return bool([p for p in parser if search_result(entity, p)])


def search_result(entity: Entity, parameter: Dict[str, Any]) -> bool:
    check = []
    for key, value in parameter.items():
        for i in value:
            logical_o = i['logicalOperator'] if 'logicalOperator' in i else 'or'
            check.append(bool(search_entity(
                entity_values=value_to_be_searched(entity, key),
                operator_=i['operator'],
                search_values=i["values"],
                logical_operator=logical_o)))
    return bool(all(check))


def search_entity(
        entity_values: Any,
        operator_: str,
        search_values: List[Any],
        logical_operator: str) -> bool:
    if operator_ == 'equal':
        if logical_operator == 'or':
            return bool(any(item in entity_values for item in search_values))
        if logical_operator == 'and':
            return bool(all(item in entity_values for item in search_values))

    if operator_ == 'notEqual':
        if logical_operator == 'or':
            return bool(
                not any(item in entity_values for item in search_values))
        if logical_operator == 'and':
            return bool(
                not all(item in entity_values for item in search_values))
    return False  # pragma: no cover


def value_to_be_searched(entity: Entity, key: str) -> Any:
    if key == "entityID":
        return [entity.id]
    if key == "entityName":
        return entity.name
    if key == "entityAliases":
        return [value for value in entity.aliases.values()]
    if key == "entityCidocClass":
        return [entity.cidoc_class.code]
    if key == "entitySystemClass":
        return [entity.class_.name]
    if key == "typeName":
        return [node.name for node in entity.types]
    if key == "typeID":
        return [node.id for node in entity.types]
