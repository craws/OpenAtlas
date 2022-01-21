from typing import Any, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.api.v03.resources.util import get_by_view


class GetByViewClass(Resource):
    @staticmethod
    @swag_from("../swagger/view_class.yml", endpoint="api_03.view_class")
    def get(code: str) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_by_view(code),
            entity_.parse_args(),
            code)
