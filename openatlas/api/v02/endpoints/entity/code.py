from typing import Any, Dict, List, Tuple, Union

from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.enpoints_util import resolve_entities
from openatlas.api.v02.resources.error import InvalidCodeError
from openatlas.api.v02.resources.parser import entity_
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetByCode(Resource):  # type: ignore
    @staticmethod
    def get(code: str) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        p = entity_.parse_args()
        return resolve_entities(GetByCode.get_by_view(code, p), p, code)

    @staticmethod
    def get_by_view(code_: str, parser: Dict[str, Any]) -> List[Entity]:
        if code_ not in g.view_class_mapping:
            raise InvalidCodeError
        sys_class = Db.get_by_system_class(g.view_class_mapping[code_], parser)
        return [Entity(row) for row in sys_class]
