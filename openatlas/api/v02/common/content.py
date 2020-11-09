from flask import request
from flask_restful import Resource

from openatlas.api.v01.parameter import Validation
from openatlas.api.v01.path import Path
from openatlas.api.v02.resources.parser import language_parser


class GetContent(Resource):
    def get(self):
        args = language_parser.parse_args()
        print(args)
        validation = Validation.validate_url_query(request.args)
        content = Path.get_content(validation=validation)
        return content
