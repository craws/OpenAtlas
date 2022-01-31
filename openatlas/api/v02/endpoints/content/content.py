from typing import Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v02.resources.parser import language
from openatlas.api.v02.resources.resolve_endpoints import download
from openatlas.api.v02.templates.content import ContentTemplate
from openatlas.models.content import get_translation


class GetContent(Resource):
    @staticmethod
    @swag_from("../swagger/content.yml", endpoint="api_02.content")
    def get() -> Union[tuple[Resource, int], Response]:
        parser = language.parse_args()
        lang = parser['lang']
        content = {
            'intro': get_translation('intro_for_frontend', lang),
            'contact': get_translation('contact_for_frontend', lang),
            'siteName': get_translation('site_name_for_frontend', lang),
            'imageSizes': app.config['IMAGE_SIZE'],
            'legalNotice': get_translation('legal_notice_for_frontend', lang)}
        template = ContentTemplate.content_template()
        if parser['download']:
            return download(content, template, 'content')
        return marshal(content, template), 200
