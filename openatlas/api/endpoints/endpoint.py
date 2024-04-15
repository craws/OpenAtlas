import ast
import itertools
import json
import os
import zipfile
from io import BytesIO
from itertools import groupby
from typing import Any, Optional

import numpy
import pandas as pd
from flask import Response, g, jsonify, request
from flask_restful import marshal
from numpy import datetime64
from rdflib import Graph

from openatlas import app
from openatlas.api.formats.csv import (
    build_entity_dataframe, build_link_dataframe)
from openatlas.api.formats.linked_places import get_linked_places_entity
from openatlas.api.formats.loud import get_loud_entities
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.error import (
    EntityDoesNotExistError, InvalidSearchSyntax, LastEntityError,
    LogicalOperatorError, NoSearchStringError, OperatorError, SearchValueError,
    TypeIDError, ValueNotIntegerError)
from openatlas.api.resources.resolve_endpoints import (
    download, parse_loud_context)
from openatlas.api.resources.search import get_search_parameter, \
    iterate_through_entities
from openatlas.api.resources.templates import (
    geojson_collection_template, geojson_pagination, linked_place_pagination,
    linked_places_template, loud_pagination, loud_template)
from openatlas.api.resources.util import (
    flatten_list_and_remove_duplicates, get_geoms_dict,
    get_linked_entities_api, get_location_link, remove_duplicate_entities,
    replace_empty_list_values_in_dict_with_none)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link


