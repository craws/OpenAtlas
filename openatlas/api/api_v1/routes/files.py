from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.models.files import LicensedFileOverviewResponse
from openatlas.api.api_v1.openapi_tags import file_tag

api_v1_files = APIBlueprint('files', __name__, url_prefix='/api/1/files')


@api_v1_files.get(
    '/licensed',
    summary="Get licensed files overview",
    tags=[file_tag],
    responses={200: LicensedFileOverviewResponse})
def get_licensed_files():
    """Retrieves all existing files with a license, their display URLs,
    and metadata."""
    # Deine Logik hier
    return {}


@api_v1_files.get(
    '/<int:id>/display',
    summary="Get image file",
    tags=[file_tag],
    responses={
        200: {
            "content": {
                "image/*": {
                    "schema": {"type": "string", "format": "binary"}
                }
            },
            "description": "Returns the actual image file (JPEG, PNG, etc.)"
        },
        404: {"description": "File not found"}
    })
def display_file(path: dict):  # Pydantic nimmt die path-Parameter
    """Serves the binary image file."""
    file_id = path['id']
    # return send_file(...)
    return {}


@api_v1_files.get(
    '/<int:id>/iiif-manifest/<string:version>',
    summary="Get IIIF Manifest",
    tags=[file_tag],
    responses={200: {"description": "IIIF Manifest JSON"}})
def get_iiif_manifest(path: dict):
    """Returns the IIIF manifest for a specific file and IIIF version."""
    # IIIF Manifeste haben eigene sehr strikte Schemata, oft reicht es,
    # hier einfach das dict zurückzugeben, ohne ein Pydantic-Modell zu
    # erzwingen.
    return {}
