from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from flask import g

from openatlas import app
from openatlas.models.entity import Entity


@dataclass
class ArcheFileMetadata:
    uri: str
    titles: list[tuple[str, str]]
    depositor: Optional[str] = None
    license: Optional[str] = None
    licensor: Optional[str] = None
    metadata_creator: Optional[str] = None
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
    submission_date: Optional[str] = None
    transfer_date: Optional[str] = None
    binary_size: Optional[int] = None
    created_start_date: Optional[str] = None
    created_end_date: Optional[str] = None
    creator: Optional[str] = None
    actors: Optional[list[dict[str, str | list[str]]]] = None
    spatial_coverages: Optional[list[dict[str, str | list[str]]]] = None
    has_publications: Optional[list[tuple[Entity, str]]] = None
    temporal_coverages: list[tuple[str, str]] = field(default_factory=list)
    temporal_coverage_identifier: Optional[str] = None

    @classmethod
    def construct(
            cls,
            entity: Entity,
            type_name: str,
            relations: list[dict[str, Any]],
            # publication: list[tuple[Entity, str]],
            license_: str) -> 'ArcheFileMetadata':
        metadata = app.config['ARCHE_METADATA']
        part_of = f"https://id.acdh.oeaw.ac.at/{metadata['topCollection']}"
        # titles = [(entity.name, metadata['language'])]
        titles = [(entity.name, 'und')]
        file_info = (g.files[entity.id].suffix[1:], g.files[entity.id].name)
        obj = cls(
            uri=f"{part_of}/{type_name}/{file_info[0]}/{file_info[1]}",
            titles=titles)
        obj.depositor = metadata['depositor']
        obj.license = license_
        obj.licensor = entity.license_holder
        obj.metadata_creator = metadata['hasMetadataCreator']
        obj.rights_holder = entity.license_holder
        obj.creator = entity.creator
        obj.is_part_of = part_of
        obj.accepted_date = metadata['acceptedDate']
        obj.curator = metadata['curator']
        # obj.descriptions = [(entity.description, metadata['language'])]
        obj.descriptions = [(entity.description, 'und')]
        obj.principal_investigator = metadata['principalInvestigator']
        obj.related_discipline = metadata['relatedDiscipline']
        obj.transfer_date = datetime.today().strftime('%Y-%m-%d')
        obj.binary_size = g.files[entity.id].stat().st_size
        actors = []
        places = []
        if relations:
            for relation in relations:
                ref_system_info: list[tuple[str, str]] = []
                for ref in relation['ref_systems']:
                    if (ref['referenceSystem']
                            in metadata['exclude_reference_systems']):
                        continue
                    ref_system_info.append(
                        (ref['identifier'], ref['referenceSystem']))
                values = {
                    'id': str(relation['entity'].id),
                    'name': relation['entity'].name,
                    'reference_systems': ref_system_info,
                    'description': relation['entity'].description}
                if relation['entity'].class_.name == 'place':
                    places.append(values)
                if relation['entity'].class_.view == 'actor':
                    actors.append(values)
        obj.actors = actors
        obj.spatial_coverages = places
        return obj
