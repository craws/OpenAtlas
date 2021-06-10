from typing import Dict

from flask_restful import fields
from flask_restful.fields import List as RestList


class GeojsonTemplate:

    @staticmethod
    def geojson_template() -> Dict[str, RestList]:
        features = {
            'type': fields.String,
            'geometry': fields.Raw,
            'properties': fields.Raw}
        return {
            'type': fields.String,
            'features': fields.List(fields.Nested(features))}

