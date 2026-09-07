from openatlas.api.api_v1.models.files import LicensedFileOverviewResponse

licensed_files_response = {200: LicensedFileOverviewResponse}

display_file_response = {
    200: {
        "content": {
            "image/*": {
                "schema": {"type": "string", "format": "binary"}}},
        "description": "Returns the actual image file (JPEG, PNG, etc.)"},
    404: {"description": "File not found"}}

thumbnail_response = {
    200: {
        "content": {
            "image/*": {
                "schema": {"type": "string", "format": "binary"}}},
        "description": "Returns the generated thumbnail image."},
    404: {"description": "File or thumbnail not found"}}

iiif_manifest_response = {
    200: {
        "description": "IIIF Manifest JSON",
        "content": {
            "application/json": {}}},
    400: {"description": "Unsupported IIIF version"},
    403: {"description": "File without license or not shareable"},
    404: {"description": "File or annotation not found"}}
