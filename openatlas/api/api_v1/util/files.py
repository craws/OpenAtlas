from __future__ import annotations

import mimetypes
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, cast
from uuid import UUID

from flask import g, url_for

from openatlas.api.api_v1.entity import get_entity_by_id
from openatlas.api.api_v1.error_handlers import (
    abort_file_not_found,
    abort_file_not_public,
    abort_file_without_license,
    abort_id_not_a_file)
from openatlas.api.api_v1.formatters.lod_util import \
    get_iiif_manifest_and_path
from openatlas.api.api_v1.models.files import FileItem, LicenseItem
from openatlas.models.entity import Entity


def get_license_url_mapping() -> dict[int, list[str]]:
    if not hasattr(g, 'license_url_mapping'):
        links = Entity.get_links_of_entities(
            list(get_valid_license_ids()),
            'P67',
            ['external_reference', 'reference_system'],
            inverse=True)
        license_mapping: dict[int, list[str]] = defaultdict(list)
        sorted_links = sorted(
            links,
            key=lambda l: l.domain.class_.name != 'external_reference')
        for link_ in sorted_links:
            url = None
            if link_.domain.class_.name == 'reference_system':
                system = g.reference_systems.get(link_.domain.id)
                if system:
                    url = f"{system.resolver_url or ''}{link_.description}"
            else:
                url = link_.domain.name
            if url and url not in license_mapping[link_.range.id]:
                license_mapping[link_.range.id].append(url)

        g.license_url_mapping = dict(license_mapping)
    return g.license_url_mapping

def get_valid_license_ids() -> set[int]:
    if not hasattr(g, 'valid_license_ids'):
        valid_ids = set()
        hierarchy = Entity.get_hierarchy('License')
        if hierarchy:
            type_sub_ids = list(hierarchy.subs)
            while type_sub_ids:
                current_id = type_sub_ids.pop()
                valid_ids.add(current_id)
                entity = g.types.get(current_id)
                if entity and getattr(entity, 'subs', None):
                    type_sub_ids.extend(entity.subs)
        g.valid_license_ids = valid_ids
    return g.valid_license_ids


def get_public_share_yes_id() -> int | None:
    if not hasattr(g, 'public_share_yes_id'):
        yes_id = None
        share_hierarchy = Entity.get_hierarchy('Public sharing allowed')
        if share_hierarchy:
            for sub_id in share_hierarchy.subs:
                entity = g.types.get(sub_id)
                if entity and entity.name == 'Yes':
                    yes_id = sub_id
                    break
        g.public_share_yes_id = yes_id
    return g.public_share_yes_id


def has_file_access(file_entity: Entity) -> bool:
    file_type_ids = {type_.id for type_ in file_entity.types if type_}
    has_license = bool(file_type_ids & get_valid_license_ids())
    is_public_shareable = get_public_share_yes_id() in file_type_ids
    return has_license and is_public_shareable


def check_file_access(file_entity: Entity) -> bool:
    file_type_ids = {type_.id for type_ in file_entity.types if type_}

    has_license = bool(file_type_ids & get_valid_license_ids())
    is_public_shareable = get_public_share_yes_id() in file_type_ids

    if not has_license:
        abort_file_without_license(file_entity.id)

    if not is_public_shareable:
        abort_file_not_public(file_entity.id)

    return True


def get_file_entity(file_id: int) -> Entity:
    entity = get_entity_by_id(file_id, types=True, with_location=False)
    if entity.class_.name != 'file':
        abort_id_not_a_file(file_id)
    return entity


def get_license_item(license_type: Entity) -> LicenseItem:
    license_urls = get_license_url_mapping().get(license_type.id)
    return LicenseItem(
        id=license_type.id,
        name=license_type.name,
        url=license_urls[0] if license_urls else None)


def get_license_id(file_entity: Entity) -> int | None:
    file_type_ids = {type_.id for type_ in file_entity.types if type_}
    licenses = file_type_ids & get_valid_license_ids()
    return next(iter(licenses), None)


def get_file_path(file_id: int, upload_path: Path) -> Path | Any:
    safe_extensions = {
        '.jpg', '.png', '.jpeg', '.pdf', '.tif', '.tiff', '.bmp', '.gif',
        '.svg', '.mp4', '.avi', '.mov', '.wmv', '.mp3'}

    configured_exts = g.settings.get('file_upload_allowed_extension', [])
    extensions = safe_extensions | set(configured_exts)

    for ext in extensions:
        candidate = upload_path / f"{file_id}{ext}"
        if candidate.is_file():
            return candidate

    fallback_file = next(upload_path.glob(f"{file_id}.*"), None)

    if fallback_file and fallback_file.is_file():
        return fallback_file

    abort_file_not_found(file_id)


def get_multiple_file_paths(
        file_ids: list[int],
        upload_path: Path) -> dict[int, Path]:
    safe_extensions = {
        '.jpg', '.png', '.jpeg', '.pdf', '.tif', '.tiff', '.bmp', '.gif',
        '.svg', '.mp4', '.avi', '.mov', '.wmv', '.mp3'}

    configured_exts = g.settings.get('file_upload_allowed_extension', [])
    extensions = safe_extensions | set(configured_exts)

    results = {}
    missing_ids = set(file_ids)

    for id_ in list(missing_ids):
        for ext in extensions:
            candidate = upload_path / f"{id_}{ext}"
            if candidate.is_file():
                results[id_] = candidate
                missing_ids.remove(id_)
                break

    if missing_ids:
        with os.scandir(upload_path) as entries:
            for entry in entries:
                if entry.is_file():
                    name_parts = entry.name.split('.', 1)
                    if name_parts[0].isdigit():
                        id_ = int(name_parts[0])
                        if id_ in missing_ids:
                            results[id_] = Path(entry.path)
                            missing_ids.remove(id_)
                            if not missing_ids:
                                break

    return results


def get_file_item(entity: Entity) -> FileItem:
    file_ = g.files.get(entity.id)
    mimetype, _ = mimetypes.guess_type(file_) if file_ else (None, None)
    iiif = get_iiif_manifest_and_path(entity.id)
    return FileItem(
        id=entity.id,
        name=entity.name,
        uuid=cast(UUID, entity.uuid),
        public_shareable=entity.public,
        license=get_license_item(g.types[get_license_id(entity)]),
        mimetype=mimetype,
        extension=file_.suffix if file_ else None,
        file_url=url_for(
            'api_v1_files.display_file', id=entity.id, _external=True),
        thumbnail_url=url_for(
            'api_v1_files.display_thumbnail', id=entity.id, _external=True),
        iiif_manifest_url=iiif['IIIFManifest'] or None,
        iiif_base_url=iiif['IIIFBasePath'] or None,
        creators=[],
        license_holders=[])

