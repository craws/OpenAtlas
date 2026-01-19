import itertools
import zipfile
from io import BytesIO
from itertools import groupby
from typing import Any, Iterator

import pandas as pd
from flask import Response, jsonify, request, url_for
from flask_restful import marshal

from openatlas import app
from openatlas.api.endpoints.parser import Parser
from openatlas.api.formats.csv import (
    build_dataframe, build_link_dataframe, get_csv_links, get_csv_types)
from openatlas.api.formats.linked_places import (
    get_lp_file, get_lp_links, get_lp_time)
from openatlas.api.formats.loud import get_loud_entities
from openatlas.api.formats.rdf import rdf_output
from openatlas.api.resources.resolve_endpoints import (
    download, parse_loud_context)
from openatlas.api.resources.templates import (
    geojson_collection_template, geojson_pagination, linked_place_pagination,
    linked_places_template, loud_pagination, loud_template)
from openatlas.api.resources.util import (
    date_to_str, geometry_to_geojson, get_license_ids_with_links,
    get_location_link, get_reference_systems,
    replace_empty_list_values_in_dict_with_none)
from openatlas.display.table import entity_table
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import get_centroids_by_entities, get_gis_by_entities


class Endpoint:
    def __init__(
            self,
            entities: Entity | list[Entity],
            parser: dict[str, Any],
            single: bool = False) -> None:
        self.entities = entities if isinstance(entities, list) else [entities]
        self.parser = Parser(parser)
        self.pagination: dict[str, Any] = {}
        self.single = single
        self.entities_with_links: dict[int, dict[str, Any]] = {}
        self.formated_entities: list[dict[str, Any]] = []
        self.generator_entities: Iterator[dict[str, Any]] = iter(())

    def get_links_for_entities(self) -> None:
        if not self.entities:
            return
        for entity in self.entities:
            self.entities_with_links[entity.id] = {
                'entity': entity,
                'links': [],
                'links_inverse': [],
                'geometry': []}
        for link_ in self.link_parser_check():
            self.entities_with_links[link_.domain.id]['links'].append(link_)
        for link_ in self.link_parser_check(inverse=True):
            self.entities_with_links[
                link_.range.id]['links_inverse'].append(link_)
        for id_, geom in get_gis_by_entities(self.entities).items():
            self.entities_with_links[id_]['geometry'].extend(geom)
        if self.parser.centroid:
            for id_, geom in get_centroids_by_entities(self.entities).items():
                self.entities_with_links[id_]['geometry'].extend(geom)

    def get_pagination(self) -> None:
        total = [e.id for e in self.entities]
        count = len(total)
        self.parser.limit = self.parser.limit or count
        # List of start ids for the index/pages
        e_list = []
        if total:
            e_list = list(itertools.islice(total, 0, None, self.parser.limit))
        index = \
            [{'page': i + 1, 'startId': id_} for i, id_ in enumerate(e_list)]
        if self.parser.page:
            self.parser.first = self.parser.get_by_page(index)
        if self.parser.last or self.parser.first:
            total = self.parser.set_start_entity(total)
        # Finding position in list of first entity
        entity_list_index = 0
        for index_, entity in enumerate(self.entities):
            if entity.id == total[0]:
                entity_list_index = index_
                break
        self.pagination = {
            'count': count, 'index': index, 'entity_index': entity_list_index}

    def reduce_entities_to_limit(self) -> None:
        start = self.pagination['entity_index']
        self.entities = self.entities[start:start + int(self.parser.limit)]

    def resolve(self) -> Response | dict[str, Any]:
        if self.parser.type_id:
            self.entities = self.filter_by_type()
        if self.parser.search:
            self.entities = [
                e for e in self.entities if self.parser.search_filter(e)]
        self.remove_duplicates()
        if self.parser.count == 'true':
            return jsonify(len(self.entities))
        self.sort_entities()
        self.get_pagination()
        self.reduce_entities_to_limit()
        if self.parser.format == 'table_row':
            forms = {'checkbox': True, 'selection_ids': []}
            if self.parser.checked:
                forms['selection_ids'] = self.parser.checked
            return {
                "results": entity_table(
                    items=self.entities,
                    columns=self.parser.table_columns,
                    forms=forms).rows,
                "pagination": {
                    'entitiesPerPage': int(self.parser.limit),
                    'entities': self.pagination['count'],
                    'index': self.pagination['index'],
                    'totalPages': len(self.pagination['index'])}}
        self.get_links_for_entities()
        if self.parser.export == 'csv':
            return self.export_csv_entities()
        if self.parser.export == 'csvNetwork':
            return self.export_csv_network()
        self.get_entities_formatted()
        if self.parser.format in app.config['RDF_FORMATS']:
            return Response(
                rdf_output(self.generator_entities, self.parser.format),
                mimetype=app.config['RDF_FORMATS'][self.parser.format])
        result = self.get_json_output()
        if self.parser.download == 'true':
            return download(result, self.get_entities_template(result))
        return marshal(result, self.get_entities_template(result))

    def resolve_simple_search(self) -> Response | dict[str, Any]:
        self.get_pagination()
        self.reduce_entities_to_limit()
        self.formated_entities = [{
            'name': entity.name,
            'id': url_for('api.entity', id_=entity.id, _external=True),
            'description': entity.description,
            'system_class': entity.class_.name,
            'begin': date_to_str(
                entity.dates.begin_from or entity.dates.begin_to),
            'end': date_to_str(
                entity.dates.end_to or entity.dates.end_from)}
            for entity in self.entities]
        result = self.get_json_output()
        return marshal(result, loud_pagination())

    def get_json_output(self) -> dict[str, Any]:
        return dict(self.formated_entities[0]) if self.single else {
            "results": self.formated_entities,
            "pagination": {
                'entitiesPerPage': int(self.parser.limit),
                'entities': self.pagination['count'],
                'index': self.pagination['index'],
                'totalPages': len(self.pagination['index'])}}

    def filter_by_type(self) -> list[Entity]:
        result = []
        for entity in self.entities:
            if any(
                    id_ in [type_.id for type_ in entity.types]
                    for id_ in self.parser.type_id):
                result.append(entity)
        return result

    def export_csv_entities(self) -> Response:
        frames = []
        for e in self.entities_with_links.values():
            data = build_dataframe(e['entity'])
            for key, value in (get_csv_links(e) | get_csv_types(e)).items():
                data[key] = ' | '.join(list(map(str, value)))
            frames.append(data)
        return Response(
            pd.DataFrame(data=frames).to_csv(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=result.csv'})

    def export_csv_network(self) -> Response:
        entities = []
        links = []
        for items in self.entities_with_links.values():
            entities.append(items['entity'])
            for link_ in items['links']:
                entities.append(link_.range)
                links.append(link_)
            for link_inverse in items['links']:
                entities.append(link_inverse.domain)
                links.append(link_inverse)
        self.entities = entities
        self.remove_duplicates()
        self.get_links_for_entities()
        archive = BytesIO()
        with zipfile.ZipFile(archive, 'w') as zipped_file:
            for key, frame in self.get_entities_grouped_by_class().items():
                with zipped_file.open(f'{key}.csv', 'w') as file:
                    file.write(
                        bytes(
                            pd.DataFrame(data=frame).to_csv(),
                            encoding='utf8'))
            with zipped_file.open('links.csv', 'w') as file:
                frame = [build_link_dataframe(link_) for link_ in links]
                file.write(
                    bytes(pd.DataFrame(data=frame).to_csv(), encoding='utf8'))
        return Response(
            archive.getvalue(),
            mimetype='application/zip',
            headers={'Content-Disposition': 'attachment;filename=oa_csv.zip'})

    def get_entities_grouped_by_class(self) -> dict[str, Any]:
        grouped_entities = {}
        for class_, entities_ in groupby(
                sorted(self.entities, key=lambda entity: entity.class_.name),
                key=lambda entity: entity.class_.name):
            grouped_entities[class_] = [build_dataframe(e) for e in entities_]
        return grouped_entities

    def link_parser_check(self, inverse: bool = False) -> list[Link]:
        links = []
        show_ = {'relations', 'types', 'depictions', 'links'}
        if set(self.parser.show) & show_:
            links = Entity.get_links_of_entities(
                [entity.id for entity in self.entities],
                self.parser.get_properties_for_links(),
                inverse=inverse)
        return links

    def sort_entities(self) -> None:
        if 'latest' in request.path:
            return

        def safe_key(entity: Entity) -> tuple[str, str | int, str]:
            return self.parser.get_key(entity)

        self.entities = sorted(
            self.entities,
            key=safe_key,
            reverse=bool(self.parser.sort == "desc"))

    def remove_duplicates(self) -> None:
        exists: set[int] = set()
        add_ = exists.add  # Faster than always call exists.add()
        self.entities = \
            [e for e in self.entities if not (e.id in exists or add_(e.id))]

    def get_entities_formatted(self) -> None:
        if not self.entities:
            return
        match self.parser.format:
            case 'geojson':
                self.formated_entities = [self.get_geojson()]
            case 'geojson-v2':
                self.formated_entities = [self.get_geojson_v2()]
            case 'loud':
                parsed_context = parse_loud_context()
                license_links = get_license_ids_with_links()
                self.formated_entities = [
                    get_loud_entities(item, parsed_context, license_links)
                    for item in self.entities_with_links.values()]
            case 'lp' | 'lpx':
                self.formated_entities = [
                    self.get_linked_places_entity(_id)
                    for _id in self.entities_with_links]
            case _ if self.parser.format in app.config['RDF_FORMATS']:
                license_links = get_license_ids_with_links()
                parsed_context = parse_loud_context()
                self.generator_entities = (
                    get_loud_entities(
                        item,
                        parsed_context,
                        license_links)
                    for item in self.entities_with_links.values())

    def get_geojson(self) -> dict[str, Any]:
        out = []
        for e in self.entities_with_links.values():
            if e['entity'].class_.group.get('name') == 'place':
                e['entity'].types.update(
                    get_location_link(e['links']).range.types)
            if e['geometry']:
                for geom in e['geometry']:
                    out.append(self.parser.get_geojson_dict(e, geom))
            else:
                out.append(self.parser.get_geojson_dict(e))
        return {'type': 'FeatureCollection', 'features': out}

    def get_geojson_v2(self) -> dict[str, Any]:
        out = []
        for e in self.entities_with_links.values():
            if e['entity'].class_.group.get('name') == 'place':
                e['entity'].types.update(
                    get_location_link(e['links']).range.types)
            out.append(self.parser.get_geojson_dict(e))
        return {'type': 'FeatureCollection', 'features': out}

    def get_entities_template(self, result: dict[str, Any]) -> dict[str, Any]:
        match self.parser.format:
            case 'geojson' | 'geojson-v2':
                template = geojson_collection_template()
                if not self.single:
                    template = geojson_pagination()
            case 'loud':
                template = loud_template(result)
                if not self.single:
                    template = loud_pagination()
            case _:
                template = linked_places_template(self.parser)
                if not self.single:
                    template = linked_place_pagination(self.parser)
        return template

    def get_chained_events(self, root_id: int) -> dict[str, Any]:
        self.get_links_for_entities()
        event_root = self.entities_with_links[root_id]
        event_chain = {
            "name": event_root['entity'].name,
            "id": event_root['entity'].id,
            "system_class": event_root['entity'].class_.name,
            "geometries": event_root['geometry'],
            "children": self.walk_event_tree(event_root['links_inverse'])}
        return event_chain

    def walk_event_tree(self, inverse_l: list[Link]) -> list[dict[str, Any]]:
        items = []
        for links_ in inverse_l:
            if links_.property.code == 'P134':
                items.append(
                    {
                        "name": links_.domain.name,
                        "id": links_.domain.id,
                        "system_class": links_.domain.class_.name,
                        "geometries":
                            self.entities_with_links[links_.domain.id][
                                'geometry'],
                        "children":
                            self.walk_event_tree(
                                self.entities_with_links[links_.domain.id][
                                    'links_inverse'])})
        return items

    def prepare_rdf_export_data(self) -> Iterator[dict[str, Any]]:
        self.get_links_for_entities()
        self.get_entities_formatted()
        return self.generator_entities

    def get_linked_places_entity(self, _id: int) -> dict[str, Any]:
        entity = self.entities_with_links[_id]['entity']
        links = self.entities_with_links[_id]['links']
        links_inverse = self.entities_with_links[_id]['links_inverse']
        geometry = self.entities_with_links[_id]['geometry']
        crm = f'crm:{entity.cidoc_class.code} {entity.cidoc_class.i18n['en']}'
        feature = {
            '@id': url_for('api.entity', id_=entity.id, _external=True),
            'type': 'Feature',
            'crmClass': crm,
            'viewClass': entity.class_.group.get('name'),
            'systemClass': entity.class_.name,
            'properties': {'title': entity.name},
            'types': self.parser.get_lp_types(entity, links)
            if 'types' in self.parser.show else None,
            'depictions': None,
            'when': {'timespans': [get_lp_time(entity)]}
            if 'when' in self.parser.show else None,
            'links': get_reference_systems(links_inverse)
            if 'links' in self.parser.show else None,
            'descriptions': [{'value': entity.description}]
            if 'description' in self.parser.show else None,
            'names':
                [{"alias": value} for value in entity.aliases.values()]
                if entity.aliases and 'names' in self.parser.show else
                None,
            'geometry': geometry_to_geojson(geometry)
            if 'geometry' in self.parser.show else None,
            'relations': get_lp_links(links, links_inverse, self.parser)
            if 'relations' in self.parser.show else None}
        if 'depictions' in self.parser.show:
            if entity.class_.name == 'file':
                feature['depictions'] = get_lp_file(entity)
            else:
                feature['depictions'] = [
                    get_lp_file(link.domain, entity) for link in links_inverse
                    if link.domain.class_.name == 'file']
        return {
            'type': 'FeatureCollection',
            '@context': app.config['API_CONTEXT']['LPF'],
            'features': [replace_empty_list_values_in_dict_with_none(feature)]}
