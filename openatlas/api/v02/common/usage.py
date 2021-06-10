from typing import Tuple, Union

from flask import Response, url_for
from flask_restful import Resource, marshal

from openatlas.api.v02.templates.usage import UsageTemplate


class ShowUsage(Resource):  # type: ignore
    @staticmethod
    def get() -> Union[Tuple[Resource, int], Response]:
        usage = {
            'message': 'The path you entered is not correct.',
            'examples': {
                'entity': url_for('api.entity', id_=23, _external=True),
                'code': url_for('api.code', code='actor', _external=True),
                'class': url_for('api.class', class_code='E18', _external=True),
                'system_class': url_for('api.system_class', system_class='person', _external=True),
                'query':
                    url_for('api.query', classes='E18', view='actor', entities=23, _external=True),
                'latest': url_for('api.latest', latest='30', _external=True),
                'node_entities': url_for('api.node_entities', id_=23, _external=True),
                'node_entities_all': url_for('api.node_entities_all', id_=23, _external=True),
                'subunit': url_for('api.subunit', id_=23, _external=True),
                'subunit_hierarchy': url_for('api.subunit_hierarchy', id_=23, _external=True)}}
        return marshal(usage, UsageTemplate.usage_template()), 200
