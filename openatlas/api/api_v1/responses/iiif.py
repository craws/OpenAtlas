iiif_manifest_response = {
    200: {
        "description": "IIIF Manifest JSON",
        "content": {
            "application/json": {}}},
    400: {"description": "Unsupported IIIF version"},
    403: {"description": "File without license or not shareable"},
    404: {"description": "File or annotation not found"}}

iiif_canvas_response = {
    200: {
        "description": "IIIF Canvas JSON",
        "content": {
            "application/json": {}}},
    400: {"description": "Unsupported IIIF version"},
    403: {"description": "File without license or not shareable"},
    404: {"description": "File not found"}}

iiif_image_response = {
    200: {
        "description": "IIIF Image JSON",
        "content": {
            "application/json": {}}},
    400: {"description": "Unsupported IIIF version"},
    403: {"description": "File without license or not shareable"},
    404: {"description": "File not found"}}

iiif_annotation_list_response = {
    200: {
        "description": "IIIF Annotation List/Page JSON",
        "content": {
            "application/json": {}}},
    400: {"description": "Unsupported IIIF version"},
    403: {"description": "File without license or not shareable"},
    404: {"description": "File not found"}}

iiif_annotation_response = {
    200: {
        "description": "IIIF Annotation JSON",
        "content": {
            "application/json": {}}},
    400: {"description": "Unsupported IIIF version"},
    403: {"description": "File without license or not shareable"},
    404: {"description": "Annotation or file not found"}}
