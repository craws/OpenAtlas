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
            aliases: bool = False,
            with_location: bool = True) -> Entity:
        try:
            entity = Entity.get_by_id(id_, types=types, aliases=aliases)
        except Exception as e:
            raise EntityDoesNotExistError from e
        return entity

    @staticmethod
    def get_by_uuid(
            uuid: str,
            types: bool = False,
            aliases: bool = False,
            with_location: bool = True) -> Entity:
        try:
            entity = Entity.get_by_uuid(uuid, types=types, aliases=aliases)
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
    def get_by_view_classes(names: list[str]) -> list[Entity]:
        names = list(g.class_groups) if 'all' in names else names
        # artifact group (now called item) will be deprecated in API v1
        groups = [name.replace('artifact', 'item') for name in names]
        if not set(groups).issubset(g.class_groups):
            raise InvalidViewClassError
        classes = []
        for group in groups:
            classes.extend(g.class_groups[group]['classes'])
        return Entity.get_by_class(classes, types=True, aliases=True)

    @staticmethod
    def get_by_system_classes(names: list[str]) -> list[Entity]:
        names = list(g.classes) if 'all' in names else names
        classes: list[str] = []
        for name in names:
            match name:
                case 'appellation':
                    classes.append('alias')  # pragma: no cover
                case 'source_translation':
                    classes.append('text')  # pragma: no cover
                case _:
                    classes.append(name)
        if not set(classes).issubset(g.classes):
            raise InvalidSystemClassError
        return Entity.get_by_class(classes, types=True, aliases=True)

    @staticmethod
    def get_linked_entities_with_properties(
            id_: int,
            properties: list[str]) -> list[Entity]:
        if 'all' in properties:
            properties = list(g.properties)
        entity = ApiEntity.get_by_id(id_, types=True)
        return (
            [entity]
            + entity.get_linked_entities_recursive(properties, types=True)
            + entity.get_linked_entities_recursive(
                    properties,
                    inverse=True,
                    types=True))
