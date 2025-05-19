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
from openatlas.api.resources.search import get_search_values, search_entity
from openatlas.api.resources.search_validation import (
    check_if_date_search, validate_search_parameters)
from openatlas.api.resources.util import (
    flatten_list_and_remove_duplicates, geometry_to_geojson,
    get_location_link, get_reference_systems,
    get_value_for_types, replace_empty_list_values_in_dict_with_none)
from openatlas.models.entity import Entity, Link


class Parser:
    download = None
    count = None
    locale = None
    sort = None
    column: str = ''
    search: str = ''
    search_param: list[list[dict[str, Any]]]
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
    url: str = ''
    remove_empty_values = None
    depth: int = 1
    place_hierarchy = None

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
        if self.centroid:
            self.centroid = parser['centroid'] == 'true'
        if self.place_hierarchy:
            self.place_hierarchy = parser['place_hierarchy'] == 'true'
        if self.remove_empty_values:
            self.remove_empty_values = parser['remove_empty_values'] == 'true'

    def set_search_param(self) -> None:
        try:
            url_parameters = [ast.literal_eval(i) for i in self.search]
        except Exception as e:
            raise InvalidSearchSyntax from e
        for search in url_parameters:
            for category, value_list in search.items():
                for values in value_list:
                    values['logicalOperator'] = \
                        values.get('logicalOperator') or 'or'
                    validate_search_parameters(category, values)
                    if category in app.config['INT_VALUES']:
                        values['values'] = list(map(int, values['values']))
                    if check_if_date_search(category):
                        try:
                            values["values"] = [
                                numpy.datetime64(values["values"][0])]
                        except ValueError as e:
                            raise InvalidSearchValueError(
                                category,
                                values["values"]) from e

        for search in url_parameters:
            search_parameter = []
            for category, value_list in search.items():
                for values in value_list:
                    links = []
                    is_comparable = check_if_date_search(category)
                    if category == 'valueTypeID':
                        is_comparable = True
                        for value in values["values"]:
                            links.append(
                                Entity.get_links_of_entities(
                                    value[0],
                                    inverse=True))
                    search_parameter.append({
                        "search_values": get_search_values(category, values),
                        "logical_operator": values['logicalOperator'],
                        "operator": values['operator'],
                        "category": category,
                        "is_comparable": is_comparable,
                        "value_type_links":
                            flatten_list_and_remove_duplicates(links)})
            self.search_param.append(search_parameter)

    def search_filter(self, entity: Entity) -> bool:
        found = False
        for set_of_param in self.search_param:
            for param in set_of_param:
                if not search_entity(entity, param):
                    found = False
                    break
                found = True
            if found:
                return True
        return found

    def get_properties_for_links(self) -> list[str]:
        codes: list[str] = []
        if self.relation_type:
            codes = self.relation_type + ['P53']
            if 'geometry' in self.show:
                codes.extend(['P53', 'P74', 'OA8', 'OA9', 'P7', 'P26', 'P27'])
            if 'types' in self.show:
                codes.append('P2')
            if any(i in ['depictions', 'links'] for i in self.show):
                codes.append('P67')
        return codes

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

    def get_by_page(
            self,
            index: list[dict[str, Any]]) -> dict[str, Any] | None:
        if not index or not self.page:
            return None
        target_page = min(int(self.page), int(index[-1]['page']))
        for entry in index:
            if entry.get('page') == target_page:
                return entry.get('startId')
        return None  # pragma: no cover

    def set_start_entity(self, total: list[int]) -> list[Any]:
        if self.first and int(self.first) in total:
            return list(
                itertools.islice(
                    total,
                    total.index(int(self.first)),
                    None))
        if self.last and int(self.last) in total:
            if not (
                    out := list(itertools.islice(
                        total,
                        total.index(int(self.last)) + 1,
                        None))):
                raise LastEntityError
            return out
        raise EntityDoesNotExistError

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
                'geometry': geometry_to_geojson(entity_dict['geometry'])
                if 'geometry' in self.show else None,
                'relations': get_lp_links(links, links_inverse, self)
                if 'relations' in self.show else None})]}

    def get_geojson_dict(
            self,
            entity_dict: dict[str, Any],
            geometry: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        entity = entity_dict['entity']
        geoms = geometry or geometry_to_geojson(entity_dict['geometry'])
        return replace_empty_list_values_in_dict_with_none({
            'type': 'Feature',
            'geometry': geoms,
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
            type_dict.update(get_value_for_types(type_, links))
            types.append(type_dict)
        return types
