from typing import Union, Optional, Any

from flask import g

from openatlas.api.resources.error import EntityDoesNotExistError, \
    InvalidCidocClassCode, InvalidCodeError, InvalidSystemClassError
from openatlas.models.entity import Entity
from openatlas.models.link import Link


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


def get_by_cidoc_classes(class_codes: list[str]) -> list[Entity]:
    class_codes = list(g.cidoc_classes) \
        if 'all' in class_codes else class_codes
    if not all(cc in g.cidoc_classes for cc in class_codes):
        raise InvalidCidocClassCode
    return Entity.get_by_cidoc_class(class_codes, types=True, aliases=True)


def get_entities_by_view_classes(codes: list[str]) -> list[Entity]:
    codes = list(g.view_class_mapping) if 'all' in codes else codes
    if not all(c in g.view_class_mapping for c in codes):
        raise InvalidCodeError
    view_classes = flatten_list_and_remove_duplicates(
        [g.view_class_mapping[view] for view in codes])
    return Entity.get_by_class(view_classes, types=True, aliases=True)


def get_entities_by_system_classes(system_classes: list[str]) -> list[Entity]:
    system_classes = list(g.classes) \
        if 'all' in system_classes else system_classes
    if not all(sc in g.classes for sc in system_classes):
        raise InvalidSystemClassError
    return Entity.get_by_class(system_classes, types=True, aliases=True)


def get_all_links_of_entities(
        entities: Union[int, list[int]],
        codes: Optional[Union[str, list[str]]] = None) -> list[Link]:
    codes = list(g.properties) if not codes else codes
    return Link.get_links(entities, codes)


def get_all_links_of_entities_inverse(
        entities: Union[int, list[int]],
        codes: Optional[Union[str, list[str]]] = None) -> list[Link]:
    codes = list(g.properties) if not codes else codes
    return Link.get_links(entities, codes, inverse=True)


def flatten_list_and_remove_duplicates(list_: list[Any]) -> list[Any]:
    return [item for sublist in list_ for item in sublist if item not in list_]
