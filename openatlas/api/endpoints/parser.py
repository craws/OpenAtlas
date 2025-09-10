from __future__ import annotations

import ast
import itertools
from typing import Any, Optional

import numpy
import validators
from flask import g, url_for
from numpy import datetime64
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

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

    #def rdf_output(
    #        self,
    #        data: list[dict[str, Any]] | dict[str, Any]) \
    #        -> Any:  # pragma: nocover
    #    if 'http' in app.config['PROXIES']:
    #        os.environ['http_proxy'] = app.config['PROXIES']['http']
    #    if 'https' in app.config['PROXIES']:
    #        os.environ['https_proxy'] = app.config['PROXIES']['https']
    #    graph = Graph().parse(data=json.dumps(data), format='json-ld')
    #    return graph.serialize(format=self.format, encoding='utf-8')


    def is_valid_url(self) -> None:
        if self.url and isinstance(
                validators.url(self.url),
                validators.ValidationFailure):
            raise UrlNotValid(self.url)

    def _add_namespaces(self, graph: Graph, context: dict):
        """
        Adds namespaces from the @context block to the RDF graph.
        """
        for prefix, uri in context["@context"].items():
            if isinstance(uri, str):
                if uri.endswith('/') or uri.endswith('#'):
                    graph.bind(prefix, Namespace(uri))

    def _add_triples_from_linked_art(self, graph: Graph, data: dict, parent_subject=None, parent_predicate=None):
        """
        Recursively processes a Linked Art JSON-LD dictionary and adds triples to the graph.
        """
        if isinstance(data, list):
            for item in data:
                self._add_triples_from_linked_art(graph, item, parent_subject, parent_predicate)
            return

        if not isinstance(data, dict):
            return

        subject_uri = data.get('id')
        if not subject_uri:
            # If no id, it's a blank node
            subject = BNode()
            if parent_subject and parent_predicate:
                graph.add((parent_subject, parent_predicate, subject))
        else:
            subject = URIRef(subject_uri)

        # Add the type triple for the current subject
        if data.get('type'):
            graph.add((subject, RDF.type, URIRef(data.get('type'))))

        for key, value in data.items():
            if key in ['id', 'type', '@context', 'results']:
                continue

            # Determine the predicate
            predicate = None
            if key in linked_art_context["@context"]:
                context_entry = linked_art_context["@context"][key]
                if isinstance(context_entry, str):
                    predicate = URIRef(context_entry)
                elif isinstance(context_entry, dict) and '@id' in context_entry:
                    predicate_uri_string = context_entry['@id']
                    if ':' in predicate_uri_string:
                        prefix, localname = predicate_uri_string.split(':', 1)
                        prefix_uri = linked_art_context["@context"].get(prefix)
                        if isinstance(prefix_uri, str):
                             predicate = URIRef(prefix_uri + localname)
                        else:
                            print(f"Warning: Could not resolve prefix '{prefix}' for key '{key}'")
                    else:
                        predicate = URIRef(predicate_uri_string)
            elif ':' in key:
                prefix, localname = key.split(':', 1)
                context_uri = linked_art_context["@context"].get(prefix)
                if isinstance(context_uri, str):
                    predicate = URIRef(context_uri + localname)
                elif isinstance(context_uri, dict):
                    predicate = URIRef(context_uri['@id'] + localname)
                else:
                    print(f"Warning: Unknown prefix '{prefix}' for key '{key}'")
            else:
                print(f"Warning: Cannot resolve local property '{key}' without a prefix.")

            if not predicate:
                continue



            if isinstance(value, dict):
                object_uri = value.get('id')
                if object_uri:
                    graph.add((subject, predicate, URIRef(object_uri)))
                    self._add_triples_from_linked_art(graph, value)
                else:
                    # This is an inline object (blank node).
                    # The recursive call will handle adding triples from it.
                    # No need to add a triple here, it will be added when the new subject is created.
                    self._add_triples_from_linked_art(graph, value, subject, predicate)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        object_uri = item.get('id')
                        if object_uri:
                            graph.add((subject, predicate, URIRef(object_uri)))
                            self._add_triples_from_linked_art(graph, item)
                        else:
                            # This is an inline object (blank node) in a list.
                            # The recursive call will handle adding triples from it.
                            self._add_triples_from_linked_art(graph, item, subject, predicate)
                    else:
                        graph.add((subject, predicate, Literal(item)))
            else:
                graph.add((subject, predicate, Literal(value)))
    # todo: move the rdf functions away from parser to own file
    # todo: go through each step and clean up
    #   fix part_of issue
    #   make linked art context better available, maybe with g.?

    def rdf_output(self, data: list[dict[str, Any]] | dict[str, Any]) -> Any:
        """
        Manually parses JSON-LD data and serializes it to an RDF graph.
        """
        graph = Graph()
        self._add_namespaces(graph, linked_art_context)

        # Handle the 'results' key if it exists
        if isinstance(data, dict) and 'results' in data:
            data = data['results']

        self._add_triples_from_linked_art(graph, data)

        # The existing function part for proxies and serialization.
        # if 'http' in app.config['PROXIES']:
        #     os.environ['http_proxy'] = app.config['PROXIES']['http']
        # if 'https' in app.config['PROXIES']:
        #     os.environ['https_proxy'] = app.config['PROXIES']['https']

        return graph.serialize(format=self.format, encoding='utf-8')

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
