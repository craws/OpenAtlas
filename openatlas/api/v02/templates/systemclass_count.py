from typing import Type, Union

from flask_restful import fields
from flask_restful.fields import Integer, String


class SystemClsCountTemplate:

    @staticmethod
    def overview_template() -> dict[str, Type[Union[String, Integer]]]:
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
