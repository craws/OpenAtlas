import json
from typing import Any, Union

from flask import request
from flasgger import swag_from
from flask import Response, g, jsonify
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.resources.formats.csv import export_database_csv
from openatlas.api.resources.formats.xml import export_database_xml
from openatlas.api.resources.parser import gis, language
from openatlas.api.resources.resolve_endpoints import download
from openatlas.api.resources.templates import (
    class_overview_template, content_template, geometries_template,
    overview_template)
from openatlas.api.resources.util import get_geometries
from openatlas.database.cidoc_class import CidocClass as DbCidocClass
from openatlas.database.cidoc_property import \
    CidocProperty as DbCidocProperty
from openatlas.models.content import get_translation
from openatlas.models.entity import Entity
from openatlas.database.link import Link as DbLink
from openatlas.database.entity import Entity as DbEntity
from openatlas.models.export import current_date_for_filename


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
        if parser['download']:
            return download(content, content_template(), 'content')
        return marshal(content, content_template()), 200


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
            class_overview_template()), 200


class GetGeometricEntities(Resource):
    @staticmethod
    @swag_from(
        "../swagger/geometric_entities.yml",
        endpoint="api_03.geometric_entities")
    def get() -> Union[int, Response, tuple[Any, int]]:
        parser = gis.parse_args()
        output: dict[str, Any] = {
            'type': 'FeatureCollection',
            'features': get_geometries(parser)}
        if parser['count'] == 'true':
            return jsonify(len(output['features']))
        if parser['download'] == 'true':
            return download(output, geometries_template(), 'geometries')
        return marshal(output, geometries_template()), 200


class SystemClassCount(Resource):
    @staticmethod
    @swag_from(
        "../swagger/system_class_count.yml",
        endpoint="api_03.system_class_count")
    def get() -> Union[tuple[Resource, int], Response]:
        return marshal(Entity.get_overview_counts(), overview_template()), 200


class ExportDatabase(Resource):
    @staticmethod
    @swag_from(
        "../swagger/system_class_count.yml",
        endpoint="api_03.export_database")
    def get(format_: str) -> Union[tuple[Resource, int], Response]:
        geoms = [ExportDatabase.get_geometries_dict(geom) for geom in
                 get_geometries({'geometry': 'gisAll'})]
        tables = {
            'entities': DbEntity.get_all_entities(),
            'links': DbLink.get_all_links(),
            'properties': DbCidocProperty.get_properties(),
            'property_hierarchy': DbCidocProperty.get_hierarchy(),
            'classes': DbCidocClass.get_classes(),
            'class_hierarchy': DbCidocClass.get_hierarchy(),
            'geometries': geoms}
        filename = f'{current_date_for_filename()}-export'
        if format_ == 'csv':
            return export_database_csv(tables, filename)
        if format_ == 'xml':
            return export_database_xml(tables, filename)
        return Response(
            json.dumps({key: str(value) for key, value in tables.items()}),
            mimetype='application/json',
            headers={
                'Content-Disposition': f'attachment;filename={filename}.json'})

    @staticmethod
    def get_geometries_dict(
            geom: dict[str, Any]) -> dict[str, Any]:
        return {
            'id': geom['properties']['id'],
            'locationId': geom['properties']['locationId'],
            'objectId': geom['properties']['objectId'],
            'name': geom['properties']['name'],
            'objectName': geom['properties']['objectName'],
            'objectDescription': geom['properties']['objectDescription'],
            'coordinates': geom['geometry']['coordinates'],
            'type': geom['geometry']['type']}
