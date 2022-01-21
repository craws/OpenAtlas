from typing import Any

from flask_restful import fields


class GeojsonTemplate:

    @staticmethod
    def geojson_template() -> dict[str, Any]:
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
            'types': fields.List(fields.String)}

        return {
            'type': fields.String,
            'geometry': fields.Raw,
            'properties': fields.Nested(properties)}

    @staticmethod
    def geojson_collection_template() -> dict[str, Any]:
        return {
            'type': fields.String,
            'features': fields.List(
                fields.Nested(GeojsonTemplate.geojson_template()))}

    @staticmethod
    def pagination() -> dict[str, Any]:
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
