from typing import Dict, List, Union

from flask_restful import fields
from flask_restful.fields import List as RestList, Nested


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

        return {
            'type': fields.String,
            'geometry': fields.Raw,
            'properties': fields.List(fields.Nested(properties))}

    @staticmethod
    def geojson_collection_template():
        return {
            'type': fields.String,
            'features': fields.List(fields.Nested(GeojsonTemplate.geojson_template()))}

    @staticmethod
    def pagination() -> Dict[str, Union[List, Nested]]:
        page_index = {
            "page": fields.Integer,
            "startId": fields.Integer}

        pagination_model = {
            "entities": fields.Integer,
            "entitiesPerPage": fields.Integer,
            "index": fields.List(fields.Nested(page_index)),
            "totalPages": fields.Integer}

        return {
            "results": fields.List(
                fields.Nested(GeojsonTemplate.geojson_collection_template())),
            "pagination": fields.Nested(pagination_model)}
