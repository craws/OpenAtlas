from typing import Any, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_entities
from openatlas.api.v03.resources.util import get_all_links, \
    get_all_links_inverse
from openatlas.models.entity import Entity


class GetEntitiesLinkedToEntity(Resource):
    @staticmethod
    @swag_from(
        "../swagger/entities_linked_to_entity.yml",
        endpoint="api_03.entities_linked_to_entity")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_entities(
            GetEntitiesLinkedToEntity.get_linked_entities(id_),
            entity_.parse_args(),
            'linkedEntities')

    @staticmethod
    def get_linked_entities(id_: int) -> list[Entity]:
        domain_ids = [link_.range for link_ in get_all_links(id_)]
        range_ids = [link_.domain for link_ in get_all_links_inverse(id_)]
        return range_ids + domain_ids
