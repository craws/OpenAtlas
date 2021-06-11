from typing import Dict

from flask_restful import fields
from flask_restful.fields import List as RestList


class GeojsonTemplate:

    @staticmethod
    def geojson_template() -> Dict[str, RestList]:
        properties = {
            '@id': fields.Integer,
            'systemClass': fields.String,
            'name': fields.String,
            'description': fields.String,
            'begin_earliest': fields.String,
            'begin_latest': fields.String,
            'begin_comment': fields.String,
            'end_earliest': fields.String,
            'end_latest': fields.String,
            'end_comment': fields.String,
            'types': fields.Raw}

        features = {
            'type': fields.String,
            'geometry': fields.Raw,
            'properties': fields.List(fields.Nested(properties))}

        return {
            'type': fields.String,
            'features': fields.List(fields.Nested(features))}
