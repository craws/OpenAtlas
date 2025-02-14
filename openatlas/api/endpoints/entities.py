from typing import Any

from flask import Response, g
from flask_restful import Resource, marshal

from openatlas.api.endpoints.endpoint import Endpoint
from openatlas.api.formats.presentation_view import get_presentation_view
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.error import (
    InvalidLimitError, NotATypeError, QueryEmptyError)
from openatlas.api.resources.parser import entity_, properties, query
from openatlas.api.resources.templates import presentation_template
from openatlas.api.resources.util import (
    get_entities_from_type_with_subs, get_entities_linked_to_special_type,
    get_entities_linked_to_special_type_recursive, get_linked_entities_api)


class GetByCidocClass(Resource):
    @staticmethod
    def get(class_: str) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            ApiEntity.get_by_cidoc_classes([class_]),
            entity_.parse_args()).resolve_entities()


class GetBySystemClass(Resource):
    @staticmethod
    def get(class_: str) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            ApiEntity.get_by_system_classes([class_]),
            entity_.parse_args()).resolve_entities()


class GetByViewClass(Resource):
    @staticmethod
    def get(class_: str) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            ApiEntity.get_by_view_classes([class_]),
            entity_.parse_args()).resolve_entities()


class GetEntitiesLinkedToEntity(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            get_linked_entities_api(id_),
            entity_.parse_args()).resolve_entities()


class GetEntityPresentationView(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        return marshal(
            get_presentation_view(
                ApiEntity.get_by_id(id_, types=True, aliases=True),
                entity_.parse_args()),
            presentation_template())


class GetLinkedEntitiesByPropertyRecursive(Resource):
    @staticmethod
    def get(id_: int) -> Response | dict[str, Any]:
        parser = properties.parse_args()
        return Endpoint(
            ApiEntity.get_linked_entities_with_properties(
                id_,
                parser['properties']),
            parser).resolve_entities()


class GetEntity(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            ApiEntity.get_by_id(id_, types=True, aliases=True),
            entity_.parse_args(),
            single=True).resolve_entities()


class GetLatest(Resource):
    @staticmethod
    def get(limit: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        if not 0 < limit < 101:
            raise InvalidLimitError
        return Endpoint(
            ApiEntity.get_latest(limit),
            entity_.parse_args()).resolve_entities()


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
        return Endpoint(entities, entity_.parse_args()).resolve_entities()


class GetTypeEntitiesAll(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        if id_ not in g.types:
            raise NotATypeError
        if not (entities := get_entities_from_type_with_subs(id_)):
            entities = ApiEntity.get_by_ids(
                get_entities_linked_to_special_type_recursive(id_, []),
                types=True,
                aliases=True)
        return Endpoint(entities, entity_.parse_args()).resolve_entities()


class GetQuery(Resource):
    @staticmethod
    def get() -> tuple[Resource, int] | Response | dict[str, Any]:
        parser = query.parse_args()
        if not any([
            parser['entities'],
            parser['cidoc_classes'],
            parser['view_classes'],
            parser['system_classes'],
            parser['linked_entities']]):
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
        if parser['linked_entities']:
            entities.extend(get_linked_entities_api(parser['linked_entities']))
        return Endpoint(entities, parser).resolve_entities()
