from typing import Union

from flask import Response, g
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.resources.model_mapper import get_overview_counts
from openatlas.api.resources.parser import default
from openatlas.api.resources.resolve_endpoints import download
from openatlas.api.resources.templates import (
    backend_details_template, class_overview_template, overview_template)


class GetBackendDetails(Resource):
    @staticmethod
    def get() -> Union[tuple[Resource, int], Response]:
        parser = default.parse_args()
        details = {
            'version': app.config['VERSION'],
            'apiVersions': app.config['API_VERSIONS'],
            'siteName': g.settings['site_name'],
            'imageProcessing': {
                'enabled': g.settings['image_processing'],
                'availableImageSizes':
                    app.config['IMAGE_SIZE']
                    if g.settings['image_processing'] else None},
            'IIIF': {
                'enabled': g.settings['iiif'],
                'url': g.settings['iiif_url'],
                'version': int(g.settings['iiif_version'])}}
        if parser['download']:
            download(details, backend_details_template(), 'content')
        return marshal(details, backend_details_template()), 200


class ClassMapping(Resource):
    @staticmethod
    def get() -> Union[tuple[Resource, int], Response]:
        return marshal([{
            "systemClass": class_.name,
            "crmClass":
                class_.cidoc_class.code if class_.cidoc_class else None,
            "view": class_.view,
            "standardTypeId": class_.standard_type_id,
            "icon": class_.icon,
            "en": class_.label}
            for class_ in g.classes.values()],
            class_overview_template()), 200


class SystemClassCount(Resource):
    @staticmethod
    def get() -> Union[tuple[Resource, int], Response]:
        return marshal(get_overview_counts(), overview_template()), 200
