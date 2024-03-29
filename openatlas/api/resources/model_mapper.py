from typing import Any

from flask import g

from openatlas.api.resources.error import (
    EntityDoesNotExistError, InvalidCidocClassCodeError,
    InvalidSystemClassError, InvalidViewClassError)
from openatlas.models.entity import Entity


def get_entity_by_id(id_: int) -> Entity:
    try:
        entity = Entity.get_by_id(id_, types=True, aliases=True)
    except Exception as e:
        raise EntityDoesNotExistError from e
    return entity


def get_entities_by_ids(ids: list[int]) -> list[Entity]:
    return Entity.get_by_ids(ids, types=True, aliases=True)


def get_latest_entities(limit: int) -> list[Entity]:
    return Entity.get_latest(limit)


def get_overview_counts() -> dict[str, int]:
    return Entity.get_overview_counts()


def get_by_cidoc_classes(codes: list[str]) -> list[Entity]:
    if 'all' in codes:
        codes = list(g.cidoc_classes)
    elif not set(codes).issubset(g.cidoc_classes):
        raise InvalidCidocClassCodeError
    return Entity.get_by_cidoc_class(codes, types=True, aliases=True)


def get_entities_by_view_classes(codes: list[str]) -> list[Entity]:
    codes = list(g.view_class_mapping) if 'all' in codes else codes
    if not all(c in g.view_class_mapping for c in codes):
        raise InvalidViewClassError
    view_classes = flatten_list_and_remove_duplicates(
        [g.view_class_mapping[view] for view in codes])
    return Entity.get_by_class(view_classes, types=True, aliases=True)


def get_entities_by_system_classes(system_classes: list[str]) -> list[Entity]:
    system_classes = list(g.classes) \
        if 'all' in system_classes else system_classes
    if not all(sc in g.classes for sc in system_classes):
        raise InvalidSystemClassError
    return Entity.get_by_class(system_classes, types=True, aliases=True)


def flatten_list_and_remove_duplicates(list_: list[Any]) -> list[Any]:
    return [item for sublist in list_ for item in sublist if item not in list_]
