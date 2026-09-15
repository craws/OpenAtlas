from openatlas.api.api_v1.models.files import PublicFileOverviewResponse

public_files_response = {200: PublicFileOverviewResponse}

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
