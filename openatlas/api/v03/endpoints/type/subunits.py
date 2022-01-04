from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v03.resources.formats.thanados import get_subunits
from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import resolve_subunit
from openatlas.api.v03.resources.util import get_all_subunits_recursive, \
    get_entity_by_id, link_builder
from openatlas.models.entity import Entity


class GetSubunits(Resource):
    @staticmethod
    @swag_from("../swagger/subunits.yml", endpoint="api_03.subunits")
    def get(id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_subunit(
            GetSubunits.iterate(get_entity_by_id(id_), entity_.parse_args()),
            entity_.parse_args(),
            id_)

    @staticmethod
    def iterate(entity: Entity, parser: Dict[str, Any]) -> List[Dict[str, Any]]:
        root = entity
        hierarchy = get_all_subunits_recursive(entity, [{entity: []}])
        entities = [entity for dict_ in hierarchy for entity in dict_]
        links = link_builder(entities)
        links_inverse = link_builder(entities, True)
        return [
            get_subunits(
                list(entity.keys())[0],
                entity[(list(entity.keys())[0])],
                [link_ for link_ in links if
                 link_.domain.id == list(entity.keys())[0].id],
                [link_ for link_ in links_inverse if
                 link_.range.id == list(entity.keys())[0].id],
                root,
                max(entity.modified for entity in entities if entity.modified),
                parser)
            for entity in hierarchy]
