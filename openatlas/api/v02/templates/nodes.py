from typing import Dict, Type

from flask_restful import fields
from flask_restful.fields import String


class NodeTemplate:

    @staticmethod
    def node_template() -> Dict[str, Type[String]]:
        node_json = {'id': fields.Integer,
                     'label': fields.String,
                     'url': fields.String}
        node = {"nodes": fields.List(fields.Nested(node_json))}
        return node
