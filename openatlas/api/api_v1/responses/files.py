from openatlas.api.api_v1.models.files import PublicFileOverviewResponse
from openatlas.api.api_v1.models.util import ErrorResponse

public_files_response = {200: PublicFileOverviewResponse}

display_file_response = {
    200: {
        "content": {
            "image/*": {
                "schema": {"type": "string", "format": "binary"}}},
        "description": "Returns the actual image file (JPEG, PNG, etc.)"},
    302: {
        "description": "Redirects to the external IIIF Image API server when "
                       "IIIF is enabled."},
    403: {
        "description": "Forbidden: file has no open license or is not marked"
                       " as publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    404: {
        "description": "File not found or entity is not a file.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}}}

thumbnail_response = {
    200: {
        "content": {
            "image/*": {
                "schema": {"type": "string", "format": "binary"}}},
        "description": "Returns the generated thumbnail image."},
    302: {
        "description": "Redirects to the external IIIF thumbnail image when "
                       "IIIF is enabled."},
    403: {
        "description": "Forbidden: file has no open license or is not marked "
                       "as publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    404: {
        "description": "File or thumbnail not found on disk.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}}}
