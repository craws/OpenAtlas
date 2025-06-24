import json
import tempfile
import zipfile
from io import BytesIO
from typing import Any

from fiona.crs import defaultdict
from flask import Response, g, jsonify, url_for
from flask_restful import Resource, marshal
from rdflib import Graph

from openatlas.api.endpoints.endpoint import Endpoint
from openatlas.api.endpoints.parser import Parser
from openatlas.api.formats.csv import export_database_csv
from openatlas.api.formats.network_visualisation import (
    get_ego_network_visualisation, get_network_visualisation)
from openatlas.api.formats.subunits import get_subunits_from_id
from openatlas.api.formats.xml import export_database_xml
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.external.arche import (ACDH, ArcheFileMetadata, \
                                          add_arche_file_metadata_to_graph)
from openatlas.api.resources.database_mapper import (
    get_all_entities_as_dict, get_all_links_as_dict, get_cidoc_hierarchy,
    get_classes, get_properties, get_property_hierarchy)
from openatlas.api.resources.error import EntityNotAnEventError, NotAPlaceError
from openatlas.api.resources.parser import arche, entity_, gis, network
from openatlas.api.resources.resolve_endpoints import (
    download, resolve_subunits)
from openatlas.api.resources.templates import geometries_template, \
    network_visualisation_template
from openatlas.api.resources.util import get_geometries
from openatlas.database.entity import get_linked_entities_recursive
from openatlas.models.export import current_date_for_filename


class GetGeometricEntities(Resource):
    @staticmethod
    def get() -> int | Response | tuple[Any, int]:
        parser = gis.parse_args()
        output: dict[str, Any] = {
            'type': 'FeatureCollection',
            'features': get_geometries(parser)}
        if parser['count'] == 'true':
            return jsonify(len(output['features']))
        if parser['download'] == 'true':
            return download(output, geometries_template())
        return marshal(output, geometries_template()), 200


class ExportDatabase(Resource):
    @staticmethod
    def get(format_: str) -> tuple[Resource, int] | Response:
        geoms = [
            ExportDatabase.get_geometries_dict(geom)
            for geom in get_geometries({'geometry': 'gisAll'})]
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
            json.dumps(tables),
            mimetype='application/json',
            headers={
                'Content-Disposition': f'attachment;filename={filename}.json'})

    @staticmethod
    def get_geometries_dict(geom: dict[str, Any]) -> dict[str, Any]:
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
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        entity = ApiEntity.get_by_id(id_, types=True, aliases=True)
        if entity.class_.name != 'place':
            raise NotAPlaceError
        parser = entity_.parse_args()
        return resolve_subunits(
            get_subunits_from_id(entity, parser),
            parser,
            str(id_))


class GetNetworkVisualisation(Resource):
    @staticmethod
    def get() -> tuple[Resource, int] | Response | dict[str, Any]:
        parser = Parser(network.parse_args())
        results = get_network_visualisation(parser)
        if parser.download:
            return download(results, network_visualisation_template())
        return marshal(results, network_visualisation_template()), 200


