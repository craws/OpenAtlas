from typing import Tuple, Union

from flask import Response
from flask_restful import Resource, marshal

from openatlas.api.export.csv_export import ApiExportCSV
from openatlas.api.v02.resources.download import Download
from openatlas.api.v02.resources.linked_places import LinkedPlaces
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.util import get_all_links, get_all_links_inverse, get_entity_by_id, \
    get_template
from openatlas.api.v02.templates.geojson import GeojsonTemplate


class GetEntity(Resource):  # type: ignore
    @staticmethod
    def get(id_: int) -> Union[Tuple[Resource, int], Response]:
        parser = entity_parser.parse_args()
        if parser['format'] == 'geojson':
            entity = GetEntity.get_geojson(id_)
            template = GeojsonTemplate.geojson_template()
            if parser['download']:
                return Download.download(entity, template, id_)
            return marshal(entity, template), 200
        if parser['export'] == 'csv':
            return ApiExportCSV.export_entity(get_entity_by_id(id_))
        entity = LinkedPlaces.get_entity(
            get_entity_by_id(id_),
            get_all_links(id_),
            get_all_links_inverse(id_),
            parser)
        if parser['download']:
            return Download.download(entity, get_template(parser), id_)
        return marshal(entity, get_template(parser)), 200
