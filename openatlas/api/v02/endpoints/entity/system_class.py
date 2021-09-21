from typing import Any, Dict, List, Tuple, Union

from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.enpoints_util import resolve_entities
from openatlas.api.v02.resources.error import InvalidSystemClassError
from openatlas.api.v02.resources.parser import entity_
from openatlas.database.api import Api as Db
from openatlas.models.entity import Entity


class GetBySystemClass(Resource):  # type: ignore
    @staticmethod
    def get(system_class: str) \
            -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_entities(
            GetBySystemClass.get_by_system(system_class, entity_.parse_args()),
            entity_.parse_args(),
            system_class)

    @staticmethod
    def get_by_system(system_class: str, parser: Dict[str, Any]) \
            -> List[Entity]:
        if system_class not in g.classes:
            raise InvalidSystemClassError
        return [Entity(row) for row in
                Db.get_by_system_class(system_class, parser)]
