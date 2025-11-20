from typing import Any

from flask import Response, g
from flask_restful import Resource, marshal

from openatlas.api.endpoints.endpoint import Endpoint
from openatlas.api.endpoints.parser import Parser
from openatlas.api.formats.presentation_view import get_presentation_view
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.database_mapper import get_api_search, \
    get_api_simple_search
from openatlas.api.resources.error import (
    InvalidLimitError, InvalidSystemClassError, NotATypeError, QueryEmptyError)
from openatlas.api.resources.parser import entity_, presentation, properties, \
    query, search_parser
from openatlas.api.resources.templates import presentation_template
from openatlas.api.resources.util import (
    get_entities_from_type_with_subs, get_entities_linked_to_special_type,
    get_entities_linked_to_special_type_recursive, get_linked_entities_api)
from openatlas.models.entity import Entity


class GetByCidocClass(Resource):
    @staticmethod
    def get(class_: str) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            ApiEntity.get_by_cidoc_classes([class_]),
            entity_.parse_args()).resolve()


class GetBySystemClass(Resource):
    @staticmethod
    def get(class_: str) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            ApiEntity.get_by_system_classes([class_]),
            entity_.parse_args()).resolve()


class GetByViewClass(Resource):
    @staticmethod
    def get(class_: str) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            ApiEntity.get_by_view_classes([class_]),
            entity_.parse_args()).resolve()


class GetEntitiesLinkedToEntity(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            get_linked_entities_api(id_),
            entity_.parse_args()).resolve()


class GetEntityPresentationView(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        parser = Parser(presentation.parse_args())
        result = get_presentation_view(
            ApiEntity.get_by_id(id_, types=True, aliases=True),
            parser)
        if parser.remove_empty_values:
            return result
        return marshal(result, presentation_template())


class GetLinkedEntitiesByPropertyRecursive(Resource):
    @staticmethod
    def get(id_: int) -> Response | dict[str, Any]:
        parser = properties.parse_args()
        return Endpoint(
            ApiEntity.get_linked_entities_with_properties(
                id_,
                parser['properties']),
            parser).resolve()


class GetEntity(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        return Endpoint(
            ApiEntity.get_by_id(id_, types=True, aliases=True),
            entity_.parse_args(),
            single=True).resolve()


class GetLatest(Resource):
    @staticmethod
    def get(limit: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        if not 0 < limit < 101:
            raise InvalidLimitError
        return Endpoint(
            ApiEntity.get_latest(limit),
            entity_.parse_args()).resolve()


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
        return Endpoint(entities, entity_.parse_args()).resolve()


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
        return Endpoint(entities, entity_.parse_args()).resolve()


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
        return Endpoint(entities, parser).resolve()


class GetSearchEntities(Resource):
    @staticmethod
    def get(class_: str) -> tuple[Resource, int] | Response | dict[str, Any]:
        parser = search_parser.parse_args()
        parser['format'] = 'search'
        term = parser['term']
        classes = list(g.classes) if 'all' in class_ else [class_]
        classes = [class_ for class_ in classes if class_ != 'type_tools']
        if not all(sc in g.classes for sc in classes):
            raise InvalidSystemClassError
        simple_search = get_api_simple_search(classes, term)
        data = simple_search
        if term:
            search = get_api_search(term, classes + ['appellation'])
            data = join_lists_of_dicts_remove_duplicates(simple_search, search)
        entities = []
        for row in data:
            if row['openatlas_class_name'] == 'appellation':
                entity = Entity.get_linked_entity_safe_static(
                    row['id'],
                    'P1',
                    True)
                if entity.class_.name not in classes:
                    continue
            else:
                entity = Entity(row)
            if entity:
                entities.append(entity)
        return Endpoint(entities, parser).resolve_simple_search()


def join_lists_of_dicts_remove_duplicates(
        list_1: list[dict[str, Any]],
        list_2: list[dict[str, Any]]) -> list[dict[str, Any]]:
    list_1_set = {tuple(sorted(d.items())) for d in list_1}
    result = list(list_1)

    for item in list_2:
        if tuple(sorted(item.items())) not in list_1_set:
            result.append(item)
            list_1_set.add(tuple(sorted(item.items())))
    return result
