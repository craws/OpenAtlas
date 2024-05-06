from typing import Any, Tuple

from flask import g

from openatlas.api.resources.search_validation import (
    check_if_date)
from openatlas.api.resources.util import (
    flatten_list_and_remove_duplicates, get_linked_entities_id_api)
from openatlas.models.entity import Entity


def get_search_values(
        category: str,
        parameter: dict[str, Any]) -> list[str | int | list[Any]]:
    values = [
        value.lower() if isinstance(value, str) else value
        for value in parameter["values"]]
    if category in ["typeIDWithSubs"]:
        return [[value] + get_sub_ids(value, []) for value in values]
    if category in ["relationToID"]:
        return flatten_list_and_remove_duplicates(
            [get_linked_entities_id_api(value) for value in values])
    if category in ["valueTypeID"]:
        return flatten_list_and_remove_duplicates(
            [search_for_value(value, parameter) for value in values])
    return values


def get_sub_ids(id_: int, subs: list[Any]) -> list[Any]:
    new_subs = g.types[id_].get_sub_ids_recursive()
    subs.extend(new_subs)
    for sub in new_subs:
        get_sub_ids(sub, subs)
    return subs


def search_for_value(
        values: Tuple[int, float],
        parameter: dict[str, Any]) -> list[int]:
    links = Entity.get_links_of_entities(values[0], inverse=True)
    ids = []
    for link_ in links:
        if link_.description and search_entity(
                entity_values=[float(link_.description)]
                if parameter['operator'] in ['equal', 'notEqual']
                else float(link_.description),
                operator_=parameter['operator'],
                search_values=[values[1]],
                logical_operator=parameter['logicalOperator'],
                is_comparable=True):
            ids.append(link_.domain.id)
    return ids


def search_entity(
        entity_values: Any,
        operator_: str,
        search_values: list[Any],
        logical_operator: str,
        is_comparable: bool) -> bool:
    if not entity_values and (operator_ == 'like' or is_comparable):
        return False

    if any(isinstance(i, list) for i in search_values):
        if logical_operator == 'or':
            search_values = flatten_list_and_remove_duplicates(search_values)
        else:
            bool_values = []
            for search_value in search_values:
                if operator_ == 'equal':
                    if logical_operator == 'and':
                        bool_values.append(bool(any(
                            item in entity_values for item in search_value)))
                if operator_ == 'notEqual':
                    if logical_operator == 'and':
                        bool_values.append(bool(not any(
                            item in entity_values for item in search_value)))
            return all(bool_values)

    bool_ = False
    match operator_:
        case 'equal' if logical_operator == 'or':
            bool_ = bool(any(item in entity_values for item in search_values))
        case 'equal' if logical_operator == 'and':
            bool_ = bool(all(item in entity_values for item in search_values))
        case 'notEqual' if logical_operator == 'or':
            bool_ = bool(
                not any(item in entity_values for item in search_values))
        case 'notEqual' if logical_operator == 'and':
            bool_ = bool(
                not all(item in entity_values for item in search_values))
        case 'like' if logical_operator == 'or':
            bool_ = bool(any(
                item in value for item in search_values
                for value in entity_values))
        case 'like' if logical_operator == 'and':
            bool_ = bool(all(
                item in ' '.join(entity_values) for item in search_values))
        case 'greaterThan' if is_comparable and logical_operator == 'or':
            bool_ = bool(any(item < entity_values for item in search_values))
        case 'greaterThan' if is_comparable and logical_operator == 'and':
            bool_ = bool(all(item < entity_values for item in search_values))
        case 'greaterThanEqual' if is_comparable and logical_operator == 'or':
            bool_ = bool(any(item <= entity_values for item in search_values))
        case 'greaterThanEqual' if is_comparable and logical_operator == 'and':
            bool_ = bool(all(item <= entity_values for item in search_values))
        case 'lesserThan' if is_comparable and logical_operator == 'or':
            bool_ = bool(any(item > entity_values for item in search_values))
        case 'lesserThan' if is_comparable and logical_operator == 'and':
            bool_ = bool(all(item > entity_values for item in search_values))
        case 'lesserThanEqual' if is_comparable and logical_operator == 'or':
            bool_ = bool(any(item >= entity_values for item in search_values))
        case 'lesserThanEqual' if is_comparable and logical_operator == 'and':
            bool_ = bool(all(item >= entity_values for item in search_values))
    return bool_


def value_to_be_searched(entity: Entity, key: str) -> Any:
    match key:
        case "entityID" | "relationToID" | "valueTypeID":
            value = [entity.id]
        case "entityName":
            value = [entity.name.lower()]
        case "entityDescription" if entity.description:
            value = [entity.description.lower()]
        case "entityAliases":
            value = list(value.lower() for value in entity.aliases.values())
        case "entityCidocClass":
            value = [entity.cidoc_class.code.lower()]
        case "entitySystemClass":
            value = [entity.class_.name.lower()]
        case "typeName":
            value = [type_.name.lower() for type_ in entity.types]
        case "typeID" | "typeIDWithSubs":
            value = [type_.id for type_ in entity.types]
        case "beginFrom":
            value = check_if_date(str(entity.begin_from))
        case "beginTo":
            value = check_if_date(str(entity.begin_to))
        case "endFrom":
            value = check_if_date(str(entity.end_from))
        case "endTo":
            value = check_if_date(str(entity.end_to))
        case _:
            value = []
    return value
