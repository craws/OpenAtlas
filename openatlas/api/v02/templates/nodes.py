from typing import Dict

from flask_restful import fields
from flask_restful.fields import List as RestList


class NodeTemplate:

    @staticmethod
    def node_template() -> Dict[str, RestList]:
        node_json = {'id': fields.Integer,
                     'label': fields.String,
                     'url': fields.String}
        node = {"nodes": fields.List(fields.Nested(node_json))}
        return node