class GetEgoNetworkVisualisation(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        parser = Parser(network.parse_args())
        results = get_ego_network_visualisation(id_, parser)
        if parser.download:
            return download(results, network_visualisation_template())
        return marshal(results, network_visualisation_template()), 200


class GetChainedEvents(Resource):
    @staticmethod
    def get(id_: int) -> tuple[Resource, int] | Response | dict[str, Any]:
        parser = entity_.parse_args()
        entity = ApiEntity.get_by_id(id_)
        if entity.class_.view != 'event':
            raise EntityNotAnEventError
        root_id = entity.id
        if chained_ids := get_linked_entities_recursive(id_, ['P134'], False):
            root_id = chained_ids[-1]
        return Endpoint(
            ApiEntity.get_linked_entities_with_properties(
                root_id,
                ['P134']),
            parser).get_chained_events(root_id)


class GetFilesForArche(Resource):
    @staticmethod
    def get() -> tuple[Resource, int] | Response | dict[str, Any]:
        parser = arche.parse_args()
        ext_metadata = {
            'topCollection': 'bItem',
            'language': 'en',
            'depositor': 'https://orcid.org/0000-0001-7608-7446',
            'acceptedDate': "2024-01-01",
            'curator': [
                'https://orcid.org/0000-0002-1218-9635',
                'https://orcid.org/0000-0001-7608-7446'],
            'principalInvestigator': ['Viola Winkler', 'Roland Filzwieser'],
            'relatedDiscipline':
                ['https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601003'],
            'typeIds': [
                196063, 234465, 229739, 198233, 197085, 197087
                ]}

        entities = ApiEntity.get_by_system_classes(['file'])
        if ext_metadata.get('typeIds'):
            print(ext_metadata.get('typeIds'))
            parser['type_id'] = ext_metadata.get('typeIds')
            entities = Endpoint(entities, parser).filter_by_type()
            print(len(entities))
        license_urls = {}
        arche_metadata_list = []
        missing = defaultdict(set)
        checking = set()
        files_path = set()
        for entity in entities:
            if not g.files.get(entity.id):
                missing['No files'].add((entity.id, entity.name))
                checking.add(entity.id)
            if not entity.public:
                missing['Not public'].add((entity.id, entity.name))
                checking.add(entity.id)
            if not entity.standard_type:
                missing['No license'].add((entity.id, entity.name))
                checking.add(entity.id)
            if not entity.creator:
                missing['No creator'].add((entity.id, entity.name))
                checking.add(entity.id)
            if not entity.license_holder:
                missing['No license holder'].add((entity.id, entity.name))
                checking.add(entity.id)
            if entity.id in checking:
                continue
            if entity.standard_type.id not in license_urls:
                for link_ in (
                        entity.standard_type.get_links('P67', inverse=True)):
                    if link_.domain.class_.name == "external_reference":
                        license_urls[entity.standard_type.id] = (
                            link_.domain.name)
                        break
                if entity.standard_type.id not in license_urls:
                    continue
            license_ = license_urls[entity.standard_type.id]
            arche_metadata_list.append(
                ArcheFileMetadata.construct(
                    entity,
                    ext_metadata,
                    license_))
            files_path.add(g.files.get(entity.id))

        graph = Graph()
        graph.bind("acdh", ACDH)
        for metadata_obj in arche_metadata_list:
            add_arche_file_metadata_to_graph(graph, metadata_obj)
        graph = graph.serialize(format="turtle", encoding="utf-8")

        with tempfile.NamedTemporaryFile(
                mode='w+',
                suffix='.md',
                delete=False) as tmp_md:
            tmp_md.write("\n".join(create_failed_files_md(missing)))
            tmp_md_path = tmp_md.name

        files_by_extension = defaultdict(list)
        for f in files_path:
            files_by_extension[normalize_extension(f.suffix)].append(f)

        arche_file = BytesIO()
        with zipfile.ZipFile(arche_file, 'w') as zipf:
            zipf.write(tmp_md_path, arcname='problematic_files.md')
            zipf.writestr('files.ttl', graph)

            for ext, files_list in files_by_extension.items():
                for file_path in files_list:
                    zipf.write(file_path, arcname=f'{ext}/{file_path.name}')

        return Response(
            arche_file.getvalue(),
            mimetype='application/zip',
            headers={
                'Content-Disposition':
                    f'attachment;filename='
                    f'{ext_metadata["topCollection"]}.zip'})


def create_failed_files_md(
        missing: dict[str, set[tuple[int, str]]]) -> list[str]:
    text = []
    for topic, entities in missing.items():
        text.append(f'# {topic} ({len(entities)})')
        for entity in entities:
            text.append(
                f'\t* {entity[0]} - {entity[1]} - '
                f'{url_for("view", id_=entity[0], _external=True)}')
    return text


def normalize_extension(ext: str) -> str:
    ext = ext.lower().lstrip('.')
    if ext == 'jpg':
        return 'jpeg'
    return ext
