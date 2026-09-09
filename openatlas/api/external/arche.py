from re import search
from typing import Any
from urllib.parse import urlparse, urlunparse

import requests
from flask import abort, g
from rdflib import Graph, Literal, RDF, URIRef, XSD
from unidecode import unidecode

from config.default import ACDH
from openatlas import app
from openatlas.api.external.arche_class import ArcheFileMetadata
from openatlas.models.entity import Entity

ENTITIES_EMITTED = set()


def is_arche_likeable_uri(uri: str) -> bool:
    if not g.arche_uri_rules:
        try:
            g.arche_uri_rules = requests.get(
                app.config['ARCHE_URI_RULES'],
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            abort(400, 'ARCHE not reachable')
    for rule in g.arche_uri_rules:
        if search(rule['match'], uri):
            return True
    return False


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except ValueError:  # pragma: no cover
        return False


def create_single_uri(value: str) -> URIRef:
    if is_valid_url(value):
        return URIRef(value)
    safe_name = (
        value.strip()
        .replace(" ", "_")
        .replace(",", "_")
        .replace("/", "_")
        .lower())
    return URIRef(transliterate_url(f"https://id.acdh.oeaw.ac.at/{safe_name}"))


def create_uri(value: str | list[str]) -> list[URIRef]:
    if isinstance(value, list):
        return [create_single_uri(v) for v in value]
    return [create_single_uri(value)]


def ensure_person_exist(
        graph: Graph,
        names: str | list[str],
        entity: Entity | None = None) -> None:
    names = names if isinstance(names, list) else [names]
    for name in names:
        if not name or is_valid_url(name):
            continue  # pragma: no cover
        uri = create_single_uri(name)
        if str(uri) not in ENTITIES_EMITTED:
            if entity and entity.class_ == 'group':
                graph.add((uri, RDF.type, ACDH.Organisation))
            elif entity and entity.class_ == 'person':
                graph.add((uri, RDF.type, ACDH.Person))
            else:
                graph.add((uri, RDF.type, ACDH.Agent))
            graph.add((uri, ACDH.hasTitle, Literal(name, lang="und")))
            graph.add((uri, ACDH.hasIdentifier, uri))
            ENTITIES_EMITTED.add(str(uri))


def ensure_publication_exist(
        graph: Graph,
        publication: Entity,
        pages: str) -> None:
    uri = create_single_uri(str(publication.id))
    if str(uri) not in ENTITIES_EMITTED:
        graph.add((uri, RDF.type, ACDH.Publication))
        name = publication.name
        graph.add((uri, ACDH.hasTitle, Literal(name, lang="und")))
        graph.add((uri, ACDH.hasIdentifier, URIRef(uri)))
        if is_valid_url(name) and 'doi' in name.lower():
            graph.add((uri, ACDH.hasIdentifier, URIRef(name)))
        if pages:
            graph.add((uri, ACDH.hasPages, Literal(pages, lang="und")))


def ensure_entity_exist(
        graph: Graph,
        acdh_property: Any,
        entity_details: dict[str, Any]) -> None:
    uri = create_single_uri(entity_details['id'])
    if str(uri) not in ENTITIES_EMITTED:
        graph.add((uri, RDF.type, acdh_property))
        name = entity_details['name']
        graph.add((uri, ACDH.hasTitle, Literal(name, lang="und")))
        if is_valid_url(name):
            graph.add((uri, ACDH.hasUrl, URIRef(name)))
        if description := entity_details['description']:
            graph.add(
                (uri, ACDH.hasDescription, Literal(description, lang="und")))
        graph.add((uri, ACDH.hasIdentifier, uri))
        for ref_sys in entity_details['reference_systems']:
            if ref_link := ref_sys[0]:
                if is_valid_url(ref_link) and is_arche_likeable_uri(ref_link):
                    graph.add((uri, ACDH.hasIdentifier, URIRef(ref_link)))
                else:
                    graph.add((
                        uri,
                        ACDH.hasNonLinkedIdentifier,
                        Literal(f"{ref_sys[1]}:{ref_link}", lang="und")))
        ENTITIES_EMITTED.add(str(uri))


def transliterate_url(url: str) -> str:
    parsed = urlparse(url)
    ascii_path = unidecode(parsed.path)
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        ascii_path.replace(' ', '_'),
        parsed.params,
        parsed.query,
        parsed.fragment))


