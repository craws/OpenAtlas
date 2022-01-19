from typing import Any, Union

from flasgger import swag_from
from flask import Response, json, jsonify
from flask_restful import Resource, marshal

from openatlas.api.v03.resources.parser import gis
from openatlas.api.v03.resources.resolve_endpoints import download
from openatlas.api.v03.templates.geometries import GeometriesTemplate
from openatlas.models.gis import Gis


class GetGeometricEntities(Resource):
    @staticmethod
    @swag_from("../swagger/geometric_entities.yml",
               endpoint="api_03.geometric_entities")
    def get() -> Union[int, Response, tuple[Any, int]]:
        parser = gis.parse_args()
        output = GetGeometricEntities.get_geom_collection(parser)
        if parser['count']:
            return jsonify(len(output['features']))
        if parser['download']:
            return download(
                output,
                GeometriesTemplate.geometries_template(),
                'geometries')
        return marshal(output, GeometriesTemplate.geometries_template()), 200

    @staticmethod
    def get_geom_collection(parser: dict[str, Any]) -> dict[str, Any]:
        return {
            'type': 'FeatureCollection',
            'features': GetGeometricEntities.get_geometries(parser)}

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
