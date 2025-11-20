from __future__ import annotations

import ast
import itertools
from typing import Any, Optional

import numpy
import validators
from flask import g, url_for
from flask_babel import format_number

from openatlas import app
from openatlas.api.resources.error import (
    EntityDoesNotExistError, InvalidSearchSyntax, InvalidSearchValueError,
    LastEntityError, UrlNotValid)
from openatlas.api.resources.resolve_endpoints import get_loud_context
from openatlas.api.resources.search import get_search_values, search_entity
from openatlas.api.resources.search_validation import (
    check_if_date_search, validate_search_parameters)
from openatlas.api.resources.util import (
    flatten_list_and_remove_duplicates, geometry_to_geojson,
    get_location_link, get_value_for_types,
    replace_empty_list_values_in_dict_with_none)
from openatlas.display.table import file_preview
from openatlas.display.util2 import display_bool
from openatlas.models.dates import format_date
from openatlas.models.entity import Entity, Link

linked_art_context = get_loud_context()


class Parser:
    download = None
    count = None
    locale = None
    sort = None
    column: str = 'name'
    search: str = ''
    search_param: list[list[dict[str, Any]]]
    limit: int = 0
    first = None
    last = None
    page = None
    show: list[str]
    export = None
    format: str = ''
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
    table_columns = None
    exclude_system_classes: list[str]
    linked_to_ids: list[int]
    url: str = ''
    remove_empty_values = None
    depth: int = 1
    place_hierarchy = None
    map_overlay = None

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
        if self.map_overlay:
            self.map_overlay = parser['map_overlay'] == 'true'
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

    def get_key(self, e: Entity) -> str:
        key = ''
        match self.column:
            case 'begin_from' | 'begin_to' | 'end_from' | 'end_to':
                if not getattr(e.dates, self.column):
                    date = ("-" if self.sort == 'desc' else "") \
                           + '9999999-01-01T00:00:00'
                    key = str(date)
            case 'group' | 'cidoc_class':
                key = e.cidoc_class.name.lower()
            case 'class' | 'system_class':
                key = e.class_.label.lower()
            case 'created':
                key = format_date(e.created)
            case 'count':
                key = format_number(e.count)
            case 'content' | 'description':
                if e.description:
                    key = e.description.lower()
            case 'creator':
                if e.class_.name == 'file':
                    if g.file_info.get(e.id):
                        key = g.file_info[e.id]['creator']
            # case 'domain':
            #    key = e.name.lower()
            # case 'default_precision':
            #     if default_precision := next(iter(e.types), None):
            #         key = default_precision.name
            # case 'example_id' if isinstance(e, Entity):
            #         key = e.example_id or ''
            case 'extension':
                key = e.get_file_ext()
            case 'icon':
                key = file_preview(e.id)
            case 'license_holder':
                if e.class_.name == 'file':
                    if g.file_info.get(e.id):
                        key = g.file_info[e.id]['license_holder']
            case 'name':
                key = e.name.lower()
            case 'public':
                if e.class_.name == 'file':
                    if g.file_info.get(e.id):
                        key = display_bool(g.file_info[e.id]['public'])
            # case 'range':
            #     key = e.name.lower()
            case 'size':
                if e.class_.name == 'file':
                    key = e.get_file_size()
            case 'type' | 'license':
                if e.standard_type:
                    key = e.standard_type.name.lower()
            case _:
                key = str(getattr(e, self.column)).lower()
        return key

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
                'viewClass': entity.class_.group.get('name'),
                'name': entity.name,
                'description': entity.description
                if 'description' in self.show else None,
                'begin_earliest': entity.dates.begin_from
                if 'when' in self.show else None,
                'begin_latest': entity.dates.begin_to
                if 'when' in self.show else None,
                'begin_comment': entity.dates.begin_comment
                if 'when' in self.show else None,
                'end_earliest': entity.dates.end_from
                if 'when' in self.show else None,
                'end_latest': entity.dates.end_to
                if 'when' in self.show else None,
                'end_comment': entity.dates.end_comment
                if 'when' in self.show else None,
                'types': [{
                    'typeName': type_.name,
                    'typeId': type_.id,
                    'typeHierarchy': ' > '.join(
                        map(str, [g.types[root].name for root in type_.root]))}
                    for type_ in entity.types]
                if 'types' in self.show else None}})

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
        if entity.class_.group.get('name') == 'place':
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
