from typing import Any

from flask_restful import fields


class GeometriesTemplate:

    @staticmethod
    def geometries_template() -> dict[str, Any]:
        properties = {
            'id': fields.Integer,
            'name': fields.String,
            'description': fields.String,
            'objectId': fields.Integer,
            'objectDescription': fields.String,
            'objectName': fields.String,
            'objectType': fields.String,
            'shapeType': fields.String}

        feature = {
            'type': fields.String,
            'geometry': fields.Raw,
            'properties': fields.Nested(properties)}

        return {'type': fields.String,
                'features': fields.Nested(feature)}
