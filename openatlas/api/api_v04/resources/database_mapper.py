from typing import Any, Optional

from openatlas.database import (
    cidoc as db, entity as db_entity, link as db_link)


def get_all_entities_as_dict() -> list[dict[str, Any]]:
    return db_entity.get_all_entities()


def get_all_links_as_dict() -> list[dict[str, Any]]:
    return db_link.get_all_links()


def get_properties() -> list[dict[str, Any]]:
    return db.cidoc_properties()


def get_property_hierarchy() -> list[dict[str, Any]]:
    return db.property_hierarchy()


def get_classes() -> list[dict[str, Any]]:
    return db.cidoc_classes()


def get_cidoc_hierarchy() -> list[dict[str, Any]]:
    return db.class_hierarchy()


def get_all_links_for_network(
        system_classes: list[str]) -> list[dict[str, Any]]:
    return db_link.get_all_links_for_network(system_classes)


def get_links_by_id_network(ids: set[int]) -> list[dict[str, Any]]:
    return db_link.get_links_by_id_network(ids)


def get_place_linked_to_location_id(ids: list[int]) -> list[dict[str, Any]]:
    return db_link.get_place_linked_to_location_id(ids)


def get_types_linked_to_network_ids(
        ids: set[int],
        type_ids: set[int]) -> set[int]:
    return db_link.get_types_linked_to_network_ids(ids, type_ids)


def get_api_simple_search(
        class_: list[str],
        term: Optional[str]) -> list[dict[str, Any]]:
    return db_entity.api_search(class_, term)


def get_api_search(
        term: str,
        class_: list[str]) -> list[dict[str, Any]]:
    return db_entity.search(term, class_)
