import re
from re import search
from typing import Any
from urllib.parse import quote, urlparse, urlunparse

import requests
from flask import abort, g
from rdflib import Graph, Literal, RDF, URIRef, XSD
from unidecode import unidecode

from config.default import ACDH
from openatlas import app
from openatlas.api.external.arche_class import (
    ArcheCollection, ArcheFileMetadata, ArcheTopCollection)
from openatlas.models.entity import Entity
from openatlas.models.rights_holder import RightsHolder


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
    safe_name = re.sub(
        r'[^a-z0-9._-]+',
        '_',
        unidecode(value.strip()).lower()).strip('_')
    return URIRef(transliterate_url(f"https://id.acdh.oeaw.ac.at/{safe_name}"))


def create_uri(value: str | list[str]) -> list[URIRef]:
    if isinstance(value, list):
        return [create_single_uri(v) for v in value]
    return [create_single_uri(value)]


def transliterate_url(url: str) -> str:
    parsed = urlparse(url)
    ascii_path = quote(unidecode(parsed.path), safe='/_-.')
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        ascii_path,
        parsed.params,
        parsed.query,
        parsed.fragment))


def ensure_person_exist(
        graph: Graph,
        names: str | list[str],
        emitted: set[str],
        entity: RightsHolder | None = None) -> None:
    names = names if isinstance(names, list) else [names]
    for name in names:
        if not name or is_valid_url(name):
            continue
        uri = create_single_uri(name)
        if str(uri) not in emitted:
            if entity and entity.class_ == 'group':
                graph.add((uri, RDF.type, ACDH.Organisation))
            elif entity and entity.class_ == 'person':
                graph.add((uri, RDF.type, ACDH.Person))
            else:
                graph.add((uri, RDF.type, ACDH.Agent))
            graph.add((uri, ACDH.hasTitle, Literal(name, lang="und")))
            graph.add((uri, ACDH.hasIdentifier, uri))
            emitted.add(str(uri))


def ensure_publication_exist(
        graph: Graph,
        publication: Entity,
        pages: str,
        emitted: set[str]) -> None:
    uri = create_single_uri(str(publication.id))
    if str(uri) not in emitted:
        graph.add((uri, RDF.type, ACDH.Publication))
        name = publication.name
        graph.add((uri, ACDH.hasTitle, Literal(name, lang="und")))
        graph.add((uri, ACDH.hasIdentifier, uri))
        if is_valid_url(name) and 'doi' in name.lower():
            graph.add((uri, ACDH.hasIdentifier, URIRef(name)))
        if pages:
            graph.add((uri, ACDH.hasPages, Literal(pages)))
        emitted.add(str(uri))


def ensure_entity_exist(
        graph: Graph,
        acdh_property: Any,
        entity_details: dict[str, Any],
        emitted: set[str]) -> None:
    uri = create_single_uri(entity_details['id'])
    if str(uri) not in emitted:
        graph.add((uri, RDF.type, acdh_property))
        name = entity_details['name']
        graph.add((uri, ACDH.hasTitle, Literal(name, lang="und")))
        if is_valid_url(name):
            graph.add((
                uri,
                ACDH.hasUrl,
                Literal(name, datatype=XSD.anyURI)))
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
                        Literal(f"{ref_sys[1]}:{ref_link}")))
        emitted.add(str(uri))


def add_person_role(
        graph: Graph,
        subject_uri: URIRef,
        names: str | list[str] | None,
        predicate: Any,
        emitted: set[str]) -> None:
    if not names:
        return
    ensure_person_exist(graph, names, emitted)
    for uri in create_uri(names):
        graph.add((subject_uri, predicate, uri))


def add_entity_role(
        graph: Graph,
        subject_uri: URIRef,
        entities: list[RightsHolder] | list[str] | str | None,
        predicate: Any,
        emitted: set[str]) -> None:
    if not entities:
        return
    if isinstance(entities, str):
        add_person_role(graph, subject_uri, entities, predicate, emitted)
        return
    for entity in entities:
        if isinstance(entity, RightsHolder):
            ensure_person_exist(graph, entity.name, emitted, entity)
            graph.add((subject_uri, predicate, create_single_uri(entity.name)))
        else:
            add_person_role(graph, subject_uri, entity, predicate, emitted)


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
        entities: list[dict[str, Any]] | None,
        *,
        default_type: Any,
        predicate: Any,
        emitted: set[str]) -> None:
    if not entities:
        return
    for entity in entities:
        entity_type = (
            ACDH.Organisation
            if entity.get('class_name') == 'group'
            else default_type)
        ensure_entity_exist(graph, entity_type, entity, emitted)
        for uri in create_uri(entity['id']):
            graph.add((subject_uri, predicate, uri))


def add_publications(
        graph: Graph,
        subject_uri: URIRef,
        publications: list[tuple[Entity, str]] | None,
        emitted: set[str]) -> None:
    if not publications:
        return
    for publication, pages in publications:
        ensure_publication_exist(graph, publication, pages, emitted)
        graph.add((
            subject_uri,
            ACDH.isSourceOf,
            create_single_uri(str(publication.id))))


