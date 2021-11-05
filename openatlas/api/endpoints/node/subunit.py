from typing import Any, Dict, List, Tuple, Union

from flask import Response
from flask_restful import Resource

from openatlas.api.resources.error import InvalidSubunitError
from openatlas.api.resources.parser import default
from openatlas.api.resources.resolve_endpoints import get_node_dict, \
    resolve_node_parser
from openatlas.api.resources.util import get_entity_by_id
from openatlas.models.place import get_structure


class GetSubunit(Resource):  # type: ignore

    def get(self,
            id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_node_parser({"nodes": GetSubunit.get_subunits(id_)},
                                   default.parse_args(), id_)

    @staticmethod
    def get_subunits(id_: int) -> List[Dict[str, Any]]:
        structure = get_structure(get_entity_by_id(id_))
        if not structure or not structure['subunits']:
            raise InvalidSubunitError
        return [get_node_dict(subunit) for subunit in structure['subunits']]
