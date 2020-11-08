from flask import request
from flask_restful import Resource

from openatlas.api.parameter import Validation
from openatlas.api.path import Path
from openatlas.api.resources.parser import language_parser


class GetContent(Resource):
    def get(self):
        args = language_parser.parse_args()
        print(args)
        validation = Validation.validate_url_query(request.args)
        content = Path.get_content(validation=validation)
        return content
