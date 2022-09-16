import zipfile
from io import BytesIO
from itertools import groupby
from typing import Any, Union

import pandas as pd
from flasgger import swag_from
from flask import Response, g, json, jsonify
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v03.resources.parser import gis, language
from openatlas.api.v03.resources.resolve_endpoints import download
from openatlas.api.v03.resources.templates import (
    class_overview_template,
    content_template,
    geometries_template,
    overview_template)
from openatlas.models.content import get_translation
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.database.link import Link as Db_link
from openatlas.database.entity import Entity as Db_entity


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
            'features': GetGeometricEntities.get_geometries(parser)}
        if parser['count'] == 'true':
            return jsonify(len(output['features']))
        if parser['download'] == 'true':
            return download(output, geometries_template(), 'geometries')
        return marshal(output, geometries_template()), 200

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
        entities = Db_entity.get_all_entities()
        links = Db_link.get_all_links()
        geometries = GetGeometricEntities.get_geometries(
            {'geometry': 'gisAll'})
        archive = BytesIO()
        with zipfile.ZipFile(archive, 'w') as zipped_file:
            for key, frame in ExportDatabase.get_grouped_entities(
                    entities).items():
                with zipped_file.open(f'{key}.csv', 'w') as file:
                    file.write(bytes(
                        pd.DataFrame(data=frame).to_csv(), encoding='utf8'))
            with zipped_file.open('links.csv', 'w') as file:
                file.write(bytes(
                    pd.DataFrame(data=links).to_csv(), encoding='utf8'))
            with zipped_file.open('geometries.csv', 'w') as file:
                file.write(bytes(
                    pd.DataFrame(data=geometries).to_csv(), encoding='utf8'))
        return Response(
            archive.getvalue(),
            mimetype='application/zip',
            headers={'Content-Disposition': 'attachment;filename=oa_csv.zip'})

    @staticmethod
    def get_grouped_entities(entities: list[dict[str, Any]]) -> dict[str, Any]:
        grouped_entities = {}
        for class_, entities_ in groupby(
                sorted(entities, key=lambda entity: entity['openatlas_class_name']),
                key=lambda entity: entity['openatlas_class_name']):
            grouped_entities[class_] = \
                [entity for entity in entities_]
        return grouped_entities

    @staticmethod
    def get_entity_dataframe(entity: Entity) -> dict[str, Any]:
        return {
            'id': str(entity.id),
            'name': entity.name,
            'cidoc_class': entity.cidoc_class.name,
            'system_class': entity.class_.name,
            'description': entity.description,
            'begin_from': entity.begin_from,
            'begin_to': entity.begin_to,
            'begin_comment': entity.begin_comment,
            'end_from': entity.end_from,
            'end_to': entity.end_to,
            'end_comment': entity.end_comment}

