from flask import send_file
from flask_openapi3 import APIBlueprint

from openatlas import app
from openatlas.api.api_v1.error_handlers import abort_file_not_found, \
    abort_id_does_not_exist, abort_unsupported_iiif_version
from openatlas.api.api_v1.util.files import check_file_access, get_file_path
from openatlas.api.api_v1.util.iiif_manifest import (
    build_annotation,
    build_annotation_list,
    build_canvas,
    build_image,
    build_manifest_v2,
    build_manifest_v3)
from openatlas.api.api_v1.models.files import (
    AnnotationIiifPath,
    FileIdPath,
    FileIiifPath,
    LicensedFileOverviewResponse)
from openatlas.api.api_v1.models.util import DownloadQuery
from openatlas.api.api_v1.openapi_tags import file_tag
from openatlas.api.api_v1.responses.files import (
    display_file_response,
    iiif_manifest_response,
    licensed_files_response,
    thumbnail_response)
from openatlas.models.annotation import AnnotationImage
from openatlas.models.entity import Entity

api_v1_files = APIBlueprint(
    'api_v1_files',
    __name__,
    url_prefix='/api/1/files')


# Todo: check if really faster than with normal and many images
#   if not, delete this function


@api_v1_files.get(
    '/<int:id>/display',
    summary="Get image file",
    tags=[file_tag],
    responses=display_file_response)
def display_file(path: FileIdPath, query: DownloadQuery):
    """Serves the binary image file."""
    file_id = path.id
    path = get_file_path(file_id, app.config['UPLOAD_PATH'])
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
    path = get_file_path(
        file_id,
        app.config['RESIZED_IMAGES'] / app.config['IMAGE_SIZE']['thumbnail'])
    if not path:
        abort_file_not_found(file_id)
    return send_file(path, as_attachment=bool(query.download))


@api_v1_files.get(
    '/<int:id>/iiif-manifest/<string:version>',
    summary="Get IIIF Manifest",
    tags=[file_tag],
    responses=iiif_manifest_response)
def get_iiif_manifest(path: FileIiifPath):
    """Returns the IIIF manifest for a specific file and IIIF version."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)

    check_file_access(path.id)

    entity = Entity.get_by_id(path.id, types=True)
    if not entity:
        abort_file_not_found(path.id)

    if path.version == '3':
        return build_manifest_v3(entity)
    return build_manifest_v2(entity)


@api_v1_files.get(
    '/<int:id>/iiif-canvas/<string:version>',
    summary="Get IIIF Canvas",
    tags=[file_tag],
    responses=iiif_manifest_response)
def get_iiif_canvas(path: FileIiifPath):
    """Returns the IIIF canvas for a specific file and IIIF version."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)
    check_file_access(path.id)
    entity = Entity.get_by_id(path.id, types=True)
    if not entity:
        abort_file_not_found(path.id)
    return build_canvas(entity, version=int(path.version))


@api_v1_files.get(
    '/<int:id>/iiif-image/<string:version>',
    summary="Get IIIF Image",
    tags=[file_tag],
    responses=iiif_manifest_response)
def get_iiif_image(path: FileIiifPath):
    """Returns the IIIF image (annotation) for a specific file and version."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)
    check_file_access(path.id)
    entity = Entity.get_by_id(path.id, types=True)
    if not entity:
        abort_file_not_found(path.id)
    return build_image(entity, version=int(path.version))


@api_v1_files.get(
    '/<int:id>/iiif-annotation-list/<string:version>',
    summary="Get IIIF Annotation List/Page",
    tags=[file_tag],
    responses=iiif_manifest_response)
def get_iiif_annotation_list(path: FileIiifPath):
    """Returns the IIIF annotation list (v2) or page (v3)."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)
    check_file_access(path.id)
    entity = Entity.get_by_id(path.id, types=True)
    if not entity:
        abort_file_not_found(path.id)
    return build_annotation_list(entity, version=int(path.version))


@api_v1_files.get(
    '/annotation/<int:id>/iiif/<string:version>',
    summary="Get IIIF Annotation",
    tags=[file_tag],
    responses=iiif_manifest_response)
def get_iiif_annotation(path: AnnotationIiifPath):
    """Returns a specific IIIF annotation."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)
    annotation = AnnotationImage.get_by_id(path.id)
    if not annotation:
        abort_id_does_not_exist(path.id)
    check_file_access(annotation.image_id)
    return build_annotation(annotation, version=int(path.version))


@api_v1_files.get(
    '/licensed',
    summary="Get licensed files overview",
    tags=[file_tag],
    responses=licensed_files_response)
def get_licensed_files():
    """Retrieves all existing files with a license, their display URLs,
    and metadata."""
    return LicensedFileOverviewResponse(files={}).model_dump(by_alias=True)
