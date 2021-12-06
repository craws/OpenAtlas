from typing import Any, Dict, Tuple, Union

from flask import Response
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v03.resources.parser import language
from openatlas.api.v03.resources.resolve_endpoints import download
from openatlas.api.v03.templates.content import ContentTemplate
from openatlas.models.content import get_translation


class GetContent(Resource):
    @staticmethod
    def get() -> Union[Tuple[Resource, int], Response]:
        parser = language.parse_args()
        content = GetContent.get_content(parser)
        template = ContentTemplate.content_template()
        if parser['download']:
            return download(content, template, 'content')
        return marshal(content, template), 200

    @staticmethod
    def get_content(parser: Dict[str, Any]) -> Dict[str, Any]:
        lang = parser['lang']
        return {
            'intro': get_translation('intro_for_frontend', lang),
            'contact': get_translation('contact_for_frontend', lang),
            'siteName': get_translation('site_name_for_frontend', lang),
            'imageSizes': app.config['IMAGE_SIZE'],
            'legalNotice': get_translation('legal_notice_for_frontend', lang)}
