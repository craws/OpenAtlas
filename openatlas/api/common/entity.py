from flask import request
from flask_restful import Resource, marshal_with

import openatlas.api.resources.json_templates as template
from openatlas.api.apifunction import ApiFunction
from openatlas.api.parameter import Validation
from openatlas.api.resources.parser import entity_parser


class GetEntity(Resource):
    @marshal_with(template.entity_json)
    def get(self, id_):
        args = entity_parser.parse_args()
        validation = Validation.validate_url_query(request.args)
        entity = ApiFunction.get_entity(id_, validation)
        entity = {"@context": "teteet",
                  "type": "fields.String",
                  "features": [{"test": "funktioniert"}]
                  }
        return entity
