import json

from flask import Response
from flask_restful import Resource

from openatlas.api.v02.resources.parser import language_parser
from openatlas.models.content import Content


class GetContent(Resource):
    def get(self):
        parser = language_parser.parse_args()
        content = {'intro': Content.get_translation('intro_for_frontend', parser['lang']),
                   'contact': Content.get_translation('contact_for_frontend', parser['lang']),
                   'legal-notice': Content.get_translation('legal_notice_for_frontend',
                                                           parser['lang'])}
        if parser['download']:
            return Response(json.dumps(content), mimetype='application/json',
                            headers={
                                'Content-Disposition': 'attachment;filename=content_' + parser[
                                    'lang'] + '.json'})
        return content
