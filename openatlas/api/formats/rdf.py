from __future__ import annotations

import os
from typing import Any, Iterator

from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

from openatlas import app
from openatlas.api.resources.resolve_endpoints import get_loud_context

linked_art_context = get_loud_context()


def _add_namespaces(graph: Graph, context: dict):
    """
    Adds namespaces from the @context block to the RDF graph.
    """
    for prefix, uri in context["@context"].items():
        if isinstance(uri, str):
            if uri.endswith('/') or uri.endswith('#'):
                graph.bind(prefix, Namespace(uri))

def _add_triples_from_linked_art(
        graph: Graph,
        data: list[dict[str, Any]] | dict[str, Any],
        parent_subject=None,
        parent_predicate=None):
    """
    Recursively processes a Linked Art JSON-LD dictionary and adds triples
    to the graph.
    """
    if isinstance(data, list):
        for item in data:
            _add_triples_from_linked_art(
                graph,
                item,
                parent_subject,
                parent_predicate)
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
        # First, check if the key is a direct alias in the context
        context_entry = linked_art_context["@context"].get(key)
        if isinstance(context_entry, dict) and '@id' in context_entry:
            predicate_uri_string = context_entry['@id']
        elif isinstance(context_entry, str):
            predicate_uri_string = context_entry
        else:
            # If not in context, assume it's a prefixed URI
            predicate_uri_string = key

        if ':' in predicate_uri_string:
            prefix, localname = predicate_uri_string.split(':', 1)
            prefix_uri = linked_art_context["@context"].get(prefix)
            if isinstance(prefix_uri, str):
                predicate = URIRef(prefix_uri + localname)
            else:
                print(f"Warning: Could not resolve prefix '{prefix}' for key '{key}'")
        else:
            predicate = URIRef(predicate_uri_string)

        if not predicate:
            continue

        if isinstance(value, dict):
            object_uri = value.get('id')
            if object_uri:
                graph.add((subject, predicate, URIRef(object_uri)))
                _add_triples_from_linked_art(graph, value)
            else:
                # This is an inline object (blank node).
                # The recursive call will handle adding triples from it.
                _add_triples_from_linked_art(graph, value, subject, predicate)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    object_uri = item.get('id')
                    if object_uri:
                        graph.add((subject, predicate, URIRef(object_uri)))
                        _add_triples_from_linked_art(graph, item)
                    else:
                        # This is an inline object (blank node) in a list.
                        # The recursive call will handle adding triples from
                        # it.
                        _add_triples_from_linked_art(graph, item, subject,
                                                     predicate)
                else:
                    graph.add((subject, predicate, Literal(item)))
        else:
            graph.add((subject, predicate, Literal(value)))

def rdf_output(data: Iterator[dict[str, Any]], format_: str) -> Any:
    """
    Manually parses JSON-LD data from an iterator and serializes it to an
    RDF graph.
    """
    graph = Graph()
    _add_namespaces(graph, linked_art_context)

    for item in data:
        _add_triples_from_linked_art(graph, item)

    if 'http' in app.config['PROXIES']:
        os.environ['http_proxy'] = app.config['PROXIES']['http']
    if 'https' in app.config['PROXIES']:
        os.environ['https_proxy'] = app.config['PROXIES']['https']

    return graph.serialize(format=format_, encoding='utf-8')
