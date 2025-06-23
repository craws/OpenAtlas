from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from urllib.parse import urlparse

from flask import g
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

from openatlas.models.entity import Entity

ACDH = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")

PERSONS_EMITTED = set()

def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False

def create_uri(value: str | list[str]) -> URIRef | list[URIRef]:
    if isinstance(value, list):
        return [create_uri(v) for v in value]
    if is_valid_url(value):
        return URIRef(value)
    safe_name = value.strip().replace(" ", "_").replace(',', '')
    return URIRef(f"https://id.acdh.oeaw.ac.at/{safe_name}")

def ensure_person(graph: Graph, names: str | list[str]) -> None:
    names = names if isinstance(names, list) else [names]
    for name in names:
        if is_valid_url(name):
            continue
        uri = create_uri(name)
        if str(uri) not in PERSONS_EMITTED:
            graph.add((uri, RDF.type, ACDH.Person))
            graph.add((uri, ACDH.hasTitle, Literal(name, lang="und")))
            PERSONS_EMITTED.add(str(uri))

@dataclass
class ArcheFileMetadata:
    uri: str
    titles: list[tuple[str, str]]
    depositor: Optional[str] = None
    license: Optional[str] = None
    licensor: Optional[str] = None
    # metadata_creator should be user like g.logger.get_log_info(entity.id)
    # but this needs way to long (each file need an extra sql query)
    metadata_creator: Optional[str] = None
    owner: Optional[str] = None
    rights_holder: Optional[str] = None
    is_part_of: Optional[str] = None
    accepted_date: Optional[str] = None
    curator: Optional[str] = None
    # Descriptions should also include information about the linked
    # entities like places and persons.
    descriptions: list[tuple[str, str]] = field(default_factory=list)
    language: Optional[str] = None
    principal_investigator: Optional[str] = None
    related_discipline: Optional[str] = None
    # If an image is linked to a place/artifact and the top level of this
    # entity is a place with geonames, than take the geonames link.
    # This will be very expansive.
    spatial_coverage: Optional[str] = None
    submission_date: Optional[str] = None
    transfer_date: Optional[str] = None
    binary_size: Optional[str] = None
    created_start_date: Optional[str] = None
    created_end_date: Optional[str] = None
    creator: Optional[str] = None
    temporal_coverages: list[tuple[str, str]] = field(default_factory=list)
    temporal_coverage_identifier: Optional[str] = None

    @classmethod
    def construct(
            cls,
            entity: Entity,
            metadata: dict[str, Any],
            license_: str) -> 'ArcheFileMetadata':
        part_of = f"https://id.acdh.oeaw.ac.at/{metadata['topCollection']}"
        titles = [(entity.name, metadata['language'])]
        obj = cls(uri=f"{part_of}/{g.files[entity.id].name}", titles=titles)
        obj.depositor = metadata['depositor']
        obj.license = license_
        obj.licensor = entity.creator
        obj.metadata_creator = entity.creator
        obj.owner = entity.license_holder
        obj.rights_holder = entity.license_holder
        obj.creator = entity.creator
        obj.is_part_of = part_of
        obj.accepted_date = metadata['acceptedDate']
        obj.curator = metadata['curator']
        obj.descriptions = [(entity.name, metadata['language'])]
        obj.principal_investigator = metadata['principalInvestigator']
        obj.related_discipline = metadata['relatedDiscipline']
        obj.spatial_coverage = ''
        obj.transfer_date = datetime.today().strftime('%Y-%m-%d')
        obj.binary_size = g.files[entity.id].stat().st_size
        return obj

