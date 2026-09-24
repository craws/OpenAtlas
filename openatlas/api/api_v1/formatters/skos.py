from flask import Response, g
from rdflib import DCTERMS, Graph, Literal, Namespace, RDF, URIRef

from openatlas.api.api_v1.formatters.lod import entity_uri
from openatlas.api.api_v1.formatters.lod_util import get_type_references
from openatlas.api.api_v1.models.util import MatchTypeEnum
from openatlas.models.entity import Entity


# todo: move to api config
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')

SKOS_FORMAT_MAP: dict[str, tuple[str, str]] = {
    'ttl': ('turtle', 'text/turtle'),
    'xml': ('xml', 'application/rdf+xml'),
    'json': ('json-ld', 'application/ld+json'),
    'nt': ('nt', 'application/n-triples')}


def _add_match_links(graph: Graph, concept: URIRef, type_id: int) -> None:
    from openatlas.api.api_v1.routes.vocabulary import \
        get_external_reference_items
    inverse_links = get_type_references().get(type_id, [])
    for reference in get_external_reference_items(inverse_links):
        if not reference.identifier:
            continue
        predicate = SKOS.exactMatch
        if reference.match_type == MatchTypeEnum.CLOSE_MATCH:
            predicate = SKOS.closeMatch
        graph.add((concept, predicate, URIRef(reference.identifier)))


def _add_concept(
        graph: Graph,
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
        graph.add((concept, SKOS.prefLabel, Literal(type_.name, lang=language)))
    if type_.description:
        graph.add((
            concept, SKOS.scopeNote, Literal(type_.description, lang=language)))
    _add_match_links(graph, concept, type_.id)
    return concept


def _walk_concepts(
        graph: Graph,
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


def build_skos_graph(root: Entity) -> Graph:
    graph = Graph()
    graph.bind('skos', SKOS)
    graph.bind('dcterms', DCTERMS)
    language = g.settings['default_language']

    scheme = URIRef(entity_uri(root))
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    if root.name:
        graph.add((scheme, SKOS.prefLabel, Literal(root.name, lang=language)))
    # TODO: replace placeholders once ConceptScheme metadata storage exists
    graph.add((scheme, DCTERMS.title, Literal(root.name or 'TODO: title')))
    graph.add((scheme, DCTERMS.creator, Literal('TODO: creator')))
    graph.add((scheme, DCTERMS.license, Literal('TODO: license')))

    _walk_concepts(graph, root.id, None, scheme, language, {root.id}, True)
    return graph


def serialize_skos(graph: Graph, ext: str) -> Response:
    rdf_format, mimetype = SKOS_FORMAT_MAP[ext]
    return Response(graph.serialize(format=rdf_format), mimetype=mimetype)
