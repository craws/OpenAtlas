import os
from pathlib import Path
from typing import Any

from flask import g, send_file
from flask_openapi3 import APIBlueprint

from openatlas import app
from openatlas.api.api_v1.error_handlers import abort_file_not_found, \
    abort_file_not_public, \
    abort_file_without_license, \
    abort_id_does_not_exist, \
    abort_id_not_a_file
from openatlas.api.api_v1.models.files import FileIdPath, FileIiifPath
from openatlas.api.api_v1.models.util import DownloadQuery
from openatlas.api.api_v1.openapi_tags import file_tag
from openatlas.api.api_v1.responses.files import (
    licensed_files_response, display_file_response, iiif_manifest_response,
    thumbnail_response)
from openatlas.database.api import check_file

api_v1_files = APIBlueprint('files', __name__, url_prefix='/api/1/files')


def _check_file_access(file_id: int) -> bool:
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


def _get_file_path(file_id: int, upload_path: Path) -> Path | Any:
    extensions = g.settings.get(
        'file_upload_allowed_extension',
        ['.jpg', '.png', '.jpeg', '.pdf', '.tif', '.tiff', '.bmp', '.gif',
         '.svg', '.mp4', '.avi', '.mov', '.wmv', '.mp3'])

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


@api_v1_files.get(
    '/<int:id>/display',
    summary="Get image file",
    tags=[file_tag],
    responses=display_file_response)
def display_file(path: FileIdPath, query: DownloadQuery):
    """Serves the binary image file."""
    file_id = path.id
    path = _get_file_path(file_id, app.config['UPLOAD_PATH'])
    if not path:
        abort_file_not_found(file_id)
    return send_file(path, as_attachment=bool(query.download))


@api_v1_files.get(
    '/<int:id>/thumbnail',
    summary="Get thumbnail image",
    tags=[file_tag],
    responses=thumbnail_response)
def display_thumbnail(path: FileIdPath, query: DownloadQuery):
    """Serves the static, pre-calculated thumbnail image."""
    file_id = path.id
    path = _get_file_path(
        file_id,
        app.config['RESIZED_IMAGES'] / app.config['IMAGE_SIZE']['thumbnail'])
    if not path:
        abort_file_not_found(file_id)
    return send_file(path, as_attachment=bool(query.download))


@api_v1_files.get(
    '/licensed',
    summary="Get licensed files overview",
    tags=[file_tag],
    responses=licensed_files_response)
def get_licensed_files():
    """Retrieves all existing files with a license, their display URLs,
    and metadata."""
    return {}


@api_v1_files.get(
    '/<int:id>/iiif-manifest/<string:version>',
    summary="Get IIIF Manifest",
    tags=[file_tag],
    responses=iiif_manifest_response)
def get_iiif_manifest(path: FileIiifPath):
    """Returns the IIIF manifest for a specific file and IIIF version."""
    return {}
