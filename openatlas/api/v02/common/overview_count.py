from typing import Tuple, Union

from flasgger import swag_from
from flask import Response, url_for
from flask_restful import Resource, marshal

from openatlas.api.v02.templates.overview_count import OverviewCountTemplate
from openatlas.models.entity import Entity
from openatlas.util.util import api_access


class OverviewCount(Resource):  # type: ignore
    @api_access()  # type: ignore
    @swag_from("../swagger/overview_count.yml", endpoint="overview_count")
    def get(self) -> Union[Tuple[Resource, int], Response]:
        overview = []
        for name, count in Entity.get_overview_counts().items():
            overview.append({'systemClass': name, 'count': count})
        template = OverviewCountTemplate.overview_template()
        return marshal(overview, template), 200
