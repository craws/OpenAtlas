from __future__ import annotations

import mimetypes
import os
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, cast
from uuid import UUID

if TYPE_CHECKING:
    from openatlas.api.api_v1.formatters.lod_util import EntityLinks

from flask import g, url_for

from openatlas import app
from openatlas.api.api_v1.entity import get_entity_by_id
from openatlas.api.api_v1.error_handlers import (
    abort_file_not_found,
    abort_file_not_public,
    abort_file_without_license,
    abort_id_not_a_file)
from openatlas.api.api_v1.models.agent import AgentItem
from openatlas.api.api_v1.models.files import FileItem, LicenseItem
from openatlas.display.image_processing import check_iiif_activation
from openatlas.display.util2 import convert_size
from openatlas.models.entity import Entity
from openatlas.models.rights_holder import RightsHolder

SAFE_FILE_EXTENSIONS = {
    '.jpg', '.png', '.jpeg', '.pdf', '.tif', '.tiff', '.bmp', '.gif',
    '.svg', '.mp4', '.avi', '.mov', '.wmv', '.mp3'}


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


def _file_extensions() -> list[str]:
    configured = g.settings.get('file_upload_allowed_extension', [])
    extensions = {
        extension if extension.startswith('.') else f'.{extension}'
        for extension in configured}
    return sorted(SAFE_FILE_EXTENSIONS | extensions)


def get_file_path(file_id: int, upload_path: Path) -> Path | Any:
    for ext in _file_extensions():
        candidate = upload_path / f"{file_id}{ext}"
        if candidate.is_file():
            return candidate

    fallback_file = next(upload_path.glob(f"{file_id}.*"), None)

    if fallback_file and fallback_file.is_file():
        return fallback_file  # pragma: no cover

    abort_file_not_found(file_id)


def get_multiple_file_paths(
        file_ids: list[int],
        upload_path: Path) -> dict[int, Path]:
    if not file_ids:
        return {}
    results = {}
    missing_ids = set(file_ids)

    for id_ in list(missing_ids):
        for ext in _file_extensions():
            candidate = upload_path / f"{id_}{ext}"
            if candidate.is_file():
                results[id_] = candidate
                missing_ids.remove(id_)
                break

    if missing_ids:
        with os.scandir(upload_path) as entries:
            for entry in entries:
                name_parts = entry.name.split('.', 1)
                if name_parts[0].isdigit():
                    id_ = int(name_parts[0])
                    if id_ in missing_ids and entry.is_file():
                        results[id_] = Path(entry.path)
                        missing_ids.remove(id_)
                        if not missing_ids:
                            break

    return results


def resolve_file_paths(ids: Iterable[int]) -> dict[int, Path]:
    if not hasattr(g, 'api_file_paths'):
        g.api_file_paths = {}
    cache: dict[int, Path | None] = g.api_file_paths
    ids = set(ids)
    if missing := [id_ for id_ in ids if id_ not in cache]:
        found = get_multiple_file_paths(missing, app.config['UPLOAD_PATH'])
        for id_ in missing:
            cache[id_] = found.get(id_)  # None is cached for missing files
    return {id_: path for id_ in ids if (path := cache[id_])}


def get_cached_file_path(id_: int) -> Path | None:
    return resolve_file_paths([id_]).get(id_)


def resolve_rights_holders(
        ids: Iterable[int]) -> dict[int, dict[str, list[RightsHolder]]]:
    if not hasattr(g, 'api_rights_holders'):
        g.api_rights_holders = {}
    cache: dict[int, dict[str, list[RightsHolder]]] = g.api_rights_holders
    ids = set(ids)
    if missing := [id_ for id_ in ids if id_ not in cache]:
        info = RightsHolder.get_rights_holder_information(missing)
        for id_ in missing:
            cache[id_] = info.get(
                id_,
                {'creator': [], 'license_holder': []})
    return {id_: cache[id_] for id_ in ids}


def prefetch_files(links_data: dict[int, EntityLinks]) -> None:
    file_ids = set()
    for item in links_data.values():
        if item.entity.class_.name == 'file':
            file_ids.add(item.entity.id)
        file_ids.update(
            link_.domain.id for link_ in item.links_inverse
            if link_.property.code == 'P67'
            and link_.domain.class_.name == 'file')
    if file_ids:
        resolve_file_paths(file_ids)
        resolve_rights_holders(file_ids)


def get_display_extensions() -> list[str]:
    extensions = list(app.config['DISPLAY_FILE_EXT'])
    if g.settings['image_processing']:
        extensions += app.config['PROCESSABLE_EXT']
    return extensions


def iiif_file_exists(id_: int) -> bool:
    if g.settings['iiif_conversion']:
        return (Path(g.settings['iiif_path']) / f'{id_}.tiff').is_file()
    return get_cached_file_path(id_) is not None


def get_file_size(id_: int) -> str:
    if path := get_cached_file_path(id_):
        return convert_size(path.stat().st_size)
    return 'N/A'


def get_agent_item(rights_holder: RightsHolder) -> AgentItem:
    return AgentItem(
        id=rights_holder.id,
        name=rights_holder.name,
        class_name=rights_holder.class_,
        description=rights_holder.description)


def get_mime_type(path: Path | None) -> str | None:
    mimetype, _ = mimetypes.guess_type(path) if path else (None, None)
    return mimetype


def get_file_item(entity: Entity) -> FileItem:
    file_ = get_cached_file_path(entity.id)
    iiif = get_iiif_manifest_and_path(entity.id)
    rights = resolve_rights_holders([entity.id])[entity.id]
    return FileItem(
        id=entity.id,
        name=entity.name,
        uuid=cast(UUID, entity.uuid),
        public_shareable=entity.public,
        license=get_license_item(g.types[get_license_id(entity)]),
        mimetype=get_mime_type(file_),
        extension=file_.suffix if file_ else None,
        file_url=url_for(
            'api_v1_files.display_file', id=entity.id, _external=True),
        thumbnail_url=url_for(
            'api_v1_files.display_thumbnail', id=entity.id, _external=True),
        iiif_manifest_url=iiif['IIIFManifest'] or None,
        iiif_base_url=iiif['IIIFBasePath'] or None,
        creators=[get_agent_item(rh) for rh in rights['creator']],
        license_holders=[
            get_agent_item(rh) for rh in rights['license_holder']])


def get_license_type(entity: Entity) -> Optional[Entity]:
    license_ = None
    for type_ in entity.types:
        if g.types[type_.root[0]].name == 'License':
            license_ = type_
            break
    return license_


def get_iiif_manifest_and_path(img_id: int) -> dict[str, str]:
    iiif_manifest = ''
    iiif_base_path = ''
    if not check_iiif_activation():
        return {'IIIFManifest': iiif_manifest, 'IIIFBasePath': iiif_base_path}
    if iiif_file_exists(img_id):
        iiif_manifest = url_for(
            'api.iiif_manifest',
            version=g.settings['iiif_version'],
            id_=img_id,
            _external=True)
        if file_ := get_cached_file_path(img_id):
            iiif_base_path = (
                f"{g.settings['iiif_url']}{img_id}{file_.suffix}")
    return {'IIIFManifest': iiif_manifest, 'IIIFBasePath': iiif_base_path}
