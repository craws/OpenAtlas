from typing import Any, Dict, List, Tuple, Union

from flask import Response
from flask_restful import Resource

from openatlas.api.resources.parser import entity_
from openatlas.api.resources.resolve_endpoints import resolve_entities
from openatlas.api.resources.util import get_all_links, \
    get_all_links_inverse
from openatlas.models.entity import Entity


class GetLinkedEntities(Resource):  # type: ignore

    def get(self,
            id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_entities(
            GetLinkedEntities.get_linked_entities(id_),
            entity_.parse_args(),
            'linkedEntities')

    @staticmethod
    def get_linked_entities(id_: int) -> List[Entity]:
        domain_ids = [link_.range for link_ in get_all_links(id_)]
        range_ids = [link_.domain for link_ in get_all_links_inverse(id_)]
        return range_ids + domain_ids
