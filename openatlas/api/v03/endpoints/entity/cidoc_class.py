from typing import Any, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.api.v03.resources.util import get_by_class


class GetByClass(Resource):
    @staticmethod
    @swag_from("../swagger/cidoc_class.yml", endpoint="api_03.cidoc_class")
    def get(class_code: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_by_class(class_code),
            entity_.parse_args(),
            class_code)
