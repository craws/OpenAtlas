import builtins
import operator
from typing import Any

from flask import g

from openatlas.api.resources.util import (
    flatten_list_and_remove_duplicates, get_linked_entities_id_api)
from openatlas.models.entity import Entity


def get_search_values(
        category: str,
        parameter: dict[str, Any]) -> list[str | int | list[int]]:
    values = parameter["values"]
    match category:
        case "typeIDWithSubs":
            values = [[i] + g.types[i].get_sub_ids_recursive() for i in values]
        case "relationToID":
            values = flatten_list_and_remove_duplicates(
                [get_linked_entities_id_api(value) for value in values])
        case _:
            values = [
                value.lower() if isinstance(value, str) else value
                for value in values]
    return values


def search_entity(entity: Entity, param: dict[str, Any]) -> bool:
    entity_values = value_to_be_searched(entity, param)
    operator_ = param['operator']
    search_values = param['search_values']
    logical_operator = param['logical_operator']
    is_comparable = param['is_comparable']

    if not entity_values and (operator_ == 'like' or is_comparable):
        return False

    if any(isinstance(i, list) for i in search_values):
        if logical_operator == 'or':
            search_values = flatten_list_and_remove_duplicates(search_values)
        else:
            bool_values = []
            for item in search_values:
                if operator_ == 'equal':
                    if logical_operator == 'and':
                        bool_values.append(
                            bool(any(item in entity_values for item in item)))
                if operator_ == 'notEqual':
                    if logical_operator == 'and':
                        bool_values.append(
                            bool(not any(
                                item in entity_values for item in item)))
            return all(bool_values)

    operator_mapping = {
        'greaterThan': 'gt',
        'greaterThanEqual': 'ge',
        'lesserThan': 'lt',
        'lesserThanEqual': 'le'}

    def check_value_type() -> bool:
        found_ = False
        values = dict(entity_values)
        op = operator_mapping[operator_]
        for i in search_values:
            if i[0] in values and getattr(operator, op)(values[i[0]], i[1]):
                found_ = True
                if logical_operator == 'or':
                    break
            else:
                if logical_operator == 'and':
                    found_ = False
                    break
        return found_

    found = False
    scope = getattr(builtins, 'any' if logical_operator == 'or' else 'all')
    match operator_:
        case 'equal':
            found = bool(scope([i in entity_values for i in search_values]))
        case 'notEqual':
            found = bool(not scope(i in entity_values for i in search_values))
        case 'like':
            found = bool(scope(
                i in value for i in search_values for value in entity_values))
        case _ if not is_comparable:
            found = False
        case _ if param['category'] == 'valueTypeID':
            found = check_value_type()
        case 'greaterThan':
            found = bool(scope(i < entity_values for i in search_values))
        case 'greaterThanEqual':
            found = bool(scope(i <= entity_values for i in search_values))
        case 'lesserThan':
            found = bool(scope(i > entity_values for i in search_values))
        case 'lesserThanEqual':
            found = bool(scope(i >= entity_values for i in search_values))
    return found


def value_to_be_searched(entity: Entity, param: dict[str, Any])  -> Any:
    value: Any = []
    match param['category']:
        case "entityID" | "relationToID":
            value = [entity.id]
        case "entityName":
            value = [entity.name.lower()]
        case "entityDescription" if entity.description:
            value = [entity.description.lower()]
        case "entityAliases":
            value = list(
                value.lower() for value in entity.aliases.values()
                if isinstance(value, str))
        case "entityCidocClass":
            value = [entity.cidoc_class.code.lower()]
        case "entitySystemClass":
            value = [entity.class_.name.lower()]
        case "typeName":
            value = [type_.name.lower() for type_ in entity.types]
        case "typeID" | "typeIDWithSubs":
            value = [type_.id for type_ in entity.types]
        case "beginFrom":
            value = entity.begin_from
        case "beginTo":
            value = entity.begin_to
        case "endFrom":
            value = entity.end_from
        case "endTo":
            value = entity.end_to
        case "valueTypeID":
            value = []
            for link_ in param['value_type_links']:
                if entity.id == link_.domain.id:
                    value.append((link_.range.id, float(link_.description)))
    return value
