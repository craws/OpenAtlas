from typing import Any
from openatlas.database.cidoc_class import CidocClass as DbCidocClass
from openatlas.database.cidoc_property import \
    CidocProperty as DbCidocProperty
from openatlas.database.link import Link as DbLink
from openatlas.database.entity import Entity as DbEntity


def get_all_entities() -> list[dict[str, Any]]:
    return DbEntity.get_all_entities()


def get_all_links() -> list[dict[str, Any]]:
    return DbLink.get_all_links()


def get_properties() -> list[dict[str, Any]]:
    return DbCidocProperty.get_properties()


def get_property_hierarchy() -> list[dict[str, Any]]:
    return DbCidocProperty.get_hierarchy()


def get_classes() -> list[dict[str, Any]]:
    return DbCidocClass.get_classes()


def get_cidoc_hierarchy() -> list[dict[str, Any]]:
    return DbCidocClass.get_hierarchy()
