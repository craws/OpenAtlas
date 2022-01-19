from typing import Any, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v03.resources.error import QueryEmptyError
from openatlas.api.v03.resources.parser import query
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.api.v03.resources.util import get_by_class, get_by_system, \
    get_by_view, get_entities_by_ids
from openatlas.models.entity import Entity


class GetQuery(Resource):
    @staticmethod
    @swag_from("../swagger/query.yml", endpoint="api_03.query")
    def get() -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        parser = query.parse_args()
        if not parser['entities'] \
                and not parser['codes'] \
                and not parser['classes'] \
                and not parser['system_classes']:
            raise QueryEmptyError
        return resolve_entities(GetQuery.get_entities(parser), parser, 'query')

    @staticmethod
    def get_entities(parser: dict[str, Any]) -> list[Entity]:
        entities = []
        if parser['entities']:
            entities.extend(get_entities_by_ids(parser['entities']))
        if parser['codes']:
            for code_ in parser['codes']:
                entities.extend(get_by_view(code_))
        if parser['system_classes']:
            for system_class in parser['system_classes']:
                entities.extend(get_by_system(system_class))
        if parser['classes']:
            for class_ in parser['classes']:
                entities.extend(get_by_class(class_))
        return entities
