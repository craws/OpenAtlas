from __future__ import annotations

import mimetypes
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import g
from unidecode import unidecode

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.rights_holder import RightsHolder

ARCHE_HOSTING_URI = 'https://id.acdh.oeaw.ac.at/arche'
ARCHE_ACCESS_PUBLIC = (
    'https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public')
ARCHE_ACCESS_RESTRICTED = (
    'https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/restricted')
ARCHE_CATEGORY_BASE = 'https://vocabs.acdh.oeaw.ac.at/archecategory/'
ARCHE_3D_EXTENSIONS = {'obj', 'ply', 'glb', 'gltf', 'stl', 'fbx', 'dae', '3ds'}
ARCHE_DATASET_EXTENSIONS = {
    'sql', 'ttl', 'nt', 'rdf', 'xml', 'json', 'csv', 'tsv', 'geojson', 'gpkg'}
ARCHE_TEXT_EXTENSIONS = {'pdf', 'txt', 'md', 'doc', 'docx', 'odt', 'rtf'}


def normalize_extension(ext: str) -> str:
    ext = ext.lower().lstrip('.')
    return 'jpeg' if ext == 'jpg' else ext


def slugify_arche_segment(value: str) -> str:
    ascii_value = unidecode(value.strip())
    cleaned = re.sub(r'[^A-Za-z0-9._-]+', '_', ascii_value).strip('_').lower()
    return '' if cleaned in {'.', '..'} else cleaned


def get_arche_slug(metadata: dict[str, Any]) -> str:
    raw = (
        metadata.get('projectAcronym')
        or metadata.get('topCollection')
        or '')
    return slugify_arche_segment(str(raw))


def get_arche_top_uri(metadata: dict[str, Any]) -> str:
    slug = get_arche_slug(metadata) or 'openatlas'
    return f'https://id.acdh.oeaw.ac.at/{slug}'


ISO_LANG_VOCABS = {2: 'iso6391', 3: 'iso6393'}


def normalize_language_uri(lang: str | None) -> str | None:
    if not lang:
        return None
    cleaned = lang.strip()
    if cleaned.startswith(('http://', 'https://')):
        return cleaned
    code = cleaned.lower()
    if code.isalpha() and (vocab := ISO_LANG_VOCABS.get(len(code))):
        return f'https://vocabs.acdh.oeaw.ac.at/{vocab}/{code}'
    return None


def get_literal_lang(metadata: dict[str, Any]) -> str:
    lang = str(metadata.get('language') or '').strip().lower()
    if lang.isalpha() and len(lang) in ISO_LANG_VOCABS:
        return lang
    return 'und'


def get_mime_format(file_path: Path, ext: str) -> str:
    overrides = {
        'sql': 'application/sql',
        'ttl': 'text/turtle',
        'nt': 'application/n-triples',
        'geojson': 'application/geo+json',
        'gpkg': 'application/geopackage+sqlite3'}
    if ext in overrides:
        return overrides[ext]
    guessed, _ = mimetypes.guess_type(str(file_path))
    return guessed or 'application/octet-stream'


def get_arche_category(ext: str, mime_type: str) -> str:
    category = 'dataset'
    if ext in ARCHE_DATASET_EXTENSIONS:
        category = 'dataset'
    elif ext in ARCHE_3D_EXTENSIONS or mime_type.startswith('model/'):
        category = '3dData'
    elif mime_type.startswith('image/'):
        category = 'image'
    elif mime_type.startswith('audio/'):
        category = 'sound'
    elif mime_type.startswith('video/'):
        category = 'audioVisual'
    elif (ext in ARCHE_TEXT_EXTENSIONS
            or mime_type.startswith('text/')
            or mime_type == 'application/pdf'):
        category = 'text'
    return f'{ARCHE_CATEGORY_BASE}{category}'


