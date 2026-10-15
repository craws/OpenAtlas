from openatlas.api.api_v1.models.lod import (
    LinkedArtCollectionResponse,
    LinkedArtResponse,
)
from openatlas.api.api_v1.models.util import ErrorResponse

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
        'description': 'Entity not found.',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}

lod_collection_responses = {
    200: {
        'description': 'Collection response in different LOD '
                       'formats with OrderedCollectionPage pagination',
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
                'schema': ErrorResponse.model_json_schema()}}}}
