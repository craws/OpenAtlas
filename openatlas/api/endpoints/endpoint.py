import itertools
import zipfile
from io import BytesIO
from itertools import groupby
from typing import Any

import pandas as pd
from flask import Response, jsonify, request
from flask_restful import marshal

from openatlas import app
from openatlas.api.endpoints.parser import Parser
from openatlas.api.formats.csv import (
    build_dataframe,
    build_dataframe_with_relations,
    build_link_dataframe, get_csv_links, get_csv_types)
from openatlas.api.formats.loud import get_loud_entities
from openatlas.api.resources.resolve_endpoints import (
    download, parse_loud_context)
from openatlas.api.resources.templates import (
    geojson_collection_template, geojson_pagination, linked_place_pagination,
    linked_places_template, loud_pagination, loud_template)
from openatlas.api.resources.util import get_location_link
from openatlas.models.entity import Entity, Link


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

    def get_links_for_entities(self) -> None:
        if not self.entities:
            return
        for entity in self.entities:
            self.entities_with_links[entity.id] = {
                'entity': entity,
                'links': [],
                'links_inverse': []}
        for link_ in self.link_parser_check():
            self.entities_with_links[link_.domain.id]['links'].append(link_)
        for link_ in self.link_parser_check(inverse=True):
            self.entities_with_links[
                link_.range.id]['links_inverse'].append(link_)

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

    def resolve_entities(self) -> Response | dict[str, Any]:
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
        self.get_links_for_entities()
        if self.parser.export == 'csv':
            return self.export_csv_entities()
        if self.parser.export == 'csvNetwork':
            return self.export_csv_network()
        self.get_entities_formatted()
        if self.parser.format in app.config['RDF_FORMATS']:  # pragma: no cover
            return Response(
                self.parser.rdf_output(self.formated_entities),
                mimetype=app.config['RDF_FORMATS'][self.parser.format])
        result = self.get_json_output()
        if self.parser.download == 'true':
            return download(result, self.get_entities_template(result))
        return marshal(result, self.get_entities_template(result))

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
            for k, v in (get_csv_links(e) | get_csv_types(e)).items():
                data[k] = ' | '.join(list(map(str, v)))
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
        show_ = {'relations', 'types', 'depictions', 'links', 'geometry'}
        if set(self.parser.show) & show_:
            links = Entity.get_links_of_entities(
                [entity.id for entity in self.entities],
                self.parser.get_properties_for_links(),
                inverse=inverse)
        return links

    def sort_entities(self) -> None:
        if 'latest' in request.path:
            return
        self.entities = sorted(
            self.entities,
            key=self.parser.get_key,
            reverse=bool(self.parser.sort == 'desc'))

    def remove_duplicates(self) -> None:
        exists: set[int] = set()
        add_ = exists.add  # Faster than always call exists.add()
        self.entities = \
            [e for e in self.entities if not (e.id in exists or add_(e.id))]

    def get_entities_formatted(self) -> None:
        if not self.entities:
            return
        entities = []
        match self.parser.format:
            case 'geojson':
                entities = [self.get_geojson()]
            case 'geojson-v2':
                entities = [self.get_geojson_v2()]
            case 'loud':
                parsed_context = parse_loud_context()
                entities = [
                    get_loud_entities(item, parsed_context)
                    for item in self.entities_with_links.values()]
            case 'lp' | 'lpx':
                entities = [
                    self.parser.get_linked_places_entity(item)
                    for item in self.entities_with_links.values()]
            case _ if self.parser.format \
                    in app.config['RDF_FORMATS']:  # pragma: no cover
                entities = [
                    get_loud_entities(item, parse_loud_context())
                    for item in self.entities_with_links.values()]
        self.formated_entities = entities

    def get_geojson(self) -> dict[str, Any]:
        out = []
        links = Entity.get_links_of_entities(
            [e.id for e in self.entities],
            'P53')
        for e in self.entities:
            if e.class_.view == 'place':
                entity_links = [x for x in links if x.domain.id == e.id]
                e.types.update(get_location_link(entity_links).range.types)
            if geoms := [
                    self.parser.get_geojson_dict(e, geom)
                    for geom in self.parser.get_geom(e)]:
                out.extend(geoms)
            else:
                out.append(self.parser.get_geojson_dict(e))
        return {'type': 'FeatureCollection', 'features': out}

    def get_geojson_v2(self) -> dict[str, Any]:
        out = []
        property_codes = ['P53', 'P74', 'OA8', 'OA9', 'P7', 'P26', 'P27']
        link_parser = self.link_parser_check()
        links = [x for x in link_parser if x.property.code in property_codes]
        for e in self.entities:
            entity_links = [
                link_ for link_ in links if link_.domain.id == e.id]
            if e.class_.view == 'place':
                e.types.update(get_location_link(entity_links).range.types)
            if geom := self.parser.get_geoms_as_collection(
                    e,
                    [x.range.id for x in entity_links]):
                out.append(self.parser.get_geojson_dict(e, geom))
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