@dataclass
class ArcheTopCollection:
    uri: str
    titles: list[tuple[str, str]]
    descriptions: list[tuple[str, str]] | None = None
    subjects: list[tuple[str, str]] | None = None
    license_summary: tuple[str, str] | None = None
    depositors: str | list[str] | None = None
    curators: str | list[str] | None = None
    editors: str | list[str] | None = None
    contacts: str | list[str] | None = None
    owners: str | list[str] | None = None
    rights_holders: str | list[str] | None = None
    licensors: str | list[str] | None = None
    metadata_creators: str | list[str] | None = None
    principal_investigators: str | list[str] | None = None
    related_disciplines: str | list[str] | None = None
    language: str | None = None
    life_cycle_status: str | None = None
    extent: tuple[str, str] | None = None
    used_software: str | None = None
    url: str | None = None
    accepted_date: str | None = None
    submission_date: str | None = None
    transfer_date: str | None = None
    hosting: str = ARCHE_HOSTING_URI

    @classmethod
    def construct(
            cls,
            extent: str,
            license_summary: str) -> 'ArcheTopCollection':
        metadata = app.config['ARCHE_METADATA']
        slug = get_arche_slug(metadata)
        title = (
            metadata.get('topCollection')
            or g.settings.get('site_name')
            or slug
            or 'OpenAtlas')
        lang = get_literal_lang(metadata)
        desc = metadata.get('description')
        subjects = [
            (str(item), 'und')
            for item in metadata.get('subject', [])
            if item]
        summary = metadata.get('licenseSummary') or license_summary
        return cls(
            uri=get_arche_top_uri(metadata),
            titles=[(str(title), lang)],
            descriptions=[(str(desc), lang)] if desc else None,
            subjects=subjects or None,
            license_summary=(str(summary), 'und') if summary else None,
            depositors=metadata.get('depositor') or None,
            curators=metadata.get('curator') or None,
            editors=metadata.get('editor') or None,
            contacts=metadata.get('contact') or None,
            owners=metadata.get('owner') or None,
            rights_holders=metadata.get('rightsHolder') or None,
            licensors=metadata.get('licensor') or None,
            metadata_creators=metadata.get('hasMetadataCreator') or None,
            principal_investigators=(
                metadata.get('principalInvestigator') or None),
            related_disciplines=metadata.get('relatedDiscipline') or None,
            language=normalize_language_uri(metadata.get('language')),
            life_cycle_status=metadata.get('lifeCycleStatus') or None,
            extent=(extent, 'und') if extent else None,
            used_software=f"OpenAtlas {app.config['VERSION']}",
            url=metadata.get('url') or None,
            accepted_date=metadata.get('acceptedDate') or None,
            submission_date=metadata.get('submissionDate') or None,
            transfer_date=datetime.today().strftime('%Y-%m-%d'))


@dataclass
class ArcheCollection:
    uri: str
    is_part_of: str
    filename: str
    titles: list[tuple[str, str]]
    license_summary: tuple[str, str] | None = None
    extent: tuple[str, str] | None = None
    depositors: str | list[str] | None = None
    curators: str | list[str] | None = None
    contacts: str | list[str] | None = None
    owners: str | list[str] | None = None
    metadata_creators: str | list[str] | None = None
    principal_investigators: str | list[str] | None = None
    related_disciplines: str | list[str] | None = None
    language: str | None = None
    life_cycle_status: str | None = None
    accepted_date: str | None = None
    submission_date: str | None = None
    transfer_date: str | None = None
    hosting: str = ARCHE_HOSTING_URI

    @classmethod
    def construct(
            cls,
            *,
            uri: str,
            is_part_of: str,
            filename: str,
            title: str,
            extent: str,
            license_summary: str) -> 'ArcheCollection':
        metadata = app.config['ARCHE_METADATA']
        summary = metadata.get('licenseSummary') or license_summary
        return cls(
            uri=uri,
            is_part_of=is_part_of,
            filename=filename,
            titles=[(title, 'und')],
            license_summary=(str(summary), 'und') if summary else None,
            extent=(extent, 'und') if extent else None,
            depositors=metadata.get('depositor') or None,
            curators=metadata.get('curator') or None,
            contacts=metadata.get('contact') or None,
            owners=metadata.get('owner') or None,
            metadata_creators=metadata.get('hasMetadataCreator') or None,
            principal_investigators=(
                metadata.get('principalInvestigator') or None),
            related_disciplines=metadata.get('relatedDiscipline') or None,
            language=normalize_language_uri(metadata.get('language')),
            life_cycle_status=metadata.get('lifeCycleStatus') or None,
            accepted_date=metadata.get('acceptedDate') or None,
            submission_date=metadata.get('submissionDate') or None,
            transfer_date=datetime.today().strftime('%Y-%m-%d'))


