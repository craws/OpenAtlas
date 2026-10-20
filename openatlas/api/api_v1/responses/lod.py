from openatlas.api.api_v1.models.lod import \
    LinkedArtCollectionResponse, LinkedArtResponse
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

context_responses = {
    200: {
        'description': 'OpenAtlas JSON-LD @context definition',
        'content': {
            'application/ld+json': {'schema': {'type': 'object'}}}}}

ontology_responses = {
    200: {
        'description': 'OpenAtlas Extension Ontology in RDF formats',
        'content': {
            'application/ld+json': {'schema': {'type': 'object'}},
            'text/turtle': {'schema': {'type': 'string'}},
            'application/n-triples': {'schema': {'type': 'string'}},
            'application/rdf+xml': {'schema': {'type': 'string'}}}}}

dump_responses = {
    200: {
        'description': 'Full Linked Open Data dump in N-Triples format (streamed)',
        'content': {
            'application/n-triples': {'schema': {'type': 'string'}}}},
    401: {
        'description': 'Authentication required. Provide a valid Bearer token or log in.',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}

la_dump_responses = {
    200: {
        'description': 'Full Linked Art dump (streamed as JSON Lines or N-Triples)',
        'content': {
            'application/x-ndjson': {'schema': {'type': 'string'}},
            'application/n-triples': {'schema': {'type': 'string'}}}},
    401: {
        'description': 'Authentication required. Provide a valid Bearer token or log in.',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
