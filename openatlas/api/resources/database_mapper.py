from typing import Any

from openatlas.database import (
    cidoc_class as db_class,
    cidoc_property as db_property,
    entity as db_entity,
    link as db_link)


def get_all_entities_as_dict() -> list[dict[str, Any]]:
    return db_entity.get_all_entities()


def get_all_links_as_dict() -> list[dict[str, Any]]:
    return db_link.get_all_links()


def get_properties() -> list[dict[str, Any]]:
    return db_property.get_properties()


def get_property_hierarchy() -> list[dict[str, Any]]:
    return db_property.get_hierarchy()


def get_classes() -> list[dict[str, Any]]:
    return db_class.get_classes()


def get_cidoc_hierarchy() -> list[dict[str, Any]]:
    return db_class.get_hierarchy()


def get_all_links_for_network(
        system_classes: list[str]) -> list[dict[str, Any]]:
    return db_link.get_all_links_for_network(system_classes)


def get_links_by_id_network(ids: list[int])-> list[dict[str, Any]]:
    return db_link.get_links_by_id_network(ids)
