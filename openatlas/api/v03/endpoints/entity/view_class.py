from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v03.resources.error import InvalidCodeError
from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.models.entity import Entity


class GetByCode(Resource):
    @swag_from("../swagger/code.yml", endpoint="api_03.code")
    def get(self,
            code: str) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_entities(
            GetByCode.get_by_view(code),
            entity_.parse_args(),
            code)

    @staticmethod
    def get_by_view(code_: str) -> List[Entity]:
        if code_ not in g.view_class_mapping:
            raise InvalidCodeError
        return Entity.get_by_class(
            g.view_class_mapping[code_],
            types=True,
            aliases=True)