@dataclass
class ArcheFileMetadata:
    uri: str
    titles: list[tuple[str, str]]
    filename: str = ''
    mime_format: str = ''
    category: str = ''
    access_restriction: str = ARCHE_ACCESS_PUBLIC
    hosting: str = ARCHE_HOSTING_URI
    is_part_of: str | None = None
    is_title_image_of: str | None = None
    depositors: str | list[str] | None = None
    license: str | None = None
    licensors: list[RightsHolder] | list[str] | str | None = None
    rights_holders: list[RightsHolder] | list[str] | str | None = None
    creators: list[RightsHolder] | list[str] | str | None = None
    owners: str | list[str] | None = None
    metadata_creators: str | list[str] | None = None
    accepted_date: str | None = None
    submission_date: str | None = None
    curators: str | list[str] | None = None
    descriptions: list[tuple[Any, str]] | None = None
    language: str | None = None
    principal_investigators: str | list[str] | None = None
    related_disciplines: str | list[str] | None = None
    transfer_date: str | None = None
    binary_size: int | None = None
    actors: list[dict[str, Any]] | None = None
    spatial_coverages: list[dict[str, Any]] | None = None
    has_publications: list[tuple[Entity, str]] | None = None

    @classmethod
    def construct(
            cls,
            entity: Entity,
            type_slug: str | None,
            relations: list[dict[str, Any]],
            publications: list[tuple[Entity, str]],
            license_: list[str] | str) -> 'ArcheFileMetadata':
        metadata = app.config['ARCHE_METADATA']
        top_uri = get_arche_top_uri(metadata)
        file_path = g.files[entity.id]
        ext = normalize_extension(file_path.suffix)
        file_name = file_path.name
        parent_uri = (
            f'{top_uri}/{type_slug}/{ext}'
            if type_slug else f'{top_uri}/{ext}')
        mime_format = get_mime_format(file_path, ext)
        primary_license = (
            license_[0] if isinstance(license_, list) else license_)
        logo_id = str(g.settings.get('logo_file_id', ''))
        is_title_image_of = (
            top_uri if logo_id and str(entity.id) == logo_id else None)
        excluded_refs = metadata.get('excludeReferenceSystems', [])
        actors = []
        places = []
        for relation in relations or []:
            ref_system_info: list[tuple[str, str]] = []
            for ref in relation['ref_systems']:
                if ref['referenceSystem'] in excluded_refs:
                    continue
                ref_system_info.append(
                    (ref['identifier'], ref['referenceSystem']))
            values = {
                'id': str(relation['entity'].id),
                'name': relation['entity'].name,
                'class_name': relation['entity'].class_.name,
                'reference_systems': ref_system_info,
                'description': relation['entity'].description}
            if relation['entity'].class_.group['name'] == 'place':
                places.append(values)
            if relation['entity'].class_.group['name'] == 'actor':
                actors.append(values)
        return cls(
            uri=f'{parent_uri}/{file_name}',
            titles=[(entity.name, 'und')],
            filename=file_name,
            mime_format=mime_format,
            category=get_arche_category(ext, mime_format),
            access_restriction=(
                ARCHE_ACCESS_PUBLIC
                if entity.public else ARCHE_ACCESS_RESTRICTED),
            is_part_of=parent_uri,
            is_title_image_of=is_title_image_of,
            depositors=metadata.get('depositor') or None,
            license=primary_license,
            licensors=(
                entity.license_holder or metadata.get('licensor') or None),
            rights_holders=(
                entity.license_holder
                or metadata.get('rightsHolder')
                or None),
            creators=entity.creator or None,
            owners=metadata.get('owner') or None,
            metadata_creators=metadata.get('hasMetadataCreator') or None,
            accepted_date=metadata.get('acceptedDate') or None,
            submission_date=metadata.get('submissionDate') or None,
            curators=metadata.get('curator') or None,
            descriptions=(
                [(entity.description, 'und')]
                if entity.description else None),
            language=normalize_language_uri(metadata.get('language')),
            principal_investigators=(
                metadata.get('principalInvestigator') or None),
            related_disciplines=metadata.get('relatedDiscipline') or None,
            transfer_date=datetime.today().strftime('%Y-%m-%d'),
            binary_size=file_path.stat().st_size,
            actors=actors,
            spatial_coverages=places,
            has_publications=publications)

    @classmethod
    def construct_dump(
            cls,
            filename: str,
            file_path: Path,
            title: str) -> 'ArcheFileMetadata':
        metadata = app.config['ARCHE_METADATA']
        top_uri = get_arche_top_uri(metadata)
        ext = normalize_extension(file_path.suffix)
        mime_format = get_mime_format(file_path, ext)
        return cls(
            uri=f'{top_uri}/{filename}',
            titles=[(title, 'und')],
            filename=filename,
            mime_format=mime_format,
            category=get_arche_category(ext, mime_format),
            access_restriction=ARCHE_ACCESS_PUBLIC,
            is_part_of=top_uri,
            depositors=metadata.get('depositor') or None,
            license=metadata.get('datasetLicense') or None,
            licensors=(
                metadata.get('licensor')
                or metadata.get('depositor')
                or None),
            rights_holders=(
                metadata.get('rightsHolder')
                or metadata.get('depositor')
                or None),
            owners=metadata.get('owner') or None,
            metadata_creators=metadata.get('hasMetadataCreator') or None,
            accepted_date=metadata.get('acceptedDate') or None,
            submission_date=metadata.get('submissionDate') or None,
            curators=metadata.get('curator') or None,
            language=normalize_language_uri(metadata.get('language')),
            principal_investigators=(
                metadata.get('principalInvestigator') or None),
            related_disciplines=metadata.get('relatedDiscipline') or None,
            transfer_date=datetime.today().strftime('%Y-%m-%d'),
            binary_size=file_path.stat().st_size)
