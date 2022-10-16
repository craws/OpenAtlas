from typing import Any, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v02.resources.error import (
    EntityDoesNotExistError, InvalidSubunitError)
from openatlas.api.v02.resources.parser import default
from openatlas.api.v02.resources.resolve_endpoints import (
    get_node_dict, resolve_node_parser)
from openatlas.api.v02.resources.util import get_entity_by_id
from openatlas.models.entity import Entity


class GetSubunitHierarchy(Resource):
    @staticmethod
    @swag_from(
        "../swagger/subunit_hierarchy.yml",
        endpoint="api_02.subunit_hierarchy")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        return resolve_node_parser(
            {"nodes": GetSubunitHierarchy.get_subunit_hierarchy(id_)},
            default.parse_args(),
            id_)

    @staticmethod
    def get_subunit_hierarchy(id_: int) -> list[dict[str, Any]]:
        try:
            entity = get_entity_by_id(id_)
        except EntityDoesNotExistError as e:  # pragma: no cover
            raise EntityDoesNotExistError from e
        if not entity.class_.name == 'place' \
                and not entity.class_.name == 'feature' \
                and not entity.class_.name == 'stratigraphic_unit':
            raise InvalidSubunitError  # pragma: no cover
        return GetSubunitHierarchy.get_subunits_recursive(entity, [])

    @staticmethod
    def get_subunits_recursive(
            entity: Entity,
            data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        structure = entity.get_structure()
        if structure and structure['subunits']:
            for sub_id in structure['subunits']:
                data.append(get_node_dict(sub_id))
                GetSubunitHierarchy.get_subunits_recursive(sub_id, data)
        return data
