from typing import Any, Dict, List, Tuple, Union

from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.error import InvalidCidocClassCode
from openatlas.api.v02.resources.helpers import resolve_entity_parser
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetByClass(Resource):  # type: ignore
    @staticmethod
    def get(class_code: str) -> Union[Tuple[Resource, int], Response]:
        p = entity_parser.parse_args()
        return resolve_entity_parser(GetByClass.get_by_class(class_code, p), p, class_code)

    @staticmethod
    def get_by_class(class_code: str, parser: Dict[str, Any]) -> List[Entity]:
        if class_code not in g.cidoc_classes:
            raise InvalidCidocClassCode
        return [Entity(row) for row in Db.get_by_class_code(class_code, parser)]
