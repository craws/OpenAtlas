from openatlas.api.api_v1.models import LinkedArtResponse

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
