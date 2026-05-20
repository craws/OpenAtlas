from __future__ import annotations

import logging
import os
import re
from functools import lru_cache
from typing import Any, Iterator
from urllib.parse import quote

from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import XSD

from openatlas import app
from openatlas.api.resources.resolve_endpoints import get_loud_context


class _SuppressYearBeforeCommonEraWarning(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover
        message = record.getMessage()
        if record.exc_info is None:
            return True
        _error_type, error_payload, _error_traceback = record.exc_info
        should_suppress = (
                message.startswith(
                    'Failed to convert Literal lexical form to value')
                and "Invalid isoformat string: '-" in str(error_payload))
        return not should_suppress


logging.getLogger('rdflib.term').addFilter(
    _SuppressYearBeforeCommonEraWarning())

_CONTEXT: dict[str, Any] = get_loud_context().get('@context', {})

_DEFAULT_NAMESPACES: dict[str, str] = {
    'crm': 'http://www.cidoc-crm.org/cidoc-crm/',
    'la': 'https://linked.art/ns/terms/',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'geo': 'http://www.opengis.net/ont/geosparql#',
    'archaeo': 'http://www.cidoc-crm.org/extensions/crmarchaeo/'}

_GEO = Namespace('http://www.opengis.net/ont/geosparql#')

_RESERVED_KEYS: frozenset[str] = frozenset({'id', 'type', '@context'})

_OWN_URI_MARKERS: tuple[str, ...] = (
    '/api/uuid/',
    '/api/entity/',
    '/api/generated/')


def _is_own_uri(uri: str) -> bool:
    return any(marker in uri for marker in _OWN_URI_MARKERS)


_DATE_RE = re.compile(r'^-?\d{4}-\d{2}-\d{2}$')
_DATETIME_RE = re.compile(
    r'^-?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
    r'(\.\d+)?(Z|[+-]\d{2}:\d{2})?$')
_GYEARMONTH_RE = re.compile(r'^-?\d{4}-\d{2}$')
_GYEAR_RE = re.compile(r'^-?\d{4}$')

_WKT_RE = re.compile(
    r'^\s*(POINT|LINESTRING|POLYGON|MULTIPOINT|MULTILINESTRING|'
    r'MULTIPOLYGON|GEOMETRYCOLLECTION)\s*[ZM]?\s*\(',
    re.IGNORECASE)


def _typed_literal(value: Any) -> Literal:
    if isinstance(value, str):
        if _DATE_RE.match(value):
            return Literal(value, datatype=XSD.date)
        if _DATETIME_RE.match(value):  # pragma: no cover
            return Literal(value, datatype=XSD.dateTime)
        if _GYEARMONTH_RE.match(value):  # pragma: no cover
            return Literal(value, datatype=XSD.gYearMonth)
        if _GYEAR_RE.match(value):  # pragma: no cover
            return Literal(value, datatype=XSD.gYear)
        if _WKT_RE.match(value):
            return Literal(value, datatype=_GEO.wktLiteral)
    return Literal(value)


def _set_proxies() -> None:  # pragma: no cover
    for scheme in ('http', 'https'):
        if scheme in app.config['PROXIES']:
            os.environ[f'{scheme}_proxy'] = app.config['PROXIES'][scheme]


def _bind_namespaces(graph: Graph) -> None:
    for prefix, uri in _CONTEXT.items():
        if isinstance(uri, str) and uri.endswith(('/', '#')):
            graph.bind(prefix, Namespace(uri))
    for prefix, uri in _DEFAULT_NAMESPACES.items():
        graph.bind(prefix, Namespace(uri))


@lru_cache(maxsize=None)
def _expand_curie(curie: str) -> str:
    if ':' not in curie:
        return curie  # pragma: no cover
    prefix, local = curie.split(':', 1)
    base = _CONTEXT.get(prefix)
    if isinstance(base, str):
        return base + local
    return curie  # pragma: no cover


def _entry_uri(entry: Any) -> str | None:
    if isinstance(entry, dict) and '@id' in entry:
        return _expand_curie(entry['@id'])
    if isinstance(entry, str):  # pragma: no cover
        return _expand_curie(entry)
    return None


@lru_cache(maxsize=None)
def _resolve_predicate(
        key: str,
        data_type: str | None) -> URIRef | None:
    if data_type:
        type_entry = _CONTEXT.get(data_type)
        if isinstance(type_entry, dict):
            sub_context = type_entry.get('@context')
            if isinstance(sub_context, dict) and key in sub_context:
                if uri := _entry_uri(sub_context[key]):
                    return URIRef(uri)
    if uri := _entry_uri(_CONTEXT.get(key)):
        return URIRef(uri)
    return None  # pragma: no cover


@lru_cache(maxsize=None)
def _resolve_type_uri(data_type: str) -> str | None:
    if ':' in data_type:
        return _expand_curie(data_type)  # pragma: no cover
    entry = _CONTEXT.get(data_type)
    if isinstance(entry, dict) and '@id' in entry:
        return _expand_curie(entry['@id'])
    # pragma: no cover
    la_base = _CONTEXT.get('la') or 'https://linked.art/ns/terms/'
    return la_base + data_type


def _uri_ref(uri: str) -> URIRef:
    return URIRef(quote(uri, safe=':/#'))


def _emit_value(
        graph: Graph,
        subject: URIRef | BNode,
        predicate: URIRef,
        value: Any,
        entity_id: str | None = None) -> None:
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                if object_id := item.get('id'):
                    target = _uri_ref(str(object_id))
                    graph.add((subject, predicate, target))
                    if _is_own_uri(str(object_id)):
                        _expand_into(graph, target, item, entity_id)
                else:
                    bnode = BNode()
                    graph.add((subject, predicate, bnode))
                    _expand_into(graph, bnode, item, entity_id)
            else:  # pragma: no cover
                graph.add((subject, predicate, _typed_literal(item)))
        return
    if isinstance(value, dict):
        if object_id := value.get('id'):
            target = _uri_ref(str(object_id))
            graph.add((subject, predicate, target))
            if _is_own_uri(str(object_id)):
                _expand_into(graph, target, value, entity_id)
        return
    graph.add((subject, predicate, _typed_literal(value)))


def _expand_into(
        graph: Graph,
        subject: URIRef | BNode,
        data: dict[str, Any],
        entity_id: str | None = None) -> None:
    data_type = data.get('type')
    if data_type and (type_uri := _resolve_type_uri(str(data_type))):
        graph.add((subject, RDF.type, URIRef(type_uri)))
    for key, value in data.items():
        if key in _RESERVED_KEYS:
            continue
        if predicate := _resolve_predicate(key, data_type):
            _emit_value(graph, subject, predicate, value, entity_id)


def _add_entity(graph: Graph, data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        return  # pragma: no cover
    subject_id = data.get('id')
    if subject_id:
        subject: URIRef | BNode = _uri_ref(str(subject_id))
    else:  # pragma: no cover
        subject = BNode()
    _expand_into(graph, subject, data, subject_id)


def rdf_output(data: Iterator[dict[str, Any]], format_: str) -> Any:
    _set_proxies()
    graph = Graph()
    _bind_namespaces(graph)
    for item in data:
        _add_entity(graph, item)
    return graph.serialize(format=format_, encoding='utf-8')


def rdf_export_to_file(
        data: Iterator[dict[str, Any]],
        rdf_export_path: str) -> str:
    _set_proxies()
    with open(rdf_export_path, 'wb') as output_file:
        for item in data:
            graph = Graph()
            _add_entity(graph, item)
            output_file.write(graph.serialize(format='nt', encoding='utf-8'))
    return rdf_export_path
