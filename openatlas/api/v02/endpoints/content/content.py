from typing import Tuple, Union

from flask import Response
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.enpoints_util import download
from openatlas.api.v02.resources.parser import language_parser
from openatlas.api.v02.templates.content import ContentTemplate
from openatlas.models.content import Content as Ct


class GetContent(Resource):  # type: ignore
    @staticmethod
    def get() -> Union[Tuple[Resource, int], Response]:
        parser = language_parser.parse_args()
        lang = parser['lang']
        content = {
            'intro': Ct.get_translation('intro_for_frontend', lang),
            'contact': Ct.get_translation('contact_for_frontend', lang),
            'legalNotice': Ct.get_translation('legal_notice_for_frontend', lang),
            'siteName': Ct.get_translation('site_name_for_frontend', lang)}
        template = ContentTemplate.content_template()
        if parser['download']:
            return download(content, template, 'content')
        return marshal(content, template), 200
