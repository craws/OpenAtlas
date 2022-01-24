from typing import Any, Union

from flasgger import swag_from
from flask import Response, g, json, jsonify
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v03.resources.parser import gis, language
from openatlas.api.v03.resources.resolve_endpoints import download
from openatlas.api.v03.templates.class_mapping import ClassMappingTemplate
from openatlas.api.v03.templates.content import ContentTemplate
from openatlas.api.v03.templates.geometries import GeometriesTemplate
from openatlas.api.v03.templates.systemclass_count import SystemClsCountTemplate
from openatlas.models.content import get_translation
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis


class GetContent(Resource):
    @staticmethod
    @swag_from("../swagger/content.yml", endpoint="api_03.content")
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


class ClassMapping(Resource):
    @staticmethod
    @swag_from("../swagger/class_mapping.yml", endpoint="api_03.class_mapping")
    def get() -> Union[tuple[Resource, int], Response]:
        return marshal([{
                "systemClass": class_.name,
                "crmClass": class_.cidoc_class.code,
                "view": class_.view,
                "icon": class_.icon,
                "en": class_.label}
                for class_ in g.classes.values() if class_.cidoc_class],
            ClassMappingTemplate.class_template()), 200


class GetGeometricEntities(Resource):
    @staticmethod
    @swag_from("../swagger/geometric_entities.yml",
               endpoint="api_03.geometric_entities")
    def get() -> Union[int, Response, tuple[Any, int]]:
        parser = gis.parse_args()
        output = {
            'type': 'FeatureCollection',
            'features': GetGeometricEntities.get_geometries(parser)}
        if parser['count']:
            return jsonify(len(output['features']))
        if parser['download']:
            return download(
                output,
                GeometriesTemplate.geometries_template(),
                'geometries')
        return marshal(output, GeometriesTemplate.geometries_template()), 200

    @staticmethod
    def get_geometries(parser: dict[str, Any]) -> list[dict[str, Any]]:
        choices = [
            'gisPointAll', 'gisPointSupers', 'gisPointSubs',
            'gisPointSibling', 'gisLineAll', 'gisPolygonAll']
        out = []
        for item in choices \
                if parser['geometry'] == 'gisAll' else parser['geometry']:
            for geom in json.loads(Gis.get_all()[item]):
                out.append(geom)
        return out


class SystemClassCount(Resource):
    @staticmethod
    @swag_from("../swagger/system_class_count.yml",
               endpoint="api_03.system_class_count")
    def get() -> Union[tuple[Resource, int], Response]:
        return marshal(
            Entity.get_overview_counts(),
            SystemClsCountTemplate.overview_template()), 200
