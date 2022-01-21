from typing import Any, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.api.v03.resources.util import get_linked_entities_api


class GetEntitiesLinkedToEntity(Resource):
    @staticmethod
    @swag_from(
        "../swagger/entities_linked_to_entity.yml",
        endpoint="api_03.entities_linked_to_entity")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            get_linked_entities_api(id_),
            entity_.parse_args(),
            'linkedEntities')
