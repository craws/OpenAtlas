from flask import request
from flask_restful import Resource

from openatlas.api.parameter import Validation
from openatlas.api.path import Path
from openatlas.api.resources.parser import entity_parser


class GetClass(Resource):
    def get(self, class_code):
        args = entity_parser.parse_args()
        print(args)
        validation = Validation.validate_url_query(request.args)
        class_ = Path.pagination(
            Path.get_entities_by_class(class_code=class_code, validation=validation),
            validation=validation)
        return class_