def add_person_role(
        graph: Graph,
        subject_uri: URIRef,
        names: str | list[str] | None,
        predicate: Any) -> None:
    if not names:
        return
    ensure_person_exist(graph, names)
    for uri in create_uri(names):
        graph.add((subject_uri, predicate, uri))


def add_entity_role(
        graph: Graph,
        subject_uri: URIRef,
        entities: list[Entity] | None,
        predicate: Any) -> None:
    if not entities:
        return
    for entity in entities:
        ensure_person_exist(graph, entity.name, entity)
        graph.add((subject_uri, predicate, create_single_uri(entity.name)))


def add_scalar_metadata(
        graph: Graph,
        subject_uri: URIRef,
        metadata: ArcheFileMetadata) -> None:
    scalar_metadata = (
        ('license', ACDH.hasLicense, URIRef),
        ('is_part_of', ACDH.isPartOf, URIRef),
        ('accepted_date', ACDH.hasAcceptedDate,
         lambda value: Literal(value, datatype=XSD.date)),
        ('language', ACDH.hasLanguage, URIRef),
        ('transfer_date', ACDH.hasTransferDate,
         lambda value: Literal(value, datatype=XSD.date)),
        ('binary_size', ACDH.hasBinarySize,
         lambda value: Literal(value, datatype=XSD.integer)))
    for attribute, predicate, value_factory in scalar_metadata:
        if value := getattr(metadata, attribute):
            graph.add((subject_uri, predicate, value_factory(value)))


def add_language_literals(
        graph: Graph,
        subject_uri: URIRef,
        values: list[tuple[Any, str]] | None,
        predicate: Any) -> None:
    if not values:
        return
    for text, language in values:
        graph.add((subject_uri, predicate, Literal(text, lang=language)))


def add_related_disciplines(
        graph: Graph,
        subject_uri: URIRef,
        disciplines: str | list[str] | None) -> None:
    if not disciplines:
        return
    for discipline in create_uri(disciplines):
        graph.add((subject_uri, ACDH.hasRelatedDiscipline, discipline))


def add_related_entities(
        graph: Graph,
        subject_uri: URIRef,
        entities: list[dict[str, str | list[str]]] | None,
        entity_type: Any,
        predicate: Any) -> None:
    if not entities:
        return
    for entity in entities:
        ensure_entity_exist(graph, entity_type, entity)
        for uri in create_uri(entity['id']):
            graph.add((subject_uri, predicate, uri))


def add_publications(
        graph: Graph,
        subject_uri: URIRef,
        publications: list[tuple[Entity, str]] | None) -> None:
    if not publications:
        return
    for publication, pages in publications:
        ensure_publication_exist(graph, publication, pages)
        graph.add((
            subject_uri,
            ACDH.isSourceOf,
            create_single_uri(str(publication.id))))


def add_arche_file_metadata_to_graph(
        graph: Graph,
        metadata: ArcheFileMetadata) -> None:
    subject_uri = URIRef(metadata.uri)

    graph.add((subject_uri, RDF.type, ACDH.Resource))

    for title_text, lang in metadata.titles:
        graph.add((subject_uri, ACDH.hasTitle, Literal(title_text, lang=lang)))

    add_scalar_metadata(graph, subject_uri, metadata)
    for attribute, predicate in (
            ('depositors', ACDH.hasDepositor),
            ('curators', ACDH.hasCurator),
            ('principal_investigators', ACDH.hasPrincipalInvestigator),
            ('metadata_creators', ACDH.hasMetadataCreator)):
        add_person_role(
            graph, subject_uri, getattr(metadata, attribute), predicate)
    for attribute, predicate in (
            ('licensors', ACDH.hasLicensor),
            ('rights_holders', ACDH.hasRightsHolder),
            ('creators', ACDH.hasCreator)):
        add_entity_role(
            graph, subject_uri, getattr(metadata, attribute), predicate)

    add_language_literals(
        graph, subject_uri, metadata.descriptions, ACDH.hasDescription)
    add_related_disciplines(graph, subject_uri, metadata.related_disciplines)
    add_related_entities(
        graph, subject_uri, metadata.actors, ACDH.Person, ACDH.hasActor)
    add_related_entities(
        graph,
        subject_uri,
        metadata.spatial_coverages,
        ACDH.Place,
        ACDH.hasSpatialCoverage)
    add_publications(graph, subject_uri, metadata.has_publications)
