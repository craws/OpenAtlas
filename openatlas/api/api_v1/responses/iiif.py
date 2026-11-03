from http import HTTPStatus

from openatlas.api.api_v1.models.util import ErrorResponse

iiif_manifest_response = {
    HTTPStatus.OK: {
        "description": "IIIF Manifest JSON (v2 or v3)",
        "content": {
            "application/json": {}}},
    HTTPStatus.FORBIDDEN: {
        "description": "Forbidden: file without license or not marked as "
                       "publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.NOT_FOUND: {
        "description": "File or annotation not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.UNPROCESSABLE_CONTENT: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}

iiif_canvas_response = {
    HTTPStatus.OK: {
        "description": "IIIF Canvas JSON",
        "content": {
            "application/json": {}}},
    HTTPStatus.FORBIDDEN: {
        "description": "Forbidden: file without license or not marked "
                       "as publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.NOT_FOUND: {
        "description": "File not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.UNPROCESSABLE_CONTENT: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}

iiif_image_response = {
    HTTPStatus.OK: {
        "description": "IIIF Image annotation JSON",
        "content": {
            "application/json": {}}},
    HTTPStatus.FORBIDDEN: {
        "description": "Forbidden: file without license or not marked as "
                       "publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.NOT_FOUND: {
        "description": "File not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.UNPROCESSABLE_CONTENT: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}

iiif_annotation_list_response = {
    HTTPStatus.OK: {
        "description": "IIIF Annotation List (v2) or Annotation Page (v3)",
        "content": {
            "application/json": {}}},
    HTTPStatus.FORBIDDEN: {
        "description": "Forbidden: file without license or not marked as "
                       "publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.NOT_FOUND: {
        "description": "File not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.UNPROCESSABLE_CONTENT: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}

iiif_annotation_response = {
    HTTPStatus.OK: {
        "description": "IIIF Annotation JSON",
        "content": {
            "application/json": {}}},
    HTTPStatus.FORBIDDEN: {
        "description": "Forbidden: file without license or not marked as "
                       "publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.NOT_FOUND: {
        "description": "Annotation or file not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.UNPROCESSABLE_CONTENT: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}
