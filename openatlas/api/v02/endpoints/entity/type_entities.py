from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, g
from flask_restful import Resource

from openatlas.api.v02.resources.error import InvalidSubunitError
from openatlas.api.v02.resources.parser import entity_
from openatlas.api.v02.resources.resolve_endpoints import resolve_entities
from openatlas.api.v02.resources.util import get_entities_by_ids
from openatlas.models.entity import Entity
from openatlas.models.link import Link


class GetTypeEntities(Resource):
    @swag_from("../swagger/type_entities.yml", endpoint="api.type_entities")
    def get(self,
            id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        entities = [entity for entity in GetTypeEntities.get_node(id_)]
        if not entities:
            entities = GetTypeEntities.get_special_nodes(id_)
        return resolve_entities(entities, entity_.parse_args(), id_)

    @staticmethod
    def get_node(id_: int) -> List[Entity]:
        if id_ not in g.types:
            raise InvalidSubunitError  # pragma: no cover
        return [e for e in
                g.types[id_].get_linked_entities(['P2', 'P89'], inverse=True)]

    @staticmethod
    def get_special_nodes(id_: int) -> List[Entity]:
        domain_ids = [link_['domain_id'] for link_ in
                      Link.get_entities_by_type(g.types[id_])]
        range_ids = [link_['range_id'] for link_ in
                     Link.get_entities_by_type(g.types[id_])]
        return get_entities_by_ids(range_ids + domain_ids)
