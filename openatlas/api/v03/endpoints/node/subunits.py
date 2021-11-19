from typing import Any, Dict, List, Tuple, Union

from flask import Response
from flask_restful import Resource

from openatlas.api.v03.resources.formats.thanados import get_subunits
from openatlas.api.v03.resources.parser import default
from openatlas.api.v03.resources.resolve_endpoints import resolve_subunit_parser
from openatlas.api.v03.resources.util import get_entity_by_id, link_builder
from openatlas.models.entity import Entity


class GetSubunits(Resource):  # type: ignore
    @staticmethod
    def get(id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_subunit_parser(
            GetSubunits.iterate(get_entity_by_id(id_)),
            default.parse_args(),
            id_)

    @staticmethod
    def iterate(entity: Entity):
        entities = GetSubunits.get_all_subunits_recursive(entity, [entity])
        links = link_builder(entities)
        links_inverse = link_builder(entities, True)
        return [
            get_subunits(
                entity,
                [link_ for link_ in links if link_.domain.id == entity.id],
                [link_ for link_ in links_inverse if
                 link_.range.id == entity.id],
                max(entity.modified for entity in entities))
            for entity in entities]

    @staticmethod
    def get_all_subunits_recursive(entity: Entity, data: List[Entity]):
        if entity.class_.name not in ['artifact', 'human_remains']:
            sub_entities = entity.get_linked_entities('P46', nodes=True)
            if sub_entities:
                for e in sub_entities:
                    data.append(e)
                for e in sub_entities:
                    GetSubunits.get_all_subunits_recursive(e, data)
        return data
