from flask import g
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.models.files import FileIdPath, FileIiifPath
from openatlas.api.api_v1.models.util import DownloadQuery
from openatlas.api.api_v1.openapi_tags import file_tag
from openatlas.api.api_v1.responses.files import (
    licensed_files_response, display_file_response, iiif_manifest_response,
    thumbnail_response)

api_v1_files = APIBlueprint('files', __name__, url_prefix='/api/1/files')


@api_v1_files.get(
    '/<int:id>/display',
    summary="Get image file",
    tags=[file_tag],
    responses=display_file_response)
def display_file(path: FileIdPath, query: DownloadQuery):
    """Serves the binary image file."""
    file_id = path.id
    force_download = query.download

    return {}


@api_v1_files.get(
    '/<int:id>/thumbnail',
    summary="Get thumbnail image",
    tags=[file_tag],
    responses=thumbnail_response)
def get_thumbnail(path: FileIdPath, query: DownloadQuery):
    """Serves the static, pre-calculated thumbnail image."""
    file_id = path.id
    force_download = query.download

    return {}


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
