from typing import Any, Dict, List, Tuple, Union

from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.enpoints_util import resolve_entities
from openatlas.api.v02.resources.error import InvalidCidocClassCode
from openatlas.api.v02.resources.parser import entity_
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetByClass(Resource):  # type: ignore
    @staticmethod
    def get(class_code: str) \
            -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_entities(
            GetByClass.get_by_class(class_code, entity_.parse_args()),
            entity_.parse_args(),
            class_code)

    @staticmethod
    def get_by_class(class_code: str, parser: Dict[str, Any]) -> List[Entity]:
        if class_code not in g.cidoc_classes:
            raise InvalidCidocClassCode  # pragma: no cover
        return [Entity(row) for row in Db.get_by_class_code(class_code, parser)]
