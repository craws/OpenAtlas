from flask import g

from openatlas.api.resources.error import (
    EntityDoesNotExistError, InvalidCidocClassCodeError,
    InvalidSystemClassError, InvalidViewClassError)
from openatlas.api.resources.util import flatten_list_and_remove_duplicates
from openatlas.models.entity import Entity


class ApiEntity(Entity):
    @staticmethod
    def get_entity_by_id_safe(id_: int) -> Entity:
        try:
            entity = super().get_by_id(id_, types=True, aliases=True)
        except Exception as e:
            raise EntityDoesNotExistError from e
        return entity

    @staticmethod
    def get_by_cidoc_classes(codes: list[str]) -> list[Entity]:
        if 'all' in codes:
            codes = list(g.cidoc_classes)
        elif not set(codes).issubset(g.cidoc_classes):
            raise InvalidCidocClassCodeError
        return super().get_by_cidoc_class(codes, types=True, aliases=True)

    @staticmethod
    def get_by_view_classes(codes: list[str]) -> list[Entity]:
        codes = list(g.view_class_mapping) if 'all' in codes else codes
        if not all(c in g.view_class_mapping for c in codes):
            raise InvalidViewClassError
        view_classes = flatten_list_and_remove_duplicates(
            [g.view_class_mapping[view] for view in codes])
        return super().get_by_class(view_classes, types=True, aliases=True)

    @staticmethod
    def get_by_system_classes(system_classes: list[str]) -> list[Entity]:
        system_classes = list(g.classes) \
            if 'all' in system_classes else system_classes
        if not all(sc in g.classes for sc in system_classes):
            raise InvalidSystemClassError
        return super().get_by_class(system_classes, types=True, aliases=True)
