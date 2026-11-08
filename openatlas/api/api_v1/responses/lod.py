from http import HTTPStatus

from openatlas.api.api_v1.models.lod import \
    LinkedArtCollectionResponse, LinkedArtResponse
from openatlas.api.api_v1.models.util import ErrorResponse

lod_responses = {
    HTTPStatus.OK: {
        'description': 'Entity response in different LOD formats',
        'content': {
            'application/ld+json': {
                'schema': LinkedArtResponse.model_json_schema()},
            'text/turtle': {'schema': {'type': 'string'}},
            'application/n-triples': {'schema': {'type': 'string'}},
            'application/rdf+xml': {'schema': {'type': 'string'}}}},
    HTTPStatus.NOT_FOUND: {
        'description': 'Entity not found.',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}

lod_collection_responses = {
    HTTPStatus.OK: {
        'description': 'Collection response in different LOD '
                       'formats with OrderedCollectionPage pagination',
        'content': {
            'application/ld+json': {
                'schema': LinkedArtCollectionResponse.model_json_schema()},
            'text/turtle': {'schema': {'type': 'string'}},
            'application/n-triples': {'schema': {'type': 'string'}},
            'application/rdf+xml': {'schema': {'type': 'string'}}}},
    HTTPStatus.NOT_FOUND: {
        'description': 'Entity class not found',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
