from typing import Tuple, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource, marshal

from openatlas.api.v02.templates.overview_count import CountTemplate
from openatlas.models.entity import Entity


# Deprecated
class OverviewCount(Resource):
    @swag_from("../swagger/overview_count.yml", endpoint="api.overview_count")
    def get(self) -> Union[Tuple[Resource, int], Response]:
        return marshal(
            [{'systemClass': name, 'count': count} for name, count in
             Entity.get_overview_counts().items()],
            CountTemplate.overview_template()), 200
