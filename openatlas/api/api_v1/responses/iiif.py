from openatlas.api.api_v1.models.util import ErrorResponse

iiif_manifest_response = {
    200: {
        "description": "IIIF Manifest JSON (v2 or v3)",
        "content": {
            "application/json": {}}},
    403: {
        "description": "Forbidden: file without license or not marked as "
                       "publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    404: {
        "description": "File or annotation not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    422: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}

iiif_canvas_response = {
    200: {
        "description": "IIIF Canvas JSON",
        "content": {
            "application/json": {}}},
    403: {
        "description": "Forbidden: file without license or not marked "
                       "as publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    404: {
        "description": "File not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    422: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}

iiif_image_response = {
    200: {
        "description": "IIIF Image annotation JSON",
        "content": {
            "application/json": {}}},
    403: {
        "description": "Forbidden: file without license or not marked as "
                       "publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    404: {
        "description": "File not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    422: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}

iiif_annotation_list_response = {
    200: {
        "description": "IIIF Annotation List (v2) or Annotation Page (v3)",
        "content": {
            "application/json": {}}},
    403: {
        "description": "Forbidden: file without license or not marked as "
                       "publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    404: {
        "description": "File not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    422: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}

iiif_annotation_response = {
    200: {
        "description": "IIIF Annotation JSON",
        "content": {
            "application/json": {}}},
    403: {
        "description": "Forbidden: file without license or not marked as "
                       "publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    404: {
        "description": "Annotation or file not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    422: {
        "description": "Validation error: unsupported IIIF version "
                       "(must be '2' or '3')."}}
