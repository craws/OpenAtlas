from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.error_handlers import (
    abort_file_not_found,
    abort_id_does_not_exist,
    abort_unsupported_iiif_version,
    register_error_handlers)
from openatlas.api.api_v1.models.iiif import (
    AnnotationIiifPath,
    FileIiifPath)
from openatlas.api.api_v1.openapi_tags import iiif_tag
from openatlas.api.api_v1.responses.iiif import (
    iiif_annotation_list_response,
    iiif_annotation_response,
    iiif_canvas_response,
    iiif_image_response,
    iiif_manifest_response)
from openatlas.api.api_v1.util.files import check_file_access, get_file_entity
from openatlas.api.api_v1.util.iiif_manifest import (
    build_annotation,
    build_annotation_list,
    build_canvas,
    build_image,
    build_manifest_v2,
    build_manifest_v3)
from openatlas.models.annotation import AnnotationImage

api_v1_iiif = APIBlueprint(
    'api_v1_iiif',
    __name__,
    url_prefix='/api/1/iiif')
register_error_handlers(api_v1_iiif)


@api_v1_iiif.get(
    '/<int:id>/manifest/<string:version>',
    summary="Get IIIF Manifest",
    tags=[iiif_tag],
    responses=iiif_manifest_response)
def get_iiif_manifest(path: FileIiifPath):
    """Returns the IIIF manifest for a specific file and IIIF version."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)
    entity = get_file_entity(path.id)
    check_file_access(entity)
    if path.version == '3':
        return build_manifest_v3(entity)
    return build_manifest_v2(entity)


@api_v1_iiif.get(
    '/<int:id>/canvas/<string:version>',
    summary="Get IIIF Canvas",
    tags=[iiif_tag],
    responses=iiif_canvas_response)
def get_iiif_canvas(path: FileIiifPath):
    """Returns the IIIF canvas for a specific file and IIIF version."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)
    entity = get_file_entity(path.id)
    check_file_access(entity)
    if not entity:
        abort_file_not_found(entity.id)
    return build_canvas(entity, version=int(path.version))


@api_v1_iiif.get(
    '/<int:id>/image/<string:version>',
    summary="Get IIIF Image",
    tags=[iiif_tag],
    responses=iiif_image_response)
def get_iiif_image(path: FileIiifPath):
    """Returns the IIIF image (annotation) for a specific file and version."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)
    entity = get_file_entity(path.id)
    check_file_access(entity)
    if not entity:
        abort_file_not_found(path.id)
    return build_image(entity, version=int(path.version))


@api_v1_iiif.get(
    '/<int:id>/annotation-list/<string:version>',
    summary="Get IIIF Annotation List/Page",
    tags=[iiif_tag],
    responses=iiif_annotation_list_response)
def get_iiif_annotation_list(path: FileIiifPath):
    """Returns the IIIF annotation list (v2) or page (v3)."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)
    entity = get_file_entity(path.id)
    check_file_access(entity)
    if not entity:
        abort_file_not_found(path.id)
    return build_annotation_list(entity, version=int(path.version))


@api_v1_iiif.get(
    '/<int:id>/annotation/<string:version>',
    summary="Get IIIF Annotation",
    tags=[iiif_tag],
    responses=iiif_annotation_response)
def get_iiif_annotation(path: AnnotationIiifPath):
    """Returns a specific IIIF annotation."""
    if path.version not in ['2', '3']:
        abort_unsupported_iiif_version(path.version)
    annotation = AnnotationImage.get_by_id(path.id)
    if not annotation:
        abort_id_does_not_exist(path.id)
    image_entity = get_file_entity(annotation.image_id)
    check_file_access(image_entity)
    return build_annotation(annotation, version=int(path.version))
