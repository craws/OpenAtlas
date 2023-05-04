from typing import Any, Union

from flask import Response, g
from flask_restful import Resource

from openatlas.api.resources.error import (
    InvalidLimitError, NotATypeError, QueryEmptyError)
from openatlas.api.resources.model_mapper import (
    get_by_cidoc_classes, get_entities_by_ids, get_entities_by_system_classes,
    get_entities_by_view_classes, get_entity_by_id, get_latest_entities)
from openatlas.api.resources.parser import entity_, query
from openatlas.api.resources.resolve_endpoints import (
    resolve_entities, resolve_entity)
from openatlas.api.resources.util import (
    get_entities_from_type_with_subs, get_entities_linked_to_special_type,
    get_entities_linked_to_special_type_recursive, get_linked_entities_api)


class GetByCidocClass(Resource):
    @staticmethod
    def get(cidoc_class: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_by_cidoc_classes([cidoc_class]),
            entity_.parse_args(),
            cidoc_class)


class GetBySystemClass(Resource):
    @staticmethod
    def get(system_class: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_entities_by_system_classes([system_class]),
            entity_.parse_args(),
            system_class)


class GetByViewClass(Resource):
    @staticmethod
    def get(view_class: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_entities_by_view_classes([view_class]),
            entity_.parse_args(),
            view_class)


class GetEntitiesLinkedToEntity(Resource):
    @staticmethod
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_linked_entities_api(id_),
            entity_.parse_args(),
            'linkedEntities')


class GetLatest(Resource):
    @staticmethod
    def get(limit: int) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        if not 0 < limit < 101:
            raise InvalidLimitError
        return resolve_entities(
            get_latest_entities(limit),
            entity_.parse_args(),
            limit)


class GetTypeEntities(Resource):
    @staticmethod
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
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
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        if id_ not in g.types:
            raise NotATypeError
        if not (entities := get_entities_from_type_with_subs(id_)):
            entities = get_entities_by_ids(
                get_entities_linked_to_special_type_recursive(id_, []))
        return resolve_entities(entities, entity_.parse_args(), id_)


class GetQuery(Resource):
    @staticmethod
    def get() -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        parser = query.parse_args()
        if not any([parser['entities'],
                    parser['cidoc_classes'],
                    parser['view_classes'],
                    parser['system_classes']]):
            raise QueryEmptyError
        entities = []
        if parser['entities']:
            entities.extend(get_entities_by_ids(parser['entities']))
        if parser['view_classes']:
            entities.extend(
                get_entities_by_view_classes(parser['view_classes']))
        if parser['system_classes']:
            entities.extend(
                get_entities_by_system_classes(parser['system_classes']))
        if parser['cidoc_classes']:
            entities.extend(get_by_cidoc_classes(parser['cidoc_classes']))
        return resolve_entities(entities, parser, 'query')


class GetEntity(Resource):
    @staticmethod
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entity(get_entity_by_id(id_), entity_.parse_args())
