from flask_restful import fields
from flask_restful.fields import List as RestList


class NodesOverviewTemplate:

    @staticmethod
    def node_overview_template() -> dict[str, RestList]:
        categories = {
            'standard': fields.Raw,
            'place': fields.Raw,
            'custom': fields.Raw,
            'value': fields.Raw,
            'system': fields.Raw}
        return {"types": fields.List(fields.Nested(categories))}
