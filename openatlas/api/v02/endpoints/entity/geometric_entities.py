from typing import Any, Tuple, Union

from flask import Response, json, jsonify
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.enpoints_util import download
from openatlas.api.v02.resources.parser import gis_parser
from openatlas.api.v02.templates.geometries import GeometriesTemplate
from openatlas.models.gis import Gis


class GetGeometricEntities(Resource):  # type: ignore
    @staticmethod
    def get() -> Union[Tuple[Any, int], Response]:
        parser = gis_parser.parse_args()
        choices = ['gisPointAll', 'gisPointSupers', 'gisPointSubs', 'gisPointSibling',
                   'gisLineAll', 'gisPolygonAll']
        out = []
        for item in choices if parser['geometry'] == 'gisAll' else parser['geometry']:
            for geom in json.loads(Gis.get_all()[item]):
                out.append(geom)
        if parser['count']:
            return jsonify(len(out))
        if parser['download']:
            return download(out, GeometriesTemplate.geometries_template(), 'geometries')
        return marshal(out, GeometriesTemplate.geometries_template()), 200
