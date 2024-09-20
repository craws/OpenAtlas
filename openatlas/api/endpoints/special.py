import json
from collections import defaultdict
from typing import Any

from flask import Response, g, jsonify
from flask_restful import Resource, marshal

from openatlas.api.endpoints.parser import Parser
from openatlas.api.formats.csv import export_database_csv
from openatlas.api.formats.subunits import get_subunits_from_id
from openatlas.api.formats.xml import export_database_xml
from openatlas.api.resources.database_mapper import (
    get_all_entities_as_dict, get_all_links_as_dict, get_all_links_for_network,
    get_cidoc_hierarchy,
    get_classes, get_links_by_id_network, get_properties,
    get_property_hierarchy)
from openatlas.api.resources.error import NotAPlaceError
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.parser import entity_, gis, network
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
        def overwrite_object_locations_with_place() -> None:
            locations = {}
            for l in links:
                if l['property_code'] == 'P53':
                    locations[l['range_id']] = {
                        'range_id': l['domain_id'],
                        'range_name': l['domain_name'],
                        'range_system_class': l['domain_system_class']}

            copy = links.copy()
            for i, l in enumerate(copy):
                if l['range_id'] in locations:
                    links[i].update(
                        range_id=locations[l['range_id']]['range_id'],
                        range_name=locations[l['range_id']]['range_name'],
                        range_system_class=locations[
                            l['range_id']]['range_system_class'])
                if (l['domain_id'] in locations
                        and "administrative_unit" not in exclude_):
                    links[i].update(
                        domain_id=locations[l['domain_id']]['range_id'],
                        domain_name=locations[
                            l['domain_id']]['range_name'],
                        domain_ystem_class=locations[
                            l['domain_id']]['range_system_class'])

        system_classes = g.classes
        location_classes = [
            "administrative_unit",
            "artifact",
            "feature",
            "human_remains",
            "place",
            "stratigraphic_unit"]
        parser = Parser(network.parse_args())
        exclude_ = parser.exclude_system_classes or []
        if all(item in location_classes for item in exclude_):
            exclude_ += ['object_location']
        if exclude_:
            system_classes = [s for s in system_classes if s not in exclude_]

        if linked_to_ids := parser.linked_to_ids:
            ids = []
            for id_ in linked_to_ids:
                ids += get_linked_entities_recursive(
                    id_,
                    list(g.properties),
                    True)
                ids += get_linked_entities_recursive(
                    id_,
                    list(g.properties),
                    False)
            all_ = get_links_by_id_network(ids + linked_to_ids)
            links = []
            if exclude_:
                for link_ in all_:
                    if (link_['domain_system_class'] not in exclude_
                            or link_['range_system_class'] not in exclude_):
                        links.append(link_)
        else:
            links = get_all_links_for_network(system_classes)

        overwrite_object_locations_with_place()
        link_dict = GetNetworkVisualisation.get_link_dictionary(links)

        results: dict[str, Any] = {'results': []}
        for id_, dict_ in link_dict.items():
            if linked_to_ids:
                if not set(linked_to_ids) & set(dict_['relations']):
                    continue
            dict_['id'] = id_
            results['results'].append(dict_)
        if parser.download:
            return download(results, network_visualisation_template())
        return marshal(results, network_visualisation_template()), 200

    @staticmethod
    def get_link_dictionary(links: list[dict[str, Any]]) -> dict[int, Any]:
        output: dict[int, Any] = defaultdict(set)
        for item in links:
            if output.get(item['domain_id']):
                output[item['domain_id']]['relations'].add(item['range_id'])
            else:
                output[item['domain_id']] = {
                    'label': item['domain_name'],
                    'systemClass': item['domain_system_class'],
                    'relations': {item['range_id']}}
            if output.get(item['range_id']):
                output[item['range_id']]['relations'].add(item['domain_id'])
            else:
                output[item['range_id']] = {
                    'label': item['range_name'],
                    'systemClass': item['range_system_class'],
                    'relations': {item['domain_id']}}
        return output
