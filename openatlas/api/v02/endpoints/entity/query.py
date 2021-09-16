from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v02.endpoints.entity.class_ import GetByClass
from openatlas.api.v02.endpoints.entity.code import GetByCode
from openatlas.api.v02.endpoints.entity.system_class import GetBySystemClass
from openatlas.api.v02.resources.enpoints_util import resolve_entities
from openatlas.api.v02.resources.error import QueryEmptyError
from openatlas.api.v02.resources.parser import query
from openatlas.api.v02.resources.util import get_entities_by_ids
from openatlas.models.entity import Entity


class GetQuery(Resource):  # type: ignore
    @swag_from("../swagger/query.yml", endpoint="api.query")
    def get(self) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        parser = query.parse_args()
        if not parser['entities'] \
                and not parser['codes'] \
                and not parser['classes'] \
                and not parser['system_classes']:
            raise QueryEmptyError
        return resolve_entities(GetQuery.get_entities(parser), parser, 'query')

    @staticmethod
    def get_entities(parser: Dict[str, Any]) -> List[Entity]:
        entities = []
        if parser['entities']:
            entities.extend(get_entities_by_ids(parser['entities']))
        if parser['codes']:
            for code_ in parser['codes']:
                entities.extend(GetByCode.get_by_view(code_, parser))
        if parser['system_classes']:
            for system_class in parser['system_classes']:
                entities.extend(GetBySystemClass.get_by_system(
                    system_class,
                    parser))
        if parser['classes']:
            for class_ in parser['classes']:
                entities.extend(GetByClass.get_by_class(class_, parser))
        return entities
