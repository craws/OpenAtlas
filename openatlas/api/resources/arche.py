from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from flask import g
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

from openatlas.models.entity import Entity


@dataclass
class ArcheFileMetadata:
    uri: str
    titles: list[tuple[str, str]]
    depositor: Optional[str] = None
    license: Optional[str] = None
    licensor: Optional[str] = None
    metadata_creator: Optional[str] = None
    owner: Optional[str] = None
    rights_holder: Optional[str] = None
    is_part_of: Optional[str] = None
    accepted_date: Optional[str] = None
    curator: Optional[str] = None
    descriptions: list[tuple[str, str]] = field(default_factory=list)
    language: Optional[str] = None
    principal_investigator: Optional[str] = None
    related_discipline: Optional[str] = None
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
        # metadata_creator should be user like g.logger.get_log_info(entity.id)
        # but this needs way to long (each file need an extra sql query)
        obj.metadata_creator = entity.creator
        obj.owner = entity.license_holder
        obj.rights_holder = entity.license_holder
        obj.creator = entity.creator
        obj.is_part_of = part_of
        obj.accepted_date = metadata['acceptedDate']
        obj.curator = metadata['curator']
        # Descriptions should also include information about the linked
        # entities like places and persons.
        obj.descriptions = [(entity.name, metadata['language'])]
        obj.principal_investigator = metadata['principalInvestigator']
        obj.related_discipline = metadata['relatedDiscipline']
        # If an image is linked to a place/artifact and the top level of this
        # entity is a place with geonames, than take the geonames link.
        # This will be very expansive.
        obj.spatial_coverage = ''
        obj.transfer_date = datetime.today().strftime('%Y-%m-%d')
        obj.binary_size = g.files[entity.id].stat().st_size
        return obj


ACDH = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")

def add_arche_file_metadata_to_graph(
        graph: Graph,
        metadata: ArcheFileMetadata) -> None:
    subject_uri = URIRef(metadata.uri)


    graph.add((subject_uri, RDF.type, ACDH.Resource))
    for title_text, lang in metadata.titles:
        graph.add((subject_uri, ACDH.hasTitle, Literal(title_text, lang=lang)))
    if metadata.depositor:
        graph.add((subject_uri, ACDH.hasDepositor, URIRef(metadata.depositor)))
    if metadata.license:
        graph.add((subject_uri, ACDH.hasLicense, URIRef(metadata.license)))
    if metadata.licensor:
        graph.add((subject_uri, ACDH.hasLicensor, URIRef(metadata.licensor)))
    if metadata.metadata_creator:
        graph.add((subject_uri, ACDH.hasMetadataCreator, URIRef(metadata.metadata_creator)))
    if metadata.owner:
        graph.add((subject_uri, ACDH.hasOwner, URIRef(metadata.owner)))
    if metadata.rights_holder:
        graph.add((subject_uri, ACDH.hasRightsHolder, URIRef(metadata.rights_holder)))
    if metadata.is_part_of:
        graph.add((subject_uri, ACDH.isPartOf, URIRef(metadata.is_part_of)))
    if metadata.accepted_date:
        graph.add((subject_uri, ACDH.hasAcceptedDate, Literal(metadata.accepted_date, datatype=XSD.date)))
    if metadata.curator:
        graph.add((subject_uri, ACDH.hasCurator, URIRef(metadata.curator)))
    for desc_text, lang in metadata.descriptions:
        graph.add((subject_uri, ACDH.hasDescription, Literal(desc_text, lang=lang)))
    if metadata.language:
        graph.add((subject_uri, ACDH.hasLanguage, URIRef(metadata.language)))
    if metadata.principal_investigator:
        graph.add((subject_uri, ACDH.hasPrincipalInvestigator, URIRef(metadata.principal_investigator)))
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
        graph.add((subject_uri, ACDH.hasCreator, URIRef(metadata.creator)))
    for tc_text, lang in metadata.temporal_coverages:
        graph.add((subject_uri, ACDH.hasTemporalCoverage, Literal(tc_text, lang=lang)))
    if metadata.temporal_coverage_identifier:
        graph.add((subject_uri, ACDH.hasTemporalCoverageIdentifier, Literal(metadata.temporal_coverage_identifier)))


