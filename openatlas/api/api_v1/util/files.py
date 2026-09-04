import os
from pathlib import Path
from typing import Any

from flask import g

from openatlas.api.api_v1.error_handlers import abort_file_not_found, \
    abort_file_not_public, \
    abort_file_without_license, \
    abort_id_does_not_exist, \
    abort_id_not_a_file
from openatlas.database.api import check_file


def check_file_access(file_id: int) -> bool:
    checked_file = check_file(file_id)

    if not checked_file:
        abort_id_does_not_exist(file_id)

    if checked_file['openatlas_class_name'] != 'file':
        abort_id_not_a_file(file_id)

    has_license = False
    is_public_shareable = False

    for type_id in checked_file.get('type_ids', []):
        if has_license and is_public_shareable:
            break

        type_item = g.types.get(type_id)
        if not type_item:
            continue

        if type_item.root and g.types.get(type_item.root[0]):

            if g.types[type_item.root[0]].name == 'License':
                has_license = True
                continue
            if type_item.name == 'Yes':
                if g.types[type_item.root[0]].name == 'Public sharing allowed':
                    is_public_shareable = True
                    continue

    if not has_license:
        abort_file_without_license(file_id)

    if not is_public_shareable:
        abort_file_not_public(file_id)

    return True


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

    prefix = f"{file_id}."

    try:
        with os.scandir(upload_path) as entries:
            for entry in entries:
                if entry.name.startswith(prefix) and entry.is_file():
                    return Path(entry.path)
    except FileNotFoundError:
        abort_file_not_found(file_id)
