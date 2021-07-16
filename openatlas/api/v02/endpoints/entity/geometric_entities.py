from typing import Any, Tuple, Union

from flasgger import swag_from
from flask import Response, json, jsonify
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.parser import gis_parser
from openatlas.api.v02.templates.geometries import GeometriesTemplate
from openatlas.models.gis import Gis


class GetGeometricEntities(Resource):  # type: ignore
    @swag_from("../swagger/geometric_entities.yml", endpoint="api.geometric_entities")
    def get(self) -> Union[Tuple[Any, int], Response]:
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
            return Download.download(out, GeometriesTemplate.geometries_template(), 'geometries')
        return marshal(out, GeometriesTemplate.geometries_template()), 200
