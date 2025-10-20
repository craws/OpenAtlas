from __future__ import annotations

import os
from typing import Any, Iterator

from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

from openatlas import app
from openatlas.api.resources.resolve_endpoints import get_loud_context

_linked_art_context = get_loud_context()


def _set_proxies() -> None:  # pragma: no cover
    if 'http' in app.config['PROXIES']:
        os.environ['http_proxy'] = app.config['PROXIES']['http']
    if 'https' in app.config['PROXIES']:
        os.environ['https_proxy'] = app.config['PROXIES']['https']


def _add_namespaces(graph: Graph, context: dict[str, Any]) -> None:
    for prefix, uri in context["@context"].items():
        if isinstance(uri, str):
            if uri.endswith('/') or uri.endswith('#'):
                graph.bind(prefix, Namespace(uri))  # type: ignore


def _resolve_predicate(key: str) -> URIRef | None:
    context_entry = _linked_art_context["@context"].get(key)

    if isinstance(context_entry, dict) and "@id" in context_entry:
        predicate_uri_string = context_entry["@id"]
    else:
        predicate_uri_string = key

    if ":" in predicate_uri_string:
        prefix, localname = predicate_uri_string.split(":", 1)
        prefix_uri = _linked_art_context["@context"].get(prefix)
        if isinstance(prefix_uri, str):
            return URIRef(prefix_uri + localname)

    return URIRef(predicate_uri_string)


def _get_subject(
        data: dict[str, Any],
        graph: Graph,
        parent_subject: URIRef | BNode | None = None,
        parent_predicate: URIRef | None = None) -> URIRef | BNode:
    subject_uri = data.get("id")
    if subject_uri:
        return URIRef(subject_uri)

    subject = BNode()  # type: ignore
    if parent_subject is not None and parent_predicate is not None:
        graph.add((parent_subject, parent_predicate, subject))
    return subject


def _handle_value(
        graph: Graph,
        subject: URIRef | BNode,
        predicate: URIRef,
        value: list[dict[str, Any]] | dict[str, Any] | Any) -> None:
    if isinstance(value, dict):
        object_uri = value.get("id")
        if object_uri:
            graph.add((subject, predicate, URIRef(object_uri)))
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, dict) and item.get("id"):
                graph.add((subject, predicate, URIRef(item["id"])))
            elif isinstance(item, dict):
                continue
            else:
                graph.add((subject, predicate, Literal(item)))
    else:
        graph.add((subject, predicate, Literal(value)))


def _add_triples_from_linked_art(
        graph: Graph,
        data: list[dict[str, Any]] | dict[str, Any],
        parent_subject: URIRef | BNode | None = None,
        parent_predicate: URIRef | None = None) -> None:
    if not isinstance(data, dict):  # pragma: no cover - mypy
        return

    subject = _get_subject(data, graph, parent_subject, parent_predicate)

    if data.get("type"):
        type_val = data["type"]

        context_entry = _linked_art_context["@context"].get(type_val)
        if isinstance(context_entry, dict) and "@id" in context_entry:
            full_type_uri = context_entry["@id"]
        elif isinstance(context_entry, str):  # pragma: no cover
            full_type_uri = context_entry
        else:  # pragma: no cover
            if (type_val.startswith("http://")
                    or type_val.startswith("https://")):
                full_type_uri = type_val
            else:
                la_base = (_linked_art_context["@context"].get("la")
                           or "https://linked.art/ns/terms/")
                full_type_uri = f"{la_base}{type_val}"

        graph.add((subject, RDF.type, URIRef(full_type_uri)))


    for key, value in data.items():
        if key in {"id", "type", "@context"}:
            continue

        predicate = _resolve_predicate(key)
        if not predicate:  # pragma: no cover - mypy
            continue

        _handle_value(graph, subject, predicate, value)

        if isinstance(value, dict) and not value.get("id"):
            _add_triples_from_linked_art(graph, value, subject, predicate)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and not item.get("id"):
                    _add_triples_from_linked_art(
                        graph,
                        item,
                        subject,
                        predicate)


def rdf_output(data: Iterator[dict[str, Any]], format_: str) -> Any:
    _set_proxies()
    graph = Graph()
    _add_namespaces(graph, _linked_art_context)
    for item in data:
        _add_triples_from_linked_art(graph, item)
    return graph.serialize(format=format_, encoding='utf-8')


def rdf_export_to_file(
        data: Iterator[dict[str, Any]],
        rdf_export_path: str) -> str:
    _set_proxies()
    with open(rdf_export_path, 'wb') as output_file:
        for item in data:
            temp_graph = Graph()
            _add_triples_from_linked_art(temp_graph, item)
            for triple in temp_graph.serialize(format='nt').splitlines():
                if triple:
                    output_file.write(triple.encode('utf-8') + b'\n')
    return rdf_export_path
