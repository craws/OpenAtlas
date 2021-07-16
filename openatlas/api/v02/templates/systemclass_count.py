from typing import Dict, Type, Union

from flask_restful import fields
from flask_restful.fields import Integer, String


class SystemClassCountTemplate:

    @staticmethod
    def overview_template() -> Dict[str, Type[Union[String, Integer]]]:
        return {'move': fields.Integer,
                'bibliography': fields.Integer,
                'person': fields.Integer,
                'acquisition': fields.Integer,
                'reference_system': fields.Integer,
                'feature': fields.Integer,
                'file': fields.Integer,
                'activity': fields.Integer,
                'type': fields.Integer,
                'administrative_unit': fields.Integer,
                'artifact': fields.Integer,
                'source_translation': fields.Integer,
                'place': fields.Integer,
                'stratigraphic_unit': fields.Integer,
                'edition': fields.Integer,
                'group': fields.Integer,
                'source': fields.Integer
                }
