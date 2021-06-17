from typing import Any, Dict, List, Tuple, Union

from flask import Response, g
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.error import InvalidCodeError
from openatlas.api.v02.resources.helpers import get_template, resolve_entity_parser
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetBySystemClass(Resource):  # type: ignore
    @staticmethod
    def get(system_class: str) -> Union[Tuple[Resource, int], Response]:
        p = entity_parser.parse_args()
        return resolve_entity_parser(
            GetBySystemClass.get_by_system_class(system_class, p), p, system_class)

    @staticmethod
    def get_by_system_class(system_class: str, parser: Dict[str, Any]) -> List[Entity]:
        if system_class not in g.classes:
            raise InvalidCodeError
        return [Entity(row) for row in Db.get_by_system_class(system_class, parser)]
