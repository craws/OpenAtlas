from typing import Dict, Type

from flask_restful import fields
from flask_restful.fields import String


class ContentTemplate:

    @staticmethod
    def content_template() -> Dict[str, Type[String]]:
        content_json = {'intro': fields.String,
                        'contact': fields.String,
                        'legal-notice': fields.String}
        return content_json
