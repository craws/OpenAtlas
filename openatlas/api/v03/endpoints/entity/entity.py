from typing import Any, Dict, List, Tuple, Union

from flask import Response
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.v03.export.csv_export import ApiExportCSV
from openatlas.api.v03.resources.formats.geojson import Geojson
from openatlas.api.v03.resources.formats.linked_places import get_entity
from openatlas.api.v03.resources.formats.rdf import rdf_output
from openatlas.api.v03.resources.parser import entity_
from openatlas.api.v03.resources.resolve_endpoints import download
from openatlas.api.v03.resources.util import get_all_links, \
    get_all_links_inverse, get_entity_by_id
from openatlas.api.v03.templates.geojson import GeojsonTemplate
from openatlas.api.v03.templates.linked_places import LinkedPlacesTemplate
from openatlas.models.entity import Entity


class GetEntity(Resource):

    def get(self,
            id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return GetEntity.resolve_entity(
            get_entity_by_id(id_),
            entity_.parse_args())

    @staticmethod
    def resolve_entity(
            entity: Entity,
            parser: Dict[str, Any]) \
            -> Union[Response, Dict[str, Any], Tuple[Any, int]]:
        if parser['export'] == 'csv':
            return ApiExportCSV.export_entity(entity)
        result = GetEntity.get_format(entity, parser)
        if parser['format'] in app.config['RDF_FORMATS']:
            return Response(
                rdf_output(result, parser),
                mimetype=app.config['RDF_FORMATS'][parser['format']])
        if parser['download']:
            return download(result, GetEntity.get_template(parser), entity.id)
        return marshal(result, GetEntity.get_template(parser)), 200

    @staticmethod
    def get_format(
            entity: Entity,
            parser: Dict[str, Any]) \
            -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        if parser['format'] == 'geojson':
            return Geojson.return_output(Geojson.get_geojson([entity]))
        return get_entity(
            entity,
            get_all_links(entity.id),
            get_all_links_inverse(entity.id),
            parser)

    @staticmethod
    def get_template(parser: Dict[str, Any]) -> Dict[str, Any]:
        if parser['format'] == 'geojson':
            return GeojsonTemplate.geojson_collection_template()
        return LinkedPlacesTemplate.linked_places_template(parser['show'])
