from typing import Any, Dict, List, Tuple, Union

from flask import Response, g
from flask_restful import Resource

from openatlas.api.v03.resources.error import InvalidCidocClassCode
from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.models.entity import Entity


class GetByClass(Resource):  # type: ignore

    def get(self,
            class_code: str) \
            -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_entities(
            GetByClass.get_by_class(class_code),
            entity_.parse_args(),
            class_code)

    @staticmethod
    def get_by_class(class_code: str) -> List[Entity]:
        if class_code not in g.cidoc_classes:
            raise InvalidCidocClassCode  # pragma: no cover
        return Entity.get_by_cidoc_class(class_code, nodes=True)
