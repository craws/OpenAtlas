from typing import Tuple, Union

from flask import Response
from flask_restful import Resource, marshal

from openatlas.api.v02.common.class_ import GetByClass
from openatlas.api.v02.common.code import GetByCode
from openatlas.api.v02.common.system_class import GetBySystemClass
from openatlas.api.v02.resources.error import QueryEmptyError
from openatlas.api.v02.resources.parser import query_parser
from openatlas.api.v02.resources.util import get_entity_by_id
from openatlas.api.v02.resources.helpers import get_template, resolve_entity_parser


class GetQuery(Resource):  # type: ignore
    @staticmethod
    def get() -> Union[Tuple[Resource, int], Response]:
        parser = query_parser.parse_args()
        if not parser['entities'] \
                and not parser['codes'] \
                and not parser['classes'] \
                and not parser['system_classes']:
            raise QueryEmptyError
        entities = []
        if parser['entities']:
            for entity in parser['entities']:
                entities.append(get_entity_by_id(entity))
        if parser['codes']:
            for code_ in parser['codes']:
                entities.extend(GetByCode.get_by_view(code_, parser))
        if parser['system_classes']:
            for system_class in parser['system_classes']:
                entities.extend(GetBySystemClass.get_by_system_class(
                    system_class,
                    parser))
        if parser['classes']:
            for class_ in parser['classes']:
                entities.extend(GetByClass.get_by_class(class_, parser))
        return resolve_entity_parser(entities, parser, 'query')
