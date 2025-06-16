from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from flask import g

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
