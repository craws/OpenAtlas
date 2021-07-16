from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.error import InvalidCidocClassCode
from openatlas.api.v02.resources.helpers import resolve_entity
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetByClass(Resource):  # type: ignore
    @swag_from("../swagger/class_code.yml", endpoint="api.class_code")
    def get(self, class_code: str) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        p = entity_parser.parse_args()
        return resolve_entity(GetByClass.get_by_class(class_code, p), p, class_code)

    @staticmethod
    def get_by_class(class_code: str, parser: Dict[str, Any]) -> List[Entity]:
        if class_code not in g.cidoc_classes:
            raise InvalidCidocClassCode
        return [Entity(row) for row in Db.get_by_class_code(class_code, parser)]
