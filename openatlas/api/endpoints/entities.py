from typing import Any

from flask import Response, g
from flask_restful import Resource

from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.error import (
    InvalidLimitError, NotATypeError, QueryEmptyError)
from openatlas.api.resources.parser import entity_, query
from openatlas.api.resources.resolve_endpoints import (
    resolve_entities, resolve_entity)
from openatlas.api.resources.util import (
    get_entities_from_type_with_subs, get_entities_linked_to_special_type,
    get_entities_linked_to_special_type_recursive, get_linked_entities_api)


class GetByCidocClass(Resource):
    @staticmethod
    def get(cidoc_class: str) \
            -> tuple[Resource, int] | Response | dict[str, Any]:
        return resolve_entities(
            ApiEntity.get_by_cidoc_classes([cidoc_class]),
            entity_.parse_args(),
            cidoc_class)


class GetBySystemClass(Resource):
    @staticmethod
    def get(system_class: str) \
            -> tuple[Resource, int] | Response | dict[str, Any]:
        return resolve_entities(
            ApiEntity.get_by_system_classes([system_class]),
            entity_.parse_args(),
            system_class)


class GetByViewClass(Resource):
    @staticmethod
    def get(view_class: str) \
            -> tuple[Resource, int] | Response | dict[str, Any]:
        return resolve_entities(
            ApiEntity.get_by_view_classes([view_class]),
            entity_.parse_args(),
            view_class)


class GetEntitiesLinkedToEntity(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        return resolve_entities(
            get_linked_entities_api(id_),
            entity_.parse_args(),
            'linkedEntities')


class GetEntity(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        return resolve_entity(
            ApiEntity.get_entity_by_id_safe(id_),
            entity_.parse_args())


class GetLatest(Resource):
    @staticmethod
    def get(limit: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        if not 0 < limit < 101:
            raise InvalidLimitError
        return resolve_entities(
            ApiEntity.get_latest(limit),
            entity_.parse_args(),
            limit)


class GetTypeEntities(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        if id_ not in g.types:
            raise NotATypeError
        if not (entities := g.types[id_].get_linked_entities(
                ['P2', 'P89'],
                inverse=True,
                types=True)):
            entities = get_entities_linked_to_special_type(id_)
        return resolve_entities(entities, entity_.parse_args(), id_)


class GetTypeEntitiesAll(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        if id_ not in g.types:
            raise NotATypeError
        # Todo rewrite this with recursive
        if not (entities := get_entities_from_type_with_subs(id_)):
            entities = ApiEntity.get_by_ids(
                get_entities_linked_to_special_type_recursive(id_, []),
                types=True,
                aliases=True)
        return resolve_entities(entities, entity_.parse_args(), id_)


class GetQuery(Resource):
    @staticmethod
    def get() -> tuple[Resource, int] | Response | dict[str, Any]:
        parser = query.parse_args()
        if not any([
                parser['entities'],
                parser['cidoc_classes'],
                parser['view_classes'],
                parser['system_classes']]):
            raise QueryEmptyError
        entities = []
        if parser['entities']:
            entities.extend(
                ApiEntity.get_by_ids(
                    parser['entities'],
                    types=True,
                    aliases=True))
        if parser['view_classes']:
            entities.extend(
                ApiEntity.get_by_view_classes(parser['view_classes']))
        if parser['system_classes']:
            entities.extend(
                ApiEntity.get_by_system_classes(parser['system_classes']))
        if parser['cidoc_classes']:
            entities.extend(
                ApiEntity.get_by_cidoc_classes(parser['cidoc_classes']))
        return resolve_entities(entities, parser, 'query')
