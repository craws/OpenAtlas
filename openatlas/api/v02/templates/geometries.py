from typing import Dict

from flask_restful import fields
from flask_restful.fields import List as RestList


class GeometriesTemplate:

    @staticmethod
    def geometries_template() -> Dict[str, RestList]:
        properties = {
            'id': fields.Integer,
            'name': fields.String,
            'description': fields.String,
            'objectId': fields.Integer,
            'objectDescription': fields.String,
            'objectName': fields.String,
            'objectType': fields.String,
            'shapeType': fields.String}

        return {
            'type': fields.String,
            'geometry': fields.Raw,
            'properties': fields.List(fields.Nested(properties))}
