from http import HTTPStatus
from typing import Any

from flask import Response
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.error_handlers import (
    abort_not_found, register_error_handlers)
from openatlas.api.api_v1.models.iiif import (
    AnnotationIiifPath, FileIiifPath)
from openatlas.api.api_v1.openapi_tags import iiif_tag
from openatlas.api.api_v1.responses.iiif import (
    IIIF_CONTENT_TYPE, iiif_annotation_list_response,
    iiif_annotation_response,
    iiif_canvas_response, iiif_georeference_response, iiif_image_response,
    iiif_manifest_response)
from openatlas.api.api_v1.util.files import check_file_access, get_file_entity
from openatlas.api.api_v1.util.iiif_manifest import (
    build_annotation, build_annotation_list, build_canvas,
    build_georeference, build_image, build_manifest)
from openatlas.database.annotation import get_annotation_image_by_id
from openatlas.models.annotation import AnnotationImage

api_v1_iiif = APIBlueprint(
    'api_v1_iiif',
    __name__,
    url_prefix='/api/1/iiif',
    abp_security=[{'bearerAuth': []}])
register_error_handlers(api_v1_iiif)


@api_v1_iiif.after_request
def set_iiif_content_type(response: Response) -> Response:
    if (response.status_code == HTTPStatus.OK
            and response.mimetype == 'application/json'):
        response.headers['Content-Type'] = IIIF_CONTENT_TYPE
    return response


@api_v1_iiif.get(
    '/<int:id>/manifest',
    summary="Get IIIF Manifest",
    tags=[iiif_tag],
    responses=iiif_manifest_response)  # type: ignore[arg-type]
def get_iiif_manifest(path: FileIiifPath) -> dict[str, Any]:
    """Returns the IIIF Presentation 3 manifest for a specific file."""
    entity = get_file_entity(path.id)
    check_file_access(entity)
    return build_manifest(entity)


@api_v1_iiif.get(
    '/<int:id>/canvas',
    summary="Get IIIF Canvas",
    tags=[iiif_tag],
    responses=iiif_canvas_response)  # type: ignore[arg-type]
def get_iiif_canvas(path: FileIiifPath) -> dict[str, Any]:
    """Returns the IIIF Presentation 3 canvas for a specific file."""
    entity = get_file_entity(path.id)
    check_file_access(entity)
    return build_canvas(entity)


@api_v1_iiif.get(
    '/<int:id>/image',
    summary="Get IIIF Image",
    tags=[iiif_tag],
    responses=iiif_image_response)  # type: ignore[arg-type]
def get_iiif_image(path: FileIiifPath) -> dict[str, Any]:
    """Returns the IIIF Presentation 3 image annotation for a file."""
    entity = get_file_entity(path.id)
    check_file_access(entity)
    return build_image(entity)


@api_v1_iiif.get(
    '/<int:id>/annotation-page',
    summary="Get IIIF Annotation Page",
    tags=[iiif_tag],
    responses=iiif_annotation_list_response)  # type: ignore[arg-type]
def get_iiif_annotation_list(path: FileIiifPath) -> dict[str, Any]:
    """Returns the IIIF Presentation 3 annotation page for a file."""
    entity = get_file_entity(path.id)
    check_file_access(entity)
    return build_annotation_list(entity)


@api_v1_iiif.get(
    '/<int:id>/georeference',
    summary="Get IIIF Georeference Annotation Page",
    tags=[iiif_tag],
    responses=iiif_georeference_response)  # type: ignore[arg-type]
def get_iiif_georeference(path: FileIiifPath) -> dict[str, Any]:
    """Returns a IIIF georeference annotation page for a file."""
    entity = get_file_entity(path.id)
    check_file_access(entity)
    return build_georeference(entity)


@api_v1_iiif.get(
    '/annotation/<int:id>',
    summary="Get IIIF Annotation",
    tags=[iiif_tag],
    responses=iiif_annotation_response)  # type: ignore[arg-type]
def get_iiif_annotation(path: AnnotationIiifPath) -> dict[str, Any]:
    """Returns a specific IIIF annotation."""
    if not (data := get_annotation_image_by_id(path.id)):
        abort_not_found(path.id)
    annotation = AnnotationImage(data)
    image_entity = get_file_entity(annotation.image_id)
    check_file_access(image_entity)
    return build_annotation(annotation)
