from typing import Tuple, Union

from flask import Response
from flask_restful import Resource, marshal

from openatlas.api.v02.templates.systemclass_count import \
    SystemClsCountTemplate
from openatlas.models.entity import Entity


class SystemClassCount(Resource):


    def get(self) -> Union[Tuple[Resource, int], Response]:
        return marshal(
            Entity.get_overview_counts(),
            SystemClsCountTemplate.overview_template()), 200
