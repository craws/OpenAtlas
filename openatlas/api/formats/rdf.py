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
                graph.bind(prefix, Namespace(uri))

    graph.bind("crm", Namespace("http://www.cidoc-crm.org/cidoc-crm/"))
    graph.bind("la", Namespace("https://linked.art/ns/terms/"))
    graph.bind("rdfs", Namespace("http://www.w3.org/2000/01/rdf-schema#"))
    graph.bind("rdf", Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"))


def _expand_curie(curie: str) -> str:  # pragma: no cover
    if ":" not in curie:
        return curie
    ctx = _linked_art_context.get("@context", {})
    prefix, local = curie.split(":", 1)
    base = ctx.get(prefix)
    if isinstance(base, str):
        return base + local
    return curie


def _resolve_predicate(
        key: str,
        data_type: str | None = None) -> URIRef | None:  # pragma: no cover
    ctx = _linked_art_context.get("@context", {})

    if data_type and data_type in ctx:
        type_data = ctx[data_type]
        if isinstance(type_data, dict):
            tctx = type_data.get("@context")
            if isinstance(tctx, dict) and key in tctx:
                entry = tctx[key]
                if isinstance(entry, dict) and "@id" in entry:
                    return URIRef(_expand_curie(entry["@id"]))
                if isinstance(entry, str):
                    return URIRef(_expand_curie(entry))

    entry = ctx.get(key)
    if isinstance(entry, dict) and "@id" in entry:
        return URIRef(_expand_curie(entry["@id"]))
    if isinstance(entry, str):
        return URIRef(_expand_curie(entry))

    return None


def _get_subject(
        data: dict[str, Any],
        graph: Graph,
        parent_subject: URIRef | BNode | None = None,
        parent_predicate: URIRef | None = None) -> URIRef | BNode:
    subject_uri = data.get("id")
    if subject_uri:
        return URIRef(subject_uri)

    subject = BNode()
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
            else:  # pragma: no cover
                graph.add((subject, predicate, Literal(item)))
    else:
        graph.add((subject, predicate, Literal(value)))


def _add_triples_from_linked_art(
        graph: Graph,
        data: list[dict[str, Any]] | dict[str, Any],
        parent_subject: URIRef | BNode | None = None,
        parent_predicate: URIRef | None = None) -> None:  # pragma: no cover
    if not isinstance(data, dict):  # pragma: no cover - mypy
        return

    subject = _get_subject(data, graph, parent_subject, parent_predicate)

    data_type = data.get("type")
    if data_type:
        ctx = _linked_art_context.get("@context", {})
        type_uri: str | None = None

        if ":" in data_type:
            type_uri = _expand_curie(data_type)

        elif isinstance(ctx.get(data_type), dict):
            entry = ctx[data_type]
            if "@id" in entry:
                type_uri = _expand_curie(entry["@id"])

        if not type_uri:
            la_base = ctx.get("la") or "https://linked.art/ns/terms/"
            type_uri = la_base + data_type

        if not type_uri:  # pragma: no cover - mypy
            return

        graph.add((subject, RDF.type, URIRef(type_uri)))

    for key, value in data.items():
        if key in {"id", "type", "@context"}:
            continue

        predicate = _resolve_predicate(key, data_type)
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
