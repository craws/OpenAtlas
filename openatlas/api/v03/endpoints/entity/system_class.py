from typing import Any, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.api.v03.resources.util import get_by_system


class GetBySystemClass(Resource):
    @staticmethod
    @swag_from("../swagger/system_class.yml", endpoint="api_03.system_class")
    def get(system_class: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_by_system(system_class),
            entity_.parse_args(),
            system_class)
