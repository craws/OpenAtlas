from flask_restful import fields
from flask_restful.fields import List as RestList


class UsageTemplate:

    @staticmethod
    def usage_template() -> dict[str, RestList]:
        examples = {
            'entity': fields.String,
            'code': fields.String,
            'class': fields.String,
            'systemClass': fields.String,
            'query': fields.String,
            'latest': fields.String,
            'nodeEntities': fields.String,
            'nodeEntitiesAll': fields.String,
            'subunit': fields.String,
            'subunitHierarchy': fields.String}

        return {
            'message': fields.String,
            'examples': fields.List(fields.Nested(examples))}
