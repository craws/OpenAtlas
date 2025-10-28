from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from flask import g

from openatlas import app
from openatlas.models.entity import Entity


@dataclass
class ArcheFileMetadata:
    uri: str
    titles: list[tuple[str, str]]
    depositors: str | list[str] | None = None
    license: str | None = None
    licensors: str | list[str] | None = None
    metadata_creators: str | list[str] | None = None
    rights_holders: str | list[str] | None = None
    is_part_of: str | None = None
    accepted_date: str | None = None
    curators: str | list[str] | None = None
    descriptions: list[tuple[str, str]] = field(default_factory=list)
    language: str | None = None
    principal_investigators: str | list[str] | None = None
    related_disciplines: str | list[str] | None = None
    transfer_date: str | None = None
    binary_size: int | None = None
    creators: str | list[str] | None = None
    actors: list[dict[str, str | list[str]]] | None = None
    spatial_coverages: list[dict[str, str | list[str]]] | None = None
    has_publications: list[tuple[Entity, str]] | None = None

    @classmethod
    def construct(
            cls,
            entity: Entity,
            type_name: str,
            relations: list[dict[str, Any]],
            publications: list[tuple[Entity, str]],
            license_: str) -> 'ArcheFileMetadata':
        metadata = app.config['ARCHE_METADATA']
        part_of = "https://id.acdh.oeaw.ac.at/" \
            f"{metadata['topCollection'].replace(' ', '_')}"
        titles = [(entity.name, 'und')]
        file_info = (g.files[entity.id].suffix[1:], g.files[entity.id].name)
        obj = cls(
            uri=f"{part_of}/{type_name.replace(' ', '_')}/"
                f"{file_info[0]}/{file_info[1]}",
            titles=titles)
        obj.depositors = metadata['depositor']
        obj.language = metadata['language']
        obj.license = license_
        obj.licensors = entity.license_holder
        obj.metadata_creators = metadata['hasMetadataCreator']
        obj.rights_holders = entity.license_holder
        obj.creators = entity.creator
        obj.is_part_of = part_of
        obj.accepted_date = metadata['acceptedDate']
        obj.curators = metadata['curator']
        obj.descriptions = [(entity.description, 'und')]
        obj.principal_investigators = metadata['principalInvestigator']
        obj.related_disciplines = metadata['relatedDiscipline']
        obj.transfer_date = datetime.today().strftime('%Y-%m-%d')
        obj.binary_size = g.files[entity.id].stat().st_size
        actors = []
        places = []
        if relations:
            for relation in relations:
                ref_system_info: list[tuple[str, str]] = []
                for ref in relation['ref_systems']:
                    if (ref['referenceSystem']
                            in metadata['excludeReferenceSystems']):
                        continue
                    ref_system_info.append(
                        (ref['identifier'], ref['referenceSystem']))
                values = {
                    'id': str(relation['entity'].id),
                    'name': relation['entity'].name,
                    'reference_systems': ref_system_info,
                    'description': relation['entity'].description}
                if relation['entity'].class_.group['name'] == 'place':
                    places.append(values)
                if relation['entity'].class_.group['name']  == 'actor':
                    actors.append(values)
        obj.actors = actors
        obj.spatial_coverages = places
        obj.has_publications = publications
        return obj
