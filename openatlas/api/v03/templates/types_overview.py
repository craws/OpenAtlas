from typing import Any

from flask_restful import fields


class TypeOverviewTemplate:

    @staticmethod
    def type_overview_template() -> dict[str, Any]:
        children = {
            'id': fields.Integer,
            'url': fields.String,
            'label': fields.String,
            'children': fields.List(fields.Raw)}

        type_details = {
            'id': fields.Integer,
            'name': fields.String,
            'viewClass': fields.List(fields.String),
            'children': fields.List(fields.Nested(children))}

        return {
            'standard': fields.List(fields.Nested(type_details)),
            'place': fields.List(fields.Nested(type_details)),
            'custom': fields.List(fields.Nested(type_details)),
            'value': fields.List(fields.Nested(type_details)),
            'system': fields.List(fields.Nested(type_details))}
