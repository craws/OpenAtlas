import json
from typing import Union, Any

from flasgger import swag_from
from flask import Response, jsonify
from flask_restful import Resource, marshal

from openatlas.api.formats.csv import export_database_csv
from openatlas.api.formats.subunits import get_subunits_from_id
from openatlas.api.formats.xml import export_database_xml
from openatlas.api.resources.database_mapper import get_all_entities_as_dict, \
    get_all_links_as_dict, get_properties, get_property_hierarchy, get_classes, \
    get_cidoc_hierarchy
from openatlas.api.resources.error import NotAPlaceError
from openatlas.api.resources.model_mapper import get_entity_by_id

from openatlas.api.resources.parser import gis, entity_
from openatlas.api.resources.resolve_endpoints import download, \
    resolve_subunits
from openatlas.api.resources.templates import geometries_template
from openatlas.api.resources.util import get_geometries
from openatlas.models.export import current_date_for_filename


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


class ExportDatabase(Resource):
    @staticmethod
    @swag_from(
        "../swagger/system_class_count.yml",
        endpoint="api_03.export_database")
    def get(format_: str) -> Union[tuple[Resource, int], Response]:
        geoms = [ExportDatabase.get_geometries_dict(geom) for geom in
                 get_geometries({'geometry': 'gisAll'})]
        tables = {
            'entities': get_all_entities_as_dict(),
            'links': get_all_links_as_dict(),
            'properties': get_properties(),
            'property_hierarchy': get_property_hierarchy(),
            'classes': get_classes(),
            'class_hierarchy': get_cidoc_hierarchy(),
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


class GetSubunits(Resource):
    @staticmethod
    @swag_from("../swagger/subunits.yml", endpoint="api_03.subunits")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        parser = entity_.parse_args()
        entity = get_entity_by_id(id_)
        if not entity.class_.name == 'place':
            raise NotAPlaceError
        subunits = get_subunits_from_id(entity, parser)
        return resolve_subunits(subunits, parser, str(id_))
