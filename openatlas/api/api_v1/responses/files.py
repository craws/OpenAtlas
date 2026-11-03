from http import HTTPStatus

from openatlas.api.api_v1.models.files import PublicFileOverviewResponse
from openatlas.api.api_v1.models.util import ErrorResponse

public_files_response = {
    HTTPStatus.OK: PublicFileOverviewResponse,
    HTTPStatus.NOT_FOUND: {
        "description": "Entity not found",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}}}

display_file_response = {
    HTTPStatus.OK: {
        "content": {
            "image/*": {
                "schema": {"type": "string", "format": "binary"}}},
        "description": "Returns the actual image file (JPEG, PNG, etc.)"},
    HTTPStatus.FOUND: {
        "description": "Redirects to the external IIIF Image API server when "
                       "IIIF is enabled."},
    HTTPStatus.FORBIDDEN: {
        "description": "Forbidden: file has no open license or is not marked"
                       " as publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.NOT_FOUND: {
        "description": "File not found or entity is not a file.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}}}

thumbnail_response = {
    HTTPStatus.OK: {
        "content": {
            "image/*": {
                "schema": {"type": "string", "format": "binary"}}},
        "description": "Returns the generated thumbnail image."},
    HTTPStatus.FOUND: {
        "description": "Redirects to the external IIIF thumbnail image when "
                       "IIIF is enabled."},
    HTTPStatus.FORBIDDEN: {
        "description": "Forbidden: file has no open license or is not marked "
                       "as publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.NOT_FOUND: {
        "description": "File or thumbnail not found on disk.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}}}
