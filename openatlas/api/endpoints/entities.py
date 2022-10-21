from typing import Any, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.resources.error import (
    InvalidLimitError, InvalidSubunitError, QueryEmptyError)
from openatlas.api.resources.parser import entity_, query
from openatlas.api.resources.resolve_endpoints import (
    resolve_entities, resolve_entity)
from openatlas.api.resources.util import (
    get_by_cidoc_classes, get_entities_by_ids, get_entities_by_system_classes,
    get_entities_by_view_classes, get_entities_linked_to_special_type,
    get_entities_linked_to_special_type_recursive, get_entity_by_id,
    get_linked_entities_api, get_entities_from_type_with_subs)
from openatlas.models.entity import Entity


class GetByCidocClass(Resource):
    @staticmethod
    @swag_from("../swagger/cidoc_class.yml", endpoint="api_03.cidoc_class")
    def get(cidoc_class: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_by_cidoc_classes([cidoc_class]),
            entity_.parse_args(),
            cidoc_class)


class GetBySystemClass(Resource):
    @staticmethod
    @swag_from("../swagger/system_class.yml", endpoint="api_03.system_class")
    def get(system_class: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_entities_by_system_classes([system_class]),
            entity_.parse_args(),
            system_class)


class GetByViewClass(Resource):
    @staticmethod
    @swag_from("../swagger/view_class.yml", endpoint="api_03.view_class")
    def get(view_class: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_entities_by_view_classes([view_class]),
            entity_.parse_args(),
            view_class)


class GetEntitiesLinkedToEntity(Resource):
    @staticmethod
    @swag_from(
        "../swagger/entities_linked_to_entity.yml",
        endpoint="api_03.entities_linked_to_entity")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_linked_entities_api(id_),
            entity_.parse_args(),
            'linkedEntities')


class GetLatest(Resource):
    @staticmethod
    @swag_from("../swagger/latest.yml", endpoint="api_03.latest")
    def get(latest: int) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        if not 0 < latest < 101:
            raise InvalidLimitError
        return resolve_entities(
            Entity.get_latest(latest),
            entity_.parse_args(),
            latest)


class GetTypeEntities(Resource):
    @staticmethod
    @swag_from("../swagger/type_entities.yml", endpoint="api_03.type_entities")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        if id_ not in g.types:
            raise InvalidSubunitError
        if not (entities := g.types[id_].get_linked_entities(
                ['P2', 'P89'],
                inverse=True,
                types=True)):
            entities = get_entities_linked_to_special_type(id_)
        return resolve_entities(entities, entity_.parse_args(), id_)


class GetTypeEntitiesAll(Resource):
    @staticmethod
    @swag_from(
        "../swagger/type_entities_all.yml",
        endpoint="api_03.type_entities_all")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        if id_ not in g.types:
            raise InvalidSubunitError
        if not (entities := get_entities_from_type_with_subs(id_)):
            entities = get_entities_by_ids(
                get_entities_linked_to_special_type_recursive(id_, []))
        return resolve_entities(entities, entity_.parse_args(), id_)


class GetQuery(Resource):
    @staticmethod
    @swag_from("../swagger/query.yml", endpoint="api_03.query")
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
    @swag_from("../swagger/entity.yml", endpoint="api_03.entity")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entity(get_entity_by_id(id_), entity_.parse_args())
