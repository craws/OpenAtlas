from typing import Any, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.error import InvalidCidocClassCode
from openatlas.api.v02.resources.parser import entity_
from openatlas.api.v02.resources.resolve_endpoints import resolve_entities
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetByClass(Resource):
    @staticmethod
    @swag_from("../swagger/class.yml", endpoint="api_02.class")
    def get(class_code: str) \
            -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            GetByClass.get_by_class(class_code, entity_.parse_args()),
            entity_.parse_args(),
            class_code)

    @staticmethod
    def get_by_class(class_code: str, parser: dict[str, Any]) -> list[Entity]:
        if class_code not in g.cidoc_classes:
            raise InvalidCidocClassCode  # pragma: no cover
        return [
            Entity(row) for row in Db.get_by_class_code(class_code, parser)]
