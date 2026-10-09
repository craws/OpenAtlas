from pathlib import Path

from flask import g, redirect, send_file
from flask_openapi3 import APIBlueprint

from openatlas import app
from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.models.files import (
    FileIdPath, PublicFileOverviewResponse, PublicFilesQuery)
from openatlas.api.api_v1.models.util import DownloadQuery
from openatlas.api.api_v1.openapi_tags import file_tag
from openatlas.api.api_v1.responses.files import (
    display_file_response, public_files_response, thumbnail_response)
from openatlas.api.api_v1.util.files import (
    check_file_access, get_display_extensions, get_file_entity,
    get_file_item, get_file_path, get_mime_type, get_public_share_yes_id,
    get_valid_license_ids, iiif_file_exists, resolve_file_paths,
    resolve_rights_holders)
from openatlas.api.api_v1.util.pagination import get_pagination_lod
from openatlas.database.api import get_public_files_api
from openatlas.display.image_processing import check_iiif_activation
from openatlas.models.entity import Entity

api_v1_files = APIBlueprint(
    'api_v1_files',
    __name__,
    url_prefix='/api/1/files')
register_error_handlers(api_v1_files)


def get_iiif_redirect_url(
        file_id: int,
        file_path: Path,
        is_thumbnail: bool = False) -> str | None:
    if not g.settings.get('iiif') or not check_iiif_activation():
        return None  # pragma: no cover

    if file_path.suffix.lower() not in get_display_extensions():
        return None # pragma: no cover

    if not iiif_file_exists(file_id):
        return None # pragma: no cover

    iiif_ext = '.tiff' if g.settings.get('iiif_conversion') \
        else file_path.suffix
    iiif_base = f"{g.settings.get('iiif_url', '')}{file_id}{iiif_ext}"

    if is_thumbnail:
        size = app.config['IMAGE_SIZE']['thumbnail']
        return f"{iiif_base}/full/!{size},{size}/0/default.jpg"

    return f"{iiif_base}/full/max/0/default.jpg"


@api_v1_files.get(
    '/<int:id>/display',
    summary="Get image file",
    tags=[file_tag],
    responses=display_file_response)
def display_file(path: FileIdPath, query: DownloadQuery):
    """Serves the binary image file."""
    entity = get_file_entity(path.id)
    check_file_access(entity)
    actual_path = get_file_path(entity.id, app.config['UPLOAD_PATH'])
    if not query.download and check_iiif_activation():
        iiif_url = get_iiif_redirect_url(
            entity.id,
            actual_path,
            is_thumbnail=False)
        if iiif_url:
            return redirect(iiif_url)

    return send_file(
        actual_path,
        mimetype=get_mime_type(actual_path),
        as_attachment=bool(query.download),
        download_name=f"{entity.id}{actual_path.suffix}")


@api_v1_files.get(
    '/<int:id>/thumbnail',
    summary="Get thumbnail image",
    tags=[file_tag],
    responses=thumbnail_response)
def display_thumbnail(path: FileIdPath, query: DownloadQuery):
    """Serves the static, pre-calculated thumbnail image."""
    entity = get_file_entity(path.id)
    check_file_access(entity)
    original_path = get_file_path(entity.id, app.config['UPLOAD_PATH'])
    if not query.download:
        iiif_url = get_iiif_redirect_url(
            entity.id,
            original_path,
            is_thumbnail=True)
        if iiif_url:
            return redirect(iiif_url)

    thumbnail_path = get_file_path(
        entity.id,
        app.config['RESIZED_IMAGES'] / app.config['IMAGE_SIZE']['thumbnail'])

    return send_file(
        thumbnail_path,
        mimetype=get_mime_type(original_path),
        as_attachment=bool(query.download))


@api_v1_files.get(
    '/public',
    summary="Get licensed files overview",
    tags=[file_tag],
    responses=public_files_response)
def get_public_files(query: PublicFilesQuery):
    """Retrieves a page of publicly shareable files with a license."""
    rows, total = get_public_files_api(
        get_valid_license_ids(),
        get_public_share_yes_id(),
        query.limit,
        (query.page - 1) * query.limit)
    entities = [Entity(row) for row in rows]
    resolve_file_paths([entity.id for entity in entities])
    resolve_rights_holders([entity.id for entity in entities])
    pagination = get_pagination_lod(
        'api_v1_files.get_public_files', total, query.page, query.limit)
    return PublicFileOverviewResponse(
        data=[get_file_item(entity) for entity in entities],
        **pagination).model_dump(by_alias=True)
