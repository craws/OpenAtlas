from typing import Dict

from flask_restful import fields
from flask_restful.fields import Nested


class TypeOverviewTemplate:

    @staticmethod
    def type_overview_template() -> Dict[str, Nested]:
        categories = {
            'standard': fields.Raw,
            'place': fields.Raw,
            'custom': fields.Raw,
            'value': fields.Raw,
            'system': fields.Raw}
        return {"types": fields.Nested(categories)}