class Endpoint:
    def __init__(
            self,
            entities: list[Entity] | Entity,
            parser: dict[str, Any]) -> None:
        self.entities = entities if isinstance(entities, list) else [entities]
        self.parser = parser

    def resolve_entities(self) -> Response | dict[str, Any] | tuple[Any, int]:
        if self.parser['type_id']:
            self.entities = self.filter_by_type(self.parser['type_id'])
            if not self.entities:
                raise TypeIDError
        if self.parser['search']:
            if search_parser := self.parameter_validation():
                parameter = [get_search_parameter(p) for p in search_parser]
                self.entities = [
                    e for e in self.entities
                    if iterate_through_entities(e, parameter)]
        if self.parser['export'] == 'csv':
            return self.export_entities_csv()
        if self.parser['export'] == 'csvNetwork':
            return self.export_csv_for_network_analysis()
        self.remove_duplicate_entities()
        self.sorting()
        result = self.get_json_output()
        if (self.parser['format']
                in app.config['RDF_FORMATS']):  # pragma: no cover
            return Response(
                self.rdf_output(result['results']),
                mimetype=app.config['RDF_FORMATS'][self.parser['format']])
        if self.parser['count'] == 'true':
            return jsonify(result['pagination']['entities'])
        if self.parser['download'] == 'true':
            return download(result, self.get_entities_template())
        return marshal(result, self.get_entities_template()), 200

    def resolve_entity(self) -> Response | dict[str, Any] | tuple[Any, int]:
        if self.parser['export'] == 'csv':
            return self.export_entities_csv()
        if self.parser['export'] == 'csvNetwork':
            return self.export_csv_for_network_analysis()
        result = self.get_entity_formatted()
        if (self.parser['format']
                in app.config['RDF_FORMATS']):  # pragma: no cover
            return Response(
                self.rdf_output(result),
                mimetype=app.config['RDF_FORMATS'][self.parser['format']])
        template = linked_places_template(self.parser)
        if self.parser['format'] in ['geojson', 'geojson-v2']:
            template = geojson_collection_template()
        if self.parser['format'] == 'loud':
            template = loud_template(result)
        if self.parser['download']:
            return download(result, template)
        return marshal(result, template), 200

    def get_entity_formatted(self) -> dict[str, Any]:
        if self.parser['format'] == 'geojson':
            return self.get_geojson()
        if self.parser['format'] == 'geojson-v2':
            return self.get_geojson_v2()
        entity = self.entities[0]
        entity_dict = {
            'entity': entity,
            'links': ApiEntity.get_links_of_entities(entity.id),
            'links_inverse': ApiEntity.get_links_of_entities(
                entity.id, inverse=True)}
        if self.parser['format'] == 'loud' \
                or self.parser['format'] in app.config['RDF_FORMATS']:
            return get_loud_entities(entity_dict, parse_loud_context())
        return get_linked_places_entity(entity_dict, self.parser)

    def filter_by_type(self, ids: list[int]) -> list[Entity]:
        result = []
        for entity in self.entities:
            if any(id_ in [key.id for key in entity.types] for id_ in ids):
                result.append(entity)
        return result

    def parameter_validation(self) -> list[dict[str, Any]]:
        try:
            parameters = \
                [ast.literal_eval(item) for item in self.parser['search']]
        except Exception as e:
            raise InvalidSearchSyntax from e
        for param in parameters:
            for search_key, value_list in param.items():
                for values in value_list:
                    values['logicalOperator'] = \
                        values.get('logicalOperator') or 'or'
                    if values['logicalOperator'] \
                            not in app.config['LOGICAL_OPERATOR']:
                        raise LogicalOperatorError
                    if (values['operator'] not in
                            app.config['COMPARE_OPERATORS']):
                        raise OperatorError
                    if not values["values"]:
                        raise NoSearchStringError
                    if search_key not in app.config['VALID_VALUES']:
                        raise SearchValueError
                    if search_key in app.config['INT_VALUES']:
                        for value in values['values']:
                            if not isinstance(value, int):
                                raise ValueNotIntegerError
        return parameters

    def export_entities_csv(self) -> Response:
        frames = \
            [build_entity_dataframe(e, relations=True) for e in self.entities]
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
                     + self.link_parser_check_inverse())]
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
                [build_entity_dataframe(entity) for entity in entities_]
        return grouped_entities

    def link_parser_check(self) -> list[Link]:
        if any(i in ['relations', 'types', 'depictions', 'links', 'geometry']
               for i in self.parser['show']):
            return Entity.get_links_of_entities(
                [entity.id for entity in self.entities],
                self.get_properties_for_links())
        return []

    def link_parser_check_inverse(self) -> list[Link]:
        if any(i in ['relations', 'types', 'depictions', 'links', 'geometry']
               for i in self.parser['show']):
            return Entity.get_links_of_entities(
                [entity.id for entity in self.entities],
                self.get_properties_for_links(),
                inverse=True)
        return []

    def get_properties_for_links(self) -> Optional[list[str]]:
        if self.parser['relation_type']:
            codes = self.parser['relation_type']
            if 'geometry' in self.parser['show']:
                codes.append('P53')
            if 'types' in self.parser['show']:
                codes.append('P2')
            if any(i in ['depictions', 'links'] for i in self.parser['show']):
                codes.append('P67')
            return codes
        return None

    def sorting(self) -> None:
        if 'latest' in request.path:
            return
        self.entities = sorted(
            self.entities,
            key=lambda entity: self.get_key(entity),
            reverse=bool(self.parser['sort'] == 'desc'))

    def get_key(self, entity: Entity) -> datetime64 | str:
        if self.parser['column'] == 'cidoc_class':
            return entity.cidoc_class.name
        if self.parser['column'] == 'system_class':
            return entity.class_.name
        if self.parser['column'] in [
            'begin_from', 'begin_to', 'end_from', 'end_to']:
            if not getattr(entity, self.parser['column']):
                date = ("-" if self.parser["sort"] == 'desc' else "") \
                       + '9999999-01-01T00:00:00'
                return numpy.datetime64(date)
        return getattr(entity, self.parser['column'])

    def remove_duplicate_entities(self) -> None:
        seen: set[int] = set()
        # Do not change, faster than always call seen.add()
        seen_add = seen.add
        self.entities = \
            [e for e in self.entities if not (e.id in seen or seen_add(e.id))]

    def get_json_output(self) -> dict[str, Any]:
        total = [e.id for e in self.entities]
        count = len(total)
        self.parser['limit'] = count \
            if self.parser['limit'] == 0 else self.parser['limit']
        e_list = list(
            itertools.islice(total, 0, None, int(self.parser['limit'])))
        index = [{'page': num + 1, 'startId': i} for num, i in
                 enumerate(e_list)]
        if index:
            self.parser['first'] = self.get_by_page(index) \
                if self.parser['page'] else self.parser['first']
        total = self.get_start_entity(total) \
            if self.parser['last'] or self.parser['first'] else total
        j = [i for i, x in enumerate(self.entities) if x.id == total[0]]
        formatted_entities = []
        if self.entities:
            self.entities = [e for idx, e in enumerate(self.entities[j[0]:])]
            formatted_entities = self.get_entities_formatted()
        return {
            "results": formatted_entities,
            "pagination": {
                'entitiesPerPage': int(self.parser['limit']),
                'entities': count,
                'index': index,
                'totalPages': len(index)}}

    def get_by_page(self, index: list[dict[str, Any]]) -> dict[str, Any]:
        page = self.parser['page'] \
            if self.parser['page'] < index[-1]['page'] else index[-1]['page']
        return \
            [entry['startId'] for entry in index if entry['page'] == page][0]

    def get_start_entity(self, total: list[int]) -> list[Any]:
        if self.parser['first'] and int(self.parser['first']) in total:
            return list(itertools.islice(
                total,
                total.index(int(self.parser['first'])),
                None))
        if self.parser['last'] and int(self.parser['last']) in total:
            if not (out := list(itertools.islice(
                    total,
                    total.index(int(self.parser['last'])) + 1,
                    None))):
                raise LastEntityError
            return out
        raise EntityDoesNotExistError

    def get_entities_formatted(self) -> list[dict[str, Any]]:
        self.entities = self.entities[:int(self.parser['limit'])]
        if self.parser['format'] == 'geojson':
            return [self.get_geojson()]
        if self.parser['format'] == 'geojson-v2':
            return [self.get_geojson_v2()]
        entities_dict: dict[int, dict[str, Any]] = {}
        for entity in self.entities:
            entities_dict[entity.id] = {
                'entity': entity,
                'links': [],
                'links_inverse': []}
        for link_ in self.link_parser_check():
            entities_dict[link_.domain.id]['links'].append(link_)
        for link_ in self.link_parser_check_inverse():
            entities_dict[link_.range.id]['links_inverse'].append(link_)
        if self.parser['format'] == 'loud' \
                or self.parser['format'] in app.config['RDF_FORMATS']:
            return [get_loud_entities(item, parse_loud_context())
                    for item in entities_dict.values()]
        return [get_linked_places_entity(item, self.parser)
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
            if geoms := [self.get_geojson_dict(entity, geom)
                         for geom in self.get_geom(entity)]:
                out.extend(geoms)
            else:
                out.append(self.get_geojson_dict(entity))
        return {'type': 'FeatureCollection', 'features': out}

    def get_geom(self, entity: Entity, ) -> list[Any]:
        if entity.class_.view == 'place' or entity.class_.name == 'artifact':
            id_ = entity.get_linked_entity_safe('P53').id
            geoms = Gis.get_by_id(id_)
            if self.parser['centroid']:
                geoms.extend(Gis.get_centroids_by_id(id_))
            return geoms
        if entity.class_.name == 'object_location':
            geoms = Gis.get_by_id(entity.id)
            if self.parser['centroid']:
                geoms.extend(Gis.get_centroids_by_id(entity.id))
            return geoms
        return []

    def get_geojson_dict(
            self,
            entity: Entity,
            geom: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        return replace_empty_list_values_in_dict_with_none({
            'type': 'Feature',
            'geometry': geom,
            'properties': {
                '@id': entity.id,
                'systemClass': entity.class_.name,
                'viewClass': entity.class_.view,
                'name': entity.name,
                'description': entity.description
                if 'description' in self.parser['show'] else None,
                'begin_earliest': entity.begin_from
                if 'when' in self.parser['show'] else None,
                'begin_latest': entity.begin_to
                if 'when' in self.parser['show'] else None,
                'begin_comment': entity.begin_comment
                if 'when' in self.parser['show'] else None,
                'end_earliest': entity.end_from
                if 'when' in self.parser['show'] else None,
                'end_latest': entity.end_to
                if 'when' in self.parser['show'] else None,
                'end_comment': entity.end_comment
                if 'when' in self.parser['show'] else None,
                'types': [{
                    'typeName': type_.name,
                    'typeId': type_.id,
                    'typeHierarchy': ' > '.join(
                        map(str, [g.types[root].name for root in type_.root]))}
                    for type_ in entity.types]
                if 'types' in self.parser['show'] else None}})

    def get_geojson_v2(self) -> dict[str, Any]:
        out = []
        links = [link_ for link_ in self.link_parser_check()
                 if link_.property.code
                 in ['P53', 'P74', 'OA8', 'OA9', 'P7', 'P26', 'P27']]
        for entity in self.entities:
            entity_links = [
                link_ for link_ in links if link_.domain.id == entity.id]
            if entity.class_.view == 'place':
                entity.types.update(
                    get_location_link(entity_links).range.types)
            if geom := self.get_geoms_as_collection(
                    entity,
                    [l_.range.id for l_ in entity_links]):
                out.append(self.get_geojson_dict(entity, geom))
        return {'type': 'FeatureCollection', 'features': out}

    def get_geoms_as_collection(
            self,
            entity: Entity,
            links: list[int]) -> Optional[dict[str, Any]]:
        if entity.class_.name == 'object_location':
            geoms: list[Any] = Gis.get_by_id(entity.id)
            if self.parser['centroid']:
                geoms.extend(Gis.get_centroids_by_id(entity.id))
            return get_geoms_dict(geoms)
        if links:
            geoms = [Gis.get_by_id(id_) for id_ in links]
            if self.parser['centroid']:
                geoms.extend([Gis.get_centroids_by_id(id_) for id_ in links])
            return get_geoms_dict(flatten_list_and_remove_duplicates(geoms))
        return None

    def rdf_output(
            self,
            data: list[dict[str, Any]] | dict[str, Any]) \
            -> Any:  # pragma: nocover
        os.environ['http_proxy'] = app.config['API_PROXY']
        os.environ['https_proxy'] = app.config['API_PROXY']
        graph = Graph().parse(data=json.dumps(data), format='json-ld')
        return graph.serialize(format=self.parser['format'], encoding='utf-8')

    def get_entities_template(self) -> dict[str, Any]:
        if self.parser['format'] in ['geojson', 'geojson-v2']:
            return geojson_pagination()
        if self.parser['format'] == 'loud':
            return loud_pagination()
        return linked_place_pagination(self.parser)
