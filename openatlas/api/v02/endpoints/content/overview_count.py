from typing import Tuple, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource, marshal

from openatlas.api.v02.templates.overview_count import CountTemplate
from openatlas.models.entity import Entity


# Deprecated
class OverviewCount(Resource):
    @staticmethod
    @swag_from("../swagger/overview_count.yml", endpoint="api_02.overview_count")
    def get() -> Union[Tuple[Resource, int], Response]:
        return marshal(
            [{'systemClass': name, 'count': count} for name, count in
             Entity.get_overview_counts().items()],
            CountTemplate.overview_template()), 200
