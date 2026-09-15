from pathlib import Path

from flask import g, redirect, send_file
from flask_openapi3 import APIBlueprint

from openatlas import app
from openatlas.api.api_v1.error_handlers import (
    abort_file_not_found,
    register_error_handlers)
from openatlas.api.api_v1.models.files import (
    FileIdPath,
    PublicFileOverviewResponse)
from openatlas.api.api_v1.models.util import DownloadQuery
from openatlas.api.api_v1.openapi_tags import file_tag
from openatlas.api.api_v1.responses.files import (
    display_file_response,
    public_files_response,
    thumbnail_response)
from openatlas.api.api_v1.util.files import (
    check_file_access,
    get_file_entity,
    get_file_item,
    get_file_path,
    has_file_access)
from openatlas.display.image_processing import (
    check_iiif_activation,
    check_iiif_file_exist)
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
        return None

    if file_path.suffix.lower() not in g.display_file_ext:
        return None

    if not check_iiif_file_exist(file_id):
        return None

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
    if not actual_path:
        abort_file_not_found(entity.id)
    if not query.download:
        iiif_url = get_iiif_redirect_url(
            entity.id,
            actual_path,
            is_thumbnail=False)
        if iiif_url:
            return redirect(iiif_url)

    return send_file(
        actual_path,
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
    if not original_path:
        abort_file_not_found(entity.id)
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
    if not thumbnail_path:
        abort_file_not_found(entity.id)

    return send_file(thumbnail_path, as_attachment=bool(query.download))


# todo
@api_v1_files.get(
    '/public',
    summary="Get licensed files overview",
    tags=[file_tag],
    responses=public_files_response)
def get_public_files():
    """Retrieves all existing files with a license, their display URLs,
    and metadata."""
    entities = Entity.get_by_class(['file'], types=True)
    valid_files = [file for file in entities if has_file_access(file)]
    #file_paths = get_multiple_file_paths(
    #    [f.id for f in valid_files], app.config['UPLOAD_PATH'])
    files = []
    for file_ in valid_files:
        files.append(get_file_item(file_))
    return PublicFileOverviewResponse(data=files).model_dump(by_alias=True)
