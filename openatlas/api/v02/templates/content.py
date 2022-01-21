from typing import Type

from flask_restful import fields
from flask_restful.fields import String


class ContentTemplate:

    @staticmethod
    def content_template() -> dict[str, Type[String]]:
        return {
            'intro': fields.String,
            'contact': fields.String,
            'legalNotice': fields.String,
            'siteName': fields.String,
            'imageSizes': fields.Raw}
