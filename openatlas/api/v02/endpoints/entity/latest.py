from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v02.resources.error import InvalidLimitError
from openatlas.api.v02.resources.helpers import resolve_entity
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.models.entity import Entity


class GetLatest(Resource):  # type: ignore
    @swag_from("../swagger/latest.yml", endpoint="api.latest")
    def get(self, latest: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_entity(
            GetLatest.get_latest(latest),
            entity_parser.parse_args(),
            latest)

    @staticmethod
    def get_latest(limit_: int) -> List[Entity]:
        if not (0 < limit_ < 101):
            raise InvalidLimitError
        return Entity.get_latest(limit_)
