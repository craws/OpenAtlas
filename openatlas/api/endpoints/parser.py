from __future__ import annotations

import ast
import itertools
import json
import os
from typing import Any, Optional

import numpy
import validators
from flask import g, url_for
from numpy import datetime64
from rdflib import Graph

from openatlas import app
from openatlas.api.formats.linked_places import (
    get_lp_file, get_lp_links, get_lp_time)
from openatlas.api.resources.error import (
    EntityDoesNotExistError, InvalidSearchSyntax, InvalidSearchValueError,
    LastEntityError, UrlNotValid)
from openatlas.api.resources.search import (
    get_search_values, search_entity, value_to_be_searched)
from openatlas.api.resources.search_validation import (
    check_if_date_search, check_search_parameters)
from openatlas.api.resources.templates import (
    geojson_pagination, linked_place_pagination, loud_pagination)
from openatlas.api.resources.util import (
    flatten_list_and_remove_duplicates, get_geometric_collection,
    get_geoms_dict, get_location_link, get_reference_systems,
    replace_empty_list_values_in_dict_with_none)
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis


class Parser:
    download = None
    count = None
    locale = None
    sort = None
    column: str = ''
    search: str = ''
    search_param: list[dict[str, Any]]
    limit: int = 0
    first = None
    last = None
    page = None
    show: list[str]
    export = None
    format = None
    type_id: list[int]
    relation_type = None
    centroid = None
    geometry = None
    entities = None
    linked_entities = None
    cidoc_classes = None
    view_classes = None
    system_classes = None
    image_size = None
    file_id = None
    exclude_system_classes: list[str]
    linked_to_ids: list[int]
    url = None

    def __init__(self, parser: dict[str, Any]):
        self.show = []
        self.type_id = []
        self.exclude_system_classes = []
        self.search_param = []
        for item in parser:
            setattr(self, item, parser[item])
        if self.search:
            self.set_search_param()
        self.is_valid_url()
        if self.url and not self.url.endswith('/'):
            self.url += '/'

    def set_search_param(self) -> None:
        try:
            url_parameters = [ast.literal_eval(i) for i in self.search]
        except Exception as e:
            raise InvalidSearchSyntax from e
        for item in url_parameters:
            for category, value_list in item.items():
                for values in value_list:
                    values['logicalOperator'] = (
                        values.get('logicalOperator') or 'or')
                    check_search_parameters(category, values)
                    if check_if_date_search(category):
                        try:
                            values["values"] = [
                                numpy.datetime64(values["values"][0])]
                        except ValueError as e:
                            raise InvalidSearchValueError(
                                category,
                                values["values"]) from e

                    self.search_param.append({
                        "search_values": get_search_values(
                            category,
                            values),
                        "logical_operator": values['logicalOperator'],
                        "operator": 'equal' if category == "valueTypeID"
                        else values['operator'],
                        "category": category,
                        "is_date": check_if_date_search(category)})


    def search_filter(self, entity: Entity) -> bool:
        for i in self.search_param:
            if not search_entity(
                    entity_values=value_to_be_searched(entity, i['category']),
                    operator_=i['operator'],
                    search_values=i['search_values'],
                    logical_operator=i['logical_operator'],
                    is_comparable=i['is_date']):
                return False
        return True

    def get_properties_for_links(self) -> Optional[list[str]]:
        if self.relation_type:
            codes = self.relation_type
            if 'geometry' in self.show:
                codes.append('P53')
            if 'types' in self.show:
                codes.append('P2')
            if any(i in ['depictions', 'links'] for i in self.show):
                codes.append('P67')
            return codes
        return None

    def get_key(self, entity: Entity) -> datetime64 | str:
        if self.column == 'cidoc_class':
            return entity.cidoc_class.name
        if self.column == 'system_class':
            return entity.class_.name
        if self.column in ['begin_from', 'begin_to', 'end_from', 'end_to']:
            if not getattr(entity, self.column):
                date = ("-" if self.sort == 'desc' else "") \
                       + '9999999-01-01T00:00:00'
                return numpy.datetime64(date)
        return getattr(entity, self.column)

    def get_by_page(self, index: list[dict[str, Any]]) -> dict[str, Any]:
        page = (
            self.page) if self.page < index[-1]['page'] else index[-1]['page']
        return \
            [entry['startId'] for entry in index if entry['page'] == page][0]

    def get_start_entity(self, total: list[int]) -> list[Any]:
        if self.first and int(self.first) in total:
            return list(itertools.islice(
                total,
                total.index(int(self.first)),
                None))
        if self.last and int(self.last) in total:
            if not (out := list(itertools.islice(
                    total,
                    total.index(int(self.last)) + 1,
                    None))):
                raise LastEntityError
            return out
        raise EntityDoesNotExistError

    def get_geom(self, entity: Entity, ) -> list[Any]:
        if entity.class_.view == 'place' or entity.class_.name == 'artifact':
            id_ = entity.get_linked_entity_safe('P53').id
            geoms = Gis.get_by_id(id_)
            if self.centroid:
                if centroid_result := Gis.get_centroids_by_id(id_):
                    geoms.extend(centroid_result)
            return geoms
        if entity.class_.name == 'object_location':
            geoms = Gis.get_by_id(entity.id)
            if self.centroid:
                if centroid_result := Gis.get_centroids_by_id(entity.id):
                    geoms.extend(centroid_result)
            return geoms
        return []

    def get_linked_places_entity(
            self,
            entity_dict: dict[str, Any]) -> dict[str, Any]:
        entity = entity_dict['entity']
        links = entity_dict['links']
        links_inverse = entity_dict['links_inverse']
        return {
            'type': 'FeatureCollection',
            '@context': app.config['API_CONTEXT']['LPF'],
            'features': [replace_empty_list_values_in_dict_with_none({
                '@id': url_for('api.entity', id_=entity.id, _external=True),
                'type': 'Feature',
                'crmClass': f'crm:{entity.cidoc_class.code} '
                            f"{entity.cidoc_class.i18n['en']}",
                'viewClass': entity.class_.view,
                'systemClass': entity.class_.name,
                'properties': {'title': entity.name},
                'types': self.get_lp_types(entity, links)
                if 'types' in self.show else None,
                'depictions': get_lp_file(links_inverse)
                if 'depictions' in self.show else None,
                'when': {'timespans': [get_lp_time(entity)]}
                if 'when' in self.show else None,
                'links': get_reference_systems(links_inverse)
                if 'links' in self.show else None,
                'descriptions': [{'value': entity.description}]
                if 'description' in self.show else None,
                'names':
                    [{"alias": value} for value in entity.aliases.values()]
                    if entity.aliases and 'names' in self.show else None,
                'geometry': get_geometric_collection(
                    entity,
                    links,
                    self) if 'geometry' in self.show else None,
                'relations': get_lp_links(links, links_inverse, self)
                if 'relations' in self.show else None})]}

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
                if 'description' in self.show else None,
                'begin_earliest': entity.begin_from
                if 'when' in self.show else None,
                'begin_latest': entity.begin_to
                if 'when' in self.show else None,
                'begin_comment': entity.begin_comment
                if 'when' in self.show else None,
                'end_earliest': entity.end_from
                if 'when' in self.show else None,
                'end_latest': entity.end_to
                if 'when' in self.show else None,
                'end_comment': entity.end_comment
                if 'when' in self.show else None,
                'types': [{
                    'typeName': type_.name,
                    'typeId': type_.id,
                    'typeHierarchy': ' > '.join(
                        map(str, [g.types[root].name for root in type_.root]))}
                    for type_ in entity.types]
                if 'types' in self.show else None}})

    def get_geoms_as_collection(
            self,
            entity: Entity,
            links: list[int]) -> Optional[dict[str, Any]]:
        if entity.class_.name == 'object_location':
            geoms: list[Any] = Gis.get_by_id(entity.id)
            if self.centroid:
                if centroid_result := Gis.get_centroids_by_id(entity.id):
                    geoms.extend(centroid_result)
            return get_geoms_dict(geoms)
        if links:
            geoms = [Gis.get_by_id(id_) for id_ in links]
            if self.centroid:
                geoms.extend([Gis.get_centroids_by_id(id_) for id_ in links])
            return get_geoms_dict(flatten_list_and_remove_duplicates(geoms))
        return None

    def rdf_output(
            self,
            data: list[dict[str, Any]] | dict[str, Any]) \
            -> Any:  # pragma: nocover
        if 'http' in app.config['PROXIES']:
            os.environ['http_proxy'] = app.config['PROXIES']['http']
        if 'https' in app.config['PROXIES']:
            os.environ['https_proxy'] = app.config['PROXIES']['https']
        graph = Graph().parse(data=json.dumps(data), format='json-ld')
        return graph.serialize(format=self.format, encoding='utf-8')

    def get_entities_template(self) -> dict[str, Any]:
        if self.format in ['geojson', 'geojson-v2']:
            return geojson_pagination()
        if self.format == 'loud':
            return loud_pagination()
        return linked_place_pagination(self)

    def is_valid_url(self) -> None:
        if self.url and isinstance(
                validators.url(self.url),
                validators.ValidationFailure):
            raise UrlNotValid(self.url)

    @staticmethod
    def get_lp_types(
            entity: Entity,
            links: list[Link]) -> list[dict[str, Any]]:
        types = []
        if entity.class_.view == 'place':
            entity.types.update(get_location_link(links).range.types)
        for type_ in entity.types:
            type_dict = {
                'identifier': url_for(
                    'api.entity', id_=type_.id, _external=True),
                'descriptions': type_.description,
                'label': type_.name,
                'hierarchy': ' > '.join(map(
                    str,
                    [g.types[root].name for root in type_.root])),
                'typeHierarchy': [{
                    'label': g.types[root].name,
                    'descriptions': g.types[root].description,
                    'identifier': url_for(
                        'api.entity', id_=g.types[root].id, _external=True)}
                    for root in type_.root]}
            for link in links:
                if link.range.id == type_.id and link.description:
                    type_dict['value'] = link.description
                    if link.range.id == type_.id and type_.description:
                        type_dict['unit'] = type_.description
            types.append(type_dict)
        return types
