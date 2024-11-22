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
    build_dataframe, build_link_dataframe)
from openatlas.api.formats.loud import get_loud_entities
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.resolve_endpoints import (
    download, parse_loud_context)
from openatlas.api.resources.templates import (
    geojson_collection_template, linked_places_template, loud_template)
from openatlas.api.resources.util import (
    get_linked_entities_api, get_location_link, remove_duplicate_entities)
from openatlas.models.entity import Entity, Link


class Endpoint:
    def __init__(
            self,
            entities: Entity | list[Entity],
            parser: dict[str, Any]) -> None:
        self.entities = entities if isinstance(entities, list) else [entities]
        self.parser = Parser(parser)

    def resolve_entities(self) -> Response | dict[str, Any]:
        if self.parser.type_id:
            self.entities = self.filter_by_type()
        if self.parser.search:
            self.entities = [
                e for e in self.entities if self.parser.search_filter(e)]
        if self.parser.export == 'csv':
            return self.export_entities_csv()
        if self.parser.export == 'csvNetwork':
            return self.export_csv_for_network_analysis()
        self.remove_duplicate_entities()
        self.sorting()
        result = self.get_json_output()
        if self.parser.format in app.config['RDF_FORMATS']:  # pragma: no cover
            return Response(
                self.parser.rdf_output(result['results']),
                mimetype=app.config['RDF_FORMATS'][self.parser.format])
        if self.parser.count == 'true':
            return jsonify(result['pagination']['entities'])
        if self.parser.download == 'true':
            return download(result, self.parser.get_entities_template())
        return marshal(result, self.parser.get_entities_template())

    def resolve_entity(self) -> Response | dict[str, Any] | tuple[Any, int]:
        if self.parser.export == 'csv':
            return self.export_entities_csv()
        if self.parser.export == 'csvNetwork':
            return self.export_csv_for_network_analysis()
        result = self.get_entity_formatted()
        if (self.parser.format
                in app.config['RDF_FORMATS']):  # pragma: no cover
            return Response(
                self.parser.rdf_output(result),
                mimetype=app.config['RDF_FORMATS'][self.parser.format])
        template = linked_places_template(self.parser)
        if self.parser.format in ['geojson', 'geojson-v2']:
            template = geojson_collection_template()
        if self.parser.format == 'loud':
            template = loud_template(result)
        if self.parser.download:
            return download(result, template)
        return marshal(result, template), 200

    def get_entity_formatted(self) -> dict[str, Any]:
        if self.parser.format == 'geojson':
            return self.get_geojson()
        if self.parser.format == 'geojson-v2':
            return self.get_geojson_v2()
        entity = self.entities[0]
        entity_dict = {
            'entity': entity,
            'links': ApiEntity.get_links_of_entities(entity.id),
            'links_inverse': ApiEntity.get_links_of_entities(
                entity.id, inverse=True)}
        if self.parser.format == 'loud' \
                or self.parser.format in app.config['RDF_FORMATS']:
            return get_loud_entities(entity_dict, parse_loud_context())
        return self.parser.get_linked_places_entity(entity_dict)

    def filter_by_type(self) -> list[Entity]:
        result = []
        for entity in self.entities:
            if any(id_ in [type_.id for type_ in entity.types]
                   for id_ in self.parser.type_id):
                result.append(entity)
        return result

    def export_entities_csv(self) -> Response:
        frames = [build_dataframe(e, relations=True) for e in self.entities]
        return Response(
            pd.DataFrame(data=frames).to_csv(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=result.csv'})

    def export_csv_for_network_analysis(self) -> Response:
        archive = BytesIO()
        with zipfile.ZipFile(archive, 'w') as zipped_file:
            for key, frame in self.get_entities_grouped_by_class().items():
                with zipped_file.open(f'{key}.csv', 'w') as file:
                    file.write(bytes(
                        pd.DataFrame(data=frame).to_csv(), encoding='utf8'))
            with zipped_file.open('links.csv', 'w') as file:
                link_frame = [
                    build_link_dataframe(link_) for link_ in
                    (self.link_parser_check()
                     + self.link_parser_check(inverse=True))]
                file.write(bytes(
                    pd.DataFrame(data=link_frame).to_csv(), encoding='utf8'))
        return Response(
            archive.getvalue(),
            mimetype='application/zip',
            headers={'Content-Disposition': 'attachment;filename=oa_csv.zip'})

    def get_entities_grouped_by_class(self) -> dict[str, Any]:
        self.entities += get_linked_entities_api([e.id for e in self.entities])
        entities = remove_duplicate_entities(self.entities)
        grouped_entities = {}
        for class_, entities_ in groupby(
                sorted(entities, key=lambda entity: entity.class_.name),
                key=lambda entity: entity.class_.name):
            grouped_entities[class_] = \
                [build_dataframe(entity) for entity in entities_]
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

    def sorting(self) -> None:
        if 'latest' in request.path:
            return

        self.entities = sorted(
            self.entities,
            key=self.parser.get_key,
            reverse=bool(self.parser.sort == 'desc'))

    def remove_duplicate_entities(self) -> None:
        seen: set[int] = set()
        seen_add = seen.add  # Faster than always call seen.add()
        self.entities = \
            [e for e in self.entities if not (e.id in seen or seen_add(e.id))]

    def get_json_output(self) -> dict[str, Any]:
        total = [e.id for e in self.entities]
        count = len(total)
        if self.parser.limit == 0:
            self.parser.limit = count
        e_list = []
        if total:
            e_list = list(itertools.islice(total, 0, None, self.parser.limit))
        index = \
            [{'page': num + 1, 'startId': i} for num, i in enumerate(e_list)]
        if index:
            self.parser.first = self.parser.get_by_page(index) \
                if self.parser.page else self.parser.first
        total = self.parser.get_start_entity(total) \
            if self.parser.last or self.parser.first else total
        j = [i for i, x in enumerate(self.entities) if x.id == total[0]]
        formatted_entities = []
        if self.entities:
            self.entities = [e for idx, e in enumerate(self.entities[j[0]:])]
            formatted_entities = self.get_entities_formatted()
        return {
            "results": formatted_entities,
            "pagination": {
                'entitiesPerPage': int(self.parser.limit),
                'entities': count,
                'index': index,
                'totalPages': len(index)}}

    def get_entities_formatted(self) -> list[dict[str, Any]]:
        self.entities = self.entities[:int(self.parser.limit)]
        if self.parser.format == 'geojson':
            return [self.get_geojson()]
        if self.parser.format == 'geojson-v2':
            return [self.get_geojson_v2()]
        entities_dict: dict[int, dict[str, Any]] = {}
        for entity in self.entities:
            entities_dict[entity.id] = {
                'entity': entity,
                'links': [],
                'links_inverse': []}
        for link_ in self.link_parser_check():
            entities_dict[link_.domain.id]['links'].append(link_)
        for link_ in self.link_parser_check(inverse=True):
            entities_dict[link_.range.id]['links_inverse'].append(link_)
        if self.parser.format == 'loud' \
                or self.parser.format in app.config['RDF_FORMATS']:
            return [
                get_loud_entities(item, parse_loud_context())
                for item in entities_dict.values()]
        return [
            self.parser.get_linked_places_entity(item)
            for item in entities_dict.values()]

    def get_geojson(self) -> dict[str, Any]:
        out = []
        links = Entity.get_links_of_entities(
            [e.id for e in self.entities],
            'P53')
        for entity in self.entities:
            if entity.class_.view == 'place':
                entity_links = \
                    [l_ for l_ in links if l_.domain.id == entity.id]
                entity.types.update(
                    get_location_link(entity_links).range.types)
            if geoms := [self.parser.get_geojson_dict(entity, geom)
                         for geom in self.parser.get_geom(entity)]:
                out.extend(geoms)
            else:
                out.append(self.parser.get_geojson_dict(entity))
        return {'type': 'FeatureCollection', 'features': out}

    def get_geojson_v2(self) -> dict[str, Any]:
        out = []
        property_codes = ['P53', 'P74', 'OA8', 'OA9', 'P7', 'P26', 'P27']
        link_parser = self.link_parser_check()
        links = [l for l in link_parser if l.property.code in property_codes]
        for entity in self.entities:
            entity_links = [
                link_ for link_ in links if link_.domain.id == entity.id]
            if entity.class_.view == 'place':
                entity.types.update(
                    get_location_link(entity_links).range.types)
            if geom := self.parser.get_geoms_as_collection(
                    entity,
                    [l_.range.id for l_ in entity_links]):
                out.append(self.parser.get_geojson_dict(entity, geom))
        return {'type': 'FeatureCollection', 'features': out}
