from typing import Tuple, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource, marshal

from openatlas.api.v02.templates.systemclass_count import \
    SystemClsCountTemplate
from openatlas.models.entity import Entity


class SystemClassCount(Resource):
    @staticmethod
    @swag_from("../swagger/system_class_count.yml",
               endpoint="api_02.system_class_count")
    def get() -> Union[Tuple[Resource, int], Response]:
        return marshal(
            Entity.get_overview_counts(),
            SystemClsCountTemplate.overview_template()), 200