def add_arche_file_metadata_to_graph(
        graph: Graph,
        metadata: ArcheFileMetadata) -> None:
    subject_uri = URIRef(metadata.uri)

    graph.add((subject_uri, RDF.type, ACDH.Resource))

    for title_text, lang in metadata.titles:
        graph.add((subject_uri, ACDH.hasTitle, Literal(title_text, lang=lang)))

    if metadata.depositor:
        ensure_person(graph, metadata.depositor)
        for uri in create_uri(metadata.depositor) if isinstance(metadata.depositor, list) else [create_uri(metadata.depositor)]:
            graph.add((subject_uri, ACDH.hasDepositor, uri))
    if metadata.license:
        graph.add((subject_uri, ACDH.hasLicense, URIRef(metadata.license)))
    if metadata.licensor:
        ensure_person(graph, metadata.licensor)
        for uri in create_uri(metadata.licensor) if isinstance(metadata.licensor, list) else [create_uri(metadata.licensor)]:
            graph.add((subject_uri, ACDH.hasLicensor, uri))
    if metadata.metadata_creator:
        ensure_person(graph, metadata.metadata_creator)
        for uri in create_uri(metadata.metadata_creator) if isinstance(metadata.metadata_creator, list) else [create_uri(metadata.metadata_creator)]:
            graph.add((subject_uri, ACDH.hasMetadataCreator, uri))
    if metadata.owner:
        ensure_person(graph, metadata.owner)
        for uri in create_uri(metadata.owner) if isinstance(metadata.owner, list) else [create_uri(metadata.owner)]:
            graph.add((subject_uri, ACDH.hasOwner, uri))
    if metadata.rights_holder:
        ensure_person(graph, metadata.rights_holder)
        for uri in create_uri(metadata.rights_holder) if isinstance(metadata.rights_holder, list) else [create_uri(metadata.rights_holder)]:
            graph.add((subject_uri, ACDH.hasRightsHolder, uri))

    if metadata.is_part_of:
        graph.add((subject_uri, ACDH.isPartOf, URIRef(metadata.is_part_of)))
    if metadata.accepted_date:
        graph.add((subject_uri, ACDH.hasAcceptedDate, Literal(metadata.accepted_date, datatype=XSD.date)))
    if metadata.curator:
        ensure_person(graph, metadata.curator)
        for uri in create_uri(metadata.curator) if isinstance(metadata.curator, list) else [create_uri(metadata.curator)]:
            graph.add((subject_uri, ACDH.hasCurator, uri))

    for desc_text, lang in metadata.descriptions:
        graph.add((subject_uri, ACDH.hasDescription, Literal(desc_text, lang=lang)))

    if metadata.language:
        graph.add((subject_uri, ACDH.hasLanguage, URIRef(metadata.language)))
    if metadata.principal_investigator:
        ensure_person(graph, metadata.principal_investigator)
        for uri in create_uri(metadata.principal_investigator) if isinstance(metadata.principal_investigator, list) else [create_uri(metadata.principal_investigator)]:
            graph.add((subject_uri, ACDH.hasPrincipalInvestigator, uri))
    if metadata.related_discipline:
        graph.add((subject_uri, ACDH.hasRelatedDiscipline, URIRef(metadata.related_discipline)))
    if metadata.spatial_coverage:
        graph.add((subject_uri, ACDH.hasSpatialCoverage, URIRef(metadata.spatial_coverage)))
    if metadata.submission_date:
        graph.add((subject_uri, ACDH.hasSubmissionDate, Literal(metadata.submission_date, datatype=XSD.date)))
    if metadata.transfer_date:
        graph.add((subject_uri, ACDH.hasTransferDate, Literal(metadata.transfer_date, datatype=XSD.date)))
    if metadata.binary_size:
        graph.add((subject_uri, ACDH.hasBinarySize, Literal(metadata.binary_size, datatype=XSD.integer)))
    if metadata.created_start_date:
        graph.add((subject_uri, ACDH.hasCreatedStartDate, Literal(metadata.created_start_date, datatype=XSD.date)))
    if metadata.created_end_date:
        graph.add((subject_uri, ACDH.hasCreatedEndDate, Literal(metadata.created_end_date, datatype=XSD.date)))
    if metadata.creator:
        ensure_person(graph, metadata.creator)
        for uri in create_uri(metadata.creator) if isinstance(metadata.creator, list) else [create_uri(metadata.creator)]:
            graph.add((subject_uri, ACDH.hasCreator, uri))

    for tc_text, lang in metadata.temporal_coverages:
        graph.add((subject_uri, ACDH.hasTemporalCoverage, Literal(tc_text, lang=lang)))

    if metadata.temporal_coverage_identifier:
        graph.add((subject_uri, ACDH.hasTemporalCoverageIdentifier, Literal(metadata.temporal_coverage_identifier)))
