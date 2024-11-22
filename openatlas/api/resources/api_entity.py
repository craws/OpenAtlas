from flask import g

from openatlas.api.resources.error import (
    EntityDoesNotExistError, InvalidCidocClassCodeError,
    InvalidSystemClassError, InvalidViewClassError)
from openatlas.models.entity import Entity


class ApiEntity(Entity):
    @staticmethod
    def get_by_id(
            id_: int,
            types: bool = False,
            aliases: bool = False) -> Entity:
        try:
            entity = Entity.get_by_id(id_, types=types, aliases=aliases)
        except Exception as e:
            raise EntityDoesNotExistError from e
        return entity

    @staticmethod
    def get_by_cidoc_classes(codes: list[str]) -> list[Entity]:
        if 'all' in codes:
            codes = list(g.cidoc_classes)
        elif not set(codes).issubset(g.cidoc_classes):
            raise InvalidCidocClassCodeError
        return Entity.get_by_cidoc_class(codes, types=True, aliases=True)

    @staticmethod
    def get_by_view_classes(codes: list[str]) -> list[Entity]:
        codes = list(g.view_class_mapping) if 'all' in codes else codes
        if not all(c in g.view_class_mapping for c in codes):
            raise InvalidViewClassError
        return Entity.get_by_class(
            sum([g.view_class_mapping[i] for i in codes], []),
            types=True,
            aliases=True)

    @staticmethod
    def get_by_system_classes(classes: list[str]) -> list[Entity]:
        classes = list(g.classes) if 'all' in classes else classes
        if not all(sc in g.classes for sc in classes):
            raise InvalidSystemClassError
        return Entity.get_by_class(classes, types=True, aliases=True)

    @staticmethod
    def get_linked_entities_with_properties(
            id_: int,
            properties: list[str]) -> list[Entity]:
        if 'all' in properties:
            properties = list(g.properties)
        entity = ApiEntity.get_by_id(id_, types=True)
        return ([entity]
                + entity.get_linked_entities_recursive(properties, types=True)
                + entity.get_linked_entities_recursive(
                    properties,
                    inverse=True,
                    types=True))