def _add_common_repo_metadata(
        graph: Graph,
        subject_uri: URIRef,
        item: Any,
        emitted: set[str]) -> None:
    graph.add((subject_uri, ACDH.hasIdentifier, subject_uri))
    add_language_literals(graph, subject_uri, item.titles, ACDH.hasTitle)
    uri_fields = (
        ('language', ACDH.hasLanguage),
        ('life_cycle_status', ACDH.hasLifeCycleStatus),
        ('hosting', ACDH.hasHosting))
    for attr, predicate in uri_fields:
        if val := getattr(item, attr, None):
            graph.add((subject_uri, predicate, URIRef(val)))
    date_fields = (
        ('accepted_date', ACDH.hasAcceptedDate),
        ('submission_date', ACDH.hasSubmissionDate),
        ('transfer_date', ACDH.hasTransferDate))
    for attr, predicate in date_fields:
        if val := getattr(item, attr, None):
            graph.add((
                subject_uri,
                predicate,
                Literal(val, datatype=XSD.date)))
    role_fields = (
        ('depositors', ACDH.hasDepositor),
        ('curators', ACDH.hasCurator),
        ('metadata_creators', ACDH.hasMetadataCreator),
        ('principal_investigators', ACDH.hasPrincipalInvestigator),
        ('contacts', ACDH.hasContact),
        ('owners', ACDH.hasOwner))
    for attr, predicate in role_fields:
        add_person_role(
            graph, subject_uri, getattr(item, attr, None), predicate, emitted)
    add_related_disciplines(
        graph, subject_uri, getattr(item, 'related_disciplines', None))


def add_arche_top_collection_to_graph(
        graph: Graph,
        top: ArcheTopCollection,
        emitted: set[str]) -> None:
    subject_uri = URIRef(top.uri)
    graph.add((subject_uri, RDF.type, ACDH.TopCollection))
    _add_common_repo_metadata(graph, subject_uri, top, emitted)
    add_language_literals(
        graph, subject_uri, top.descriptions, ACDH.hasDescription)
    add_language_literals(graph, subject_uri, top.subjects, ACDH.hasSubject)
    if top.license_summary:
        graph.add((
            subject_uri,
            ACDH.hasLicenseSummary,
            Literal(top.license_summary[0], lang=top.license_summary[1])))
    if top.extent:
        graph.add((
            subject_uri,
            ACDH.hasExtent,
            Literal(top.extent[0], lang=top.extent[1])))
    if top.used_software:
        graph.add((
            subject_uri,
            ACDH.hasUsedSoftware,
            Literal(top.used_software)))
    if top.url:
        graph.add((
            subject_uri,
            ACDH.hasUrl,
            Literal(top.url, datatype=XSD.anyURI)))
    for attr, predicate in (
            ('editors', ACDH.hasEditor),
            ('rights_holders', ACDH.hasRightsHolder),
            ('licensors', ACDH.hasLicensor)):
        add_person_role(
            graph, subject_uri, getattr(top, attr), predicate, emitted)


def add_arche_collection_to_graph(
        graph: Graph,
        collection: ArcheCollection,
        emitted: set[str]) -> None:
    subject_uri = URIRef(collection.uri)
    graph.add((subject_uri, RDF.type, ACDH.Collection))
    graph.add((subject_uri, ACDH.isPartOf, URIRef(collection.is_part_of)))
    graph.add((subject_uri, ACDH.hasFilename, Literal(collection.filename)))
    _add_common_repo_metadata(graph, subject_uri, collection, emitted)
    if collection.license_summary:
        graph.add((
            subject_uri,
            ACDH.hasLicenseSummary,
            Literal(
                collection.license_summary[0],
                lang=collection.license_summary[1])))
    if collection.extent:
        graph.add((
            subject_uri,
            ACDH.hasExtent,
            Literal(collection.extent[0], lang=collection.extent[1])))


def add_arche_file_metadata_to_graph(
        graph: Graph,
        metadata: ArcheFileMetadata,
        emitted: set[str] | None = None) -> None:
    if emitted is None:
        emitted = set()
    subject_uri = URIRef(metadata.uri)
    graph.add((subject_uri, RDF.type, ACDH.Resource))
    _add_common_repo_metadata(graph, subject_uri, metadata, emitted)
    if metadata.is_part_of:
        graph.add((subject_uri, ACDH.isPartOf, URIRef(metadata.is_part_of)))
    if metadata.is_title_image_of:
        graph.add((
            subject_uri,
            ACDH.isTitleImageOf,
            URIRef(metadata.is_title_image_of)))
    if metadata.filename:
        graph.add((subject_uri, ACDH.hasFilename, Literal(metadata.filename)))
    if metadata.mime_format:
        graph.add((subject_uri, ACDH.hasFormat, Literal(metadata.mime_format)))
    if metadata.category:
        graph.add((subject_uri, ACDH.hasCategory, URIRef(metadata.category)))
    if metadata.access_restriction:
        graph.add((
            subject_uri,
            ACDH.hasAccessRestriction,
            URIRef(metadata.access_restriction)))
    if metadata.binary_size is not None:
        graph.add((
            subject_uri,
            ACDH.hasBinarySize,
            Literal(metadata.binary_size, datatype=XSD.nonNegativeInteger)))
    if metadata.license:
        graph.add((
            subject_uri,
            ACDH.hasLicense,
            create_single_uri(metadata.license)))
    for attr, predicate in (
            ('licensors', ACDH.hasLicensor),
            ('rights_holders', ACDH.hasRightsHolder),
            ('creators', ACDH.hasCreator)):
        add_entity_role(
            graph, subject_uri, getattr(metadata, attr), predicate, emitted)
    add_language_literals(
        graph, subject_uri, metadata.descriptions, ACDH.hasDescription)
    add_related_entities(
        graph,
        subject_uri,
        metadata.actors,
        default_type=ACDH.Person,
        predicate=ACDH.hasActor,
        emitted=emitted)
    add_related_entities(
        graph,
        subject_uri,
        metadata.spatial_coverages,
        default_type=ACDH.Place,
        predicate=ACDH.hasSpatialCoverage,
        emitted=emitted)
    add_publications(graph, subject_uri, metadata.has_publications, emitted)
