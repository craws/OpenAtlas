import json
import urllib.request
from re import search
from typing import Any
from urllib.parse import urlparse, urlunparse

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD
from unidecode import unidecode

from openatlas import app
from openatlas.api.external.arche_class import ArcheFileMetadata

ACDH = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
ENTITIES_EMITTED = set()

with urllib.request.urlopen(app.config['ARCHE_URI_RULES']) as response:
    arche_uri_rules = json.load(response)

def is_arche_likeable_uri(uri: str) -> bool:
    for rule in arche_uri_rules:
        if search(rule['match'], uri):
            return True
    print(False)
    return False


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except ValueError:
        return False


def create_uri(value: str | list[str]) -> URIRef | list[URIRef]:
    if isinstance(value, list):
        return [create_uri(v) for v in value]
    if is_valid_url(value):
        return URIRef(value)
    safe_name = (value.strip()
                 .replace(" ", "_")
                 .replace(",", "_")
                 .replace("/", "_")
                 .lower())
    return URIRef(transliterate_url(f"https://id.acdh.oeaw.ac.at/{safe_name}"))

# Todo: use ensure_person_new. Refactor code to new function
def ensure_person(
        graph: Graph,
        names: str | list[str]) -> None:
    names = names if isinstance(names, list) else [names]
    for name in names:
        if not name or is_valid_url(name):
            continue
        uri = create_uri(name)
        if str(uri) not in ENTITIES_EMITTED:
            graph.add((uri, RDF.type, ACDH.Person))
            graph.add((uri, ACDH.hasTitle, Literal(name, lang="und")))
            ENTITIES_EMITTED.add(str(uri))




def ensure_entity_exist(
        graph: Graph,
        acdh_property: Any,
        entity_details: dict[str, Any]) -> None:
    name = entity_details['name']
    if not name:  # or is_valid_url(name):
        return None
    uri = create_uri(name)
    if str(uri) not in ENTITIES_EMITTED:
        graph.add((uri, RDF.type, acdh_property))
        graph.add((uri, ACDH.hasTitle, Literal(name, lang="und")))
        if description := entity_details['description']:
            graph.add(
                (uri, ACDH.hasDescription, Literal(description, lang="und")))
        for ref_sys in entity_details['reference_systems']:
            if ref_link := ref_sys[0]:
                if (is_valid_url(ref_link)
                        and is_arche_likeable_uri(ref_link)):
                    graph.add((uri, ACDH.hasIdentifier, URIRef(ref_link)))
                else:
                    graph.add((
                        uri,
                        ACDH.hasNonLinkedIdentifier,
                        Literal(f"{ref_sys[1]}:{ref_link}", lang="und")))
        ENTITIES_EMITTED.add(str(uri))
    return None



def transliterate_url(url):
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

    if metadata.depositor:
        ensure_person(graph, metadata.depositor)
        for uri in create_uri(metadata.depositor) \
                if isinstance(metadata.depositor, list) \
                else [create_uri(metadata.depositor)]:
            graph.add((subject_uri, ACDH.hasDepositor, uri))
    if metadata.license:
        graph.add((subject_uri, ACDH.hasLicense, URIRef(metadata.license)))
    if metadata.licensor:
        ensure_person(graph, metadata.licensor)
        for uri in create_uri(metadata.licensor) \
                if isinstance(metadata.licensor, list) \
                else [create_uri(metadata.licensor)]:
            graph.add((subject_uri, ACDH.hasLicensor, uri))
    if metadata.rights_holder:
        ensure_person(graph, metadata.rights_holder)
        for uri in create_uri(metadata.rights_holder) \
                if isinstance(metadata.rights_holder, list) \
                else [create_uri(metadata.rights_holder)]:
            graph.add((subject_uri, ACDH.hasRightsHolder, uri))

    if metadata.is_part_of:
        graph.add((subject_uri, ACDH.isPartOf, URIRef(metadata.is_part_of)))
    if metadata.accepted_date:
        graph.add((subject_uri,
                   ACDH.hasAcceptedDate,
                   Literal(metadata.accepted_date, datatype=XSD.date)))
    if metadata.curator:
        ensure_person(graph, metadata.curator)
        for uri in create_uri(metadata.curator) \
                if isinstance(metadata.curator, list) \
                else [create_uri(metadata.curator)]:
            graph.add((subject_uri, ACDH.hasCurator, uri))

    for desc_text, lang in metadata.descriptions:
        graph.add((subject_uri,
                   ACDH.hasDescription,
                   Literal(desc_text, lang=lang)))

    if metadata.language:
        graph.add((subject_uri, ACDH.hasLanguage, URIRef(metadata.language)))
    if metadata.principal_investigator:
        ensure_person(graph, metadata.principal_investigator)
        for uri in create_uri(metadata.principal_investigator) \
                if isinstance(metadata.principal_investigator, list) \
                else [create_uri(metadata.principal_investigator)]:
            graph.add((subject_uri, ACDH.hasPrincipalInvestigator, uri))
    if metadata.related_discipline:
        for related_discipline in metadata.related_discipline:
            graph.add((subject_uri,
                       ACDH.hasRelatedDiscipline,
                       URIRef(related_discipline)))
    if metadata.submission_date:
        graph.add((subject_uri,
                   ACDH.hasSubmissionDate,
                   Literal(metadata.submission_date, datatype=XSD.date)))
    if metadata.transfer_date:
        graph.add((subject_uri,
                   ACDH.hasTransferDate,
                   Literal(metadata.transfer_date, datatype=XSD.date)))
    if metadata.binary_size:
        graph.add((subject_uri,
                   ACDH.hasBinarySize,
                   Literal(metadata.binary_size, datatype=XSD.integer)))
    if metadata.created_start_date:
        graph.add((subject_uri,
                   ACDH.hasCreatedStartDate,
                   Literal(metadata.created_start_date, datatype=XSD.date)))
    if metadata.created_end_date:
        graph.add((subject_uri,
                   ACDH.hasCreatedEndDate,
                   Literal(metadata.created_end_date, datatype=XSD.date)))
    if metadata.creator:
        ensure_person(graph, metadata.creator)
        for uri in create_uri(metadata.creator) \
                if isinstance(metadata.creator, list) \
                else [create_uri(metadata.creator)]:
            graph.add((subject_uri, ACDH.hasCreator, uri))

    if metadata.actors:
        for actor in metadata.actors:
            ensure_entity_exist(
                graph,
                ACDH.Person,
                actor)
            graph.add((subject_uri, ACDH.hasActor, create_uri(actor['name'])))

    if metadata.spatial_coverages:
        for place in metadata.spatial_coverages:
            ensure_entity_exist(
                graph,
                ACDH.Place,
                place)
            graph.add((
                subject_uri,
                ACDH.hasSpatialCoverage,
                create_uri(place['name'])))



    for tc_text, lang in metadata.temporal_coverages:
        graph.add((subject_uri,
                   ACDH.hasTemporalCoverage,
                   Literal(tc_text, lang=lang)))

    if metadata.temporal_coverage_identifier:
        graph.add((subject_uri,
                   ACDH.hasTemporalCoverageIdentifier,
                   Literal(metadata.temporal_coverage_identifier)))
