from openatlas.api.api_v1.models.lod import (
    LinkedArtCollectionResponse, LinkedArtResponse)

lod_responses = {
    200: {
        'description': 'Entity response in different LOD formats',
        'content': {
            'application/ld+json': {
                'schema': LinkedArtResponse.model_json_schema()},
            'text/turtle': {'schema': {'type': 'string'}},
            'application/n-triples': {'schema': {'type': 'string'}},
            'application/rdf+xml': {'schema': {'type': 'string'}}}},
    404: {
        'description': 'Entität mit dieser UUID wurde nicht gefunden',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Entity not found'}}}}}}}

lod_collection_responses = {
    200: {
        'description': 'Collection response in different LOD formats with Hydra pagination',
        'content': {
            'application/ld+json': {
                'schema': LinkedArtCollectionResponse.model_json_schema()},
            'text/turtle': {'schema': {'type': 'string'}},
            'application/n-triples': {'schema': {'type': 'string'}},
            'application/rdf+xml': {'schema': {'type': 'string'}}}},
    404: {
        'description': 'Entity class not found',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Entity class not found'}}}}}}}
