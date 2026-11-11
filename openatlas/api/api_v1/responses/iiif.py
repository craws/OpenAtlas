from http import HTTPStatus

from openatlas.api.api_v1.models.util import ErrorResponse

iiif_manifest_response = {
    HTTPStatus.OK: {
        "description": "IIIF Presentation 3 Manifest JSON",
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
                "schema": ErrorResponse.model_json_schema()}}}}

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
                "schema": ErrorResponse.model_json_schema()}}}}

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
                "schema": ErrorResponse.model_json_schema()}}}}

iiif_annotation_list_response = {
    HTTPStatus.OK: {
        "description": "IIIF Presentation 3 Annotation Page",
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
                "schema": ErrorResponse.model_json_schema()}}}}

iiif_georeference_response = {
    HTTPStatus.OK: {
        "description": "IIIF Georeference Annotation Page JSON",
        "content": {
            "application/json": {}}},
    HTTPStatus.FORBIDDEN: {
        "description": "Forbidden: file without license or not marked "
                       "as publicly shareable.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}},
    HTTPStatus.NOT_FOUND: {
        "description": "File or georeference not found.",
        "content": {
            "application/json": {
                "schema": ErrorResponse.model_json_schema()}}}}

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
                "schema": ErrorResponse.model_json_schema()}}}}
