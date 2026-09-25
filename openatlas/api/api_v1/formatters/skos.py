from typing import Final
from urllib.parse import quote, urlparse

from flask import Response, g
from rdflib import DCTERMS, Dataset, Literal, Namespace, RDF, URIRef

from openatlas.api.api_v1.formatters.lod import entity_uri
from openatlas.api.api_v1.formatters.lod_util import get_type_references
from openatlas.api.api_v1.models.util import (
    ExternalReferenceSystemModel, MatchTypeEnum)
from openatlas.api.api_v1.util.content_negotiation import make_graph_response
from openatlas.models.entity import Entity

SKOS: Final[Namespace] = Namespace('http://www.w3.org/2004/02/skos/core#')

URI_SAFE_CHARS: Final[str] = ":/?#[]@!$&'()*+,;=%~"


def _get_match_uri(reference: ExternalReferenceSystemModel) -> URIRef | None:
    if not reference.identifier:
        return None
    resolver = reference.url or ''
    local_id = reference.identifier.removeprefix(resolver).strip()
    if not local_id:
        return None
    uri = f'{resolver}{quote(local_id, safe=URI_SAFE_CHARS)}'
    parsed = urlparse(uri)
    if not parsed.scheme or not parsed.netloc:
        return None  # No resolvable URI, e.g. system without resolver URL
    return URIRef(uri)


def _add_match_links(graph: Dataset, concept: URIRef, type_id: int) -> None:
    from openatlas.api.api_v1.routes.vocabulary import \
        get_external_reference_items
    inverse_links = get_type_references().get(type_id, [])
    for reference in get_external_reference_items(inverse_links):
        if not (uri := _get_match_uri(reference)):
            continue
        predicate = SKOS.exactMatch
        if reference.match_type == MatchTypeEnum.CLOSE_MATCH:
            predicate = SKOS.closeMatch
        graph.add((concept, predicate, uri))


def _add_concept(
        graph: Dataset,
        type_: Entity,
        scheme: URIRef,
        language: str,
        is_top: bool) -> URIRef:
    concept = URIRef(entity_uri(type_))
    graph.add((concept, RDF.type, SKOS.Concept))
    if is_top:
        graph.add((concept, SKOS.topConceptOf, scheme))
        graph.add((scheme, SKOS.hasTopConcept, concept))
    else:
        graph.add((concept, SKOS.inScheme, scheme))
    if type_.name:
        graph.add(
            (concept, SKOS.prefLabel, Literal(type_.name, lang=language)))
    if type_.description:
        graph.add((
            concept, SKOS.scopeNote,
            Literal(type_.description, lang=language)))
    _add_match_links(graph, concept, type_.id)
    return concept


def _walk_concepts(
        graph: Dataset,
        parent_id: int,
        parent_node: URIRef | None,
        scheme: URIRef,
        language: str,
        visited: set[int],
        is_top_level: bool) -> None:
    parent = g.types[parent_id]
    for sub_id in parent.subs:
        if sub_id in visited:
            continue
        visited.add(sub_id)
        sub = g.types[sub_id]
        concept = _add_concept(graph, sub, scheme, language, is_top_level)
        if not is_top_level and parent_node is not None:
            graph.add((concept, SKOS.broader, parent_node))
            graph.add((parent_node, SKOS.narrower, concept))
        _walk_concepts(
            graph, sub_id, concept, scheme, language, visited, False)


def build_skos_graph(root: Entity) -> Dataset:
    graph = Dataset()
    graph.bind('skos', SKOS)
    graph.bind('dcterms', DCTERMS)
    language = g.settings['default_language']

    scheme = URIRef(entity_uri(root))
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    if root.name:
        graph.add((scheme, SKOS.prefLabel, Literal(root.name, lang=language)))
    # graph.add((scheme, DCTERMS.title, Literal('title')))
    # graph.add((scheme, DCTERMS.creator, Literal('creator')))
    # graph.add((scheme, DCTERMS.license, Literal('license')))

    _walk_concepts(graph, root.id, None, scheme, language, {root.id}, True)
    return graph


def serialize_skos(graph: Dataset, ext: str | None = None) -> Response:
    return make_graph_response(graph, ext=ext)
