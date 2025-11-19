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
    return False  # pragma: no cover


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
        names: str | list[str]) -> None:
    names = names if isinstance(names, list) else [names]
    for name in names:

        if not name or is_valid_url(name):
            continue  # pragma: no cover
        uri = create_single_uri(name)
        if str(uri) not in ENTITIES_EMITTED:
            graph.add((uri, RDF.type, ACDH.Person))
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
    path = parsed.path
    ascii_path = unidecode(path)
    ascii_path = ascii_path.replace(' ', '_')
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        ascii_path,
        parsed.params,
        parsed.query,
        parsed.fragment))


def add_arche_file_metadata_to_graph(
        graph: Graph,
        metadata: ArcheFileMetadata) -> None:
    subject_uri = URIRef(metadata.uri)

    graph.add((subject_uri, RDF.type, ACDH.Resource))

    for title_text, lang in metadata.titles:
        graph.add((subject_uri, ACDH.hasTitle, Literal(title_text, lang=lang)))

    if metadata.depositors:
        ensure_person_exist(graph, metadata.depositors)
        for uri in create_uri(metadata.depositors):
            graph.add((subject_uri, ACDH.hasDepositor, uri))

    if metadata.license:
        graph.add((subject_uri, ACDH.hasLicense, URIRef(metadata.license)))

    if metadata.licensors:
        ensure_person_exist(graph, metadata.licensors)
        for uri in create_uri(metadata.licensors):
            graph.add((subject_uri, ACDH.hasLicensor, uri))

    if metadata.rights_holders:
        ensure_person_exist(graph, metadata.rights_holders)
        for uri in create_uri(metadata.rights_holders):
            graph.add((subject_uri, ACDH.hasRightsHolder, uri))

    if metadata.is_part_of:
        graph.add((subject_uri, ACDH.isPartOf, URIRef(metadata.is_part_of)))

    if metadata.accepted_date:
        graph.add((
            subject_uri,
            ACDH.hasAcceptedDate,
            Literal(metadata.accepted_date, datatype=XSD.date)))

    if metadata.curators:
        ensure_person_exist(graph, metadata.curators)
        for uri in create_uri(metadata.curators):
            graph.add((subject_uri, ACDH.hasCurator, uri))

    if metadata.descriptions:  # pragma: no cover, Todo: test or remove todo
        for desc_text, lang in metadata.descriptions:
            graph.add((
                subject_uri,
                ACDH.hasDescription,
                Literal(desc_text, lang=lang)))

    if metadata.language:
        graph.add((subject_uri, ACDH.hasLanguage, URIRef(metadata.language)))

    if metadata.principal_investigators:
        ensure_person_exist(graph, metadata.principal_investigators)
        for uri in create_uri(metadata.principal_investigators):
            graph.add((subject_uri, ACDH.hasPrincipalInvestigator, uri))

    if metadata.related_disciplines:
        for related_discipline in metadata.related_disciplines:
            graph.add((
                subject_uri,
                ACDH.hasRelatedDiscipline,
                URIRef(related_discipline)))

    if metadata.transfer_date:
        graph.add((
            subject_uri,
            ACDH.hasTransferDate,
            Literal(metadata.transfer_date, datatype=XSD.date)))

    if metadata.binary_size:
        graph.add((
            subject_uri,
            ACDH.hasBinarySize,
            Literal(metadata.binary_size, datatype=XSD.integer)))

    if metadata.creators:
        ensure_person_exist(graph, metadata.creators)
        for uri in create_uri(metadata.creators):
            graph.add((subject_uri, ACDH.hasCreator, uri))

    if metadata.metadata_creators:
        ensure_person_exist(graph, metadata.metadata_creators)
        for uri in create_uri(metadata.metadata_creators):
            graph.add((subject_uri, ACDH.hasMetadataCreator, uri))

    if metadata.actors:
        for actor in metadata.actors:
            ensure_entity_exist(graph, ACDH.Person, actor)
            for uri in create_uri(actor['id']):
                graph.add((subject_uri, ACDH.hasActor, uri))

    if metadata.spatial_coverages:
        for place in metadata.spatial_coverages:
            ensure_entity_exist(graph, ACDH.Place, place)
            for uri in create_uri(place['id']):
                graph.add((subject_uri, ACDH.hasSpatialCoverage, uri))

    if metadata.has_publications:
        for publication in metadata.has_publications:
            ensure_publication_exist(graph, publication[0], publication[1])
            graph.add((
                subject_uri,
                ACDH.isSourceOf,
                create_single_uri(str(publication[0].id))))
