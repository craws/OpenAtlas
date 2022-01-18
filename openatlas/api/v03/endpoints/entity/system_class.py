from typing import Any, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v03.resources.error import InvalidSystemClassError
from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.models.entity import Entity


class GetBySystemClass(Resource):
    @staticmethod
    @swag_from("../swagger/system_class.yml", endpoint="api_03.system_class")
    def get(system_class: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            GetBySystemClass.get_by_system(system_class),
            entity_.parse_args(),
            system_class)

    @staticmethod
    def get_by_system(system_class: str) -> list[Entity]:
        if system_class not in g.classes:
            raise InvalidSystemClassError
        return Entity.get_by_class(system_class, types=True, aliases=True)
