from openatlas.api.api_v1.models.vocabulary import (
    VocabularyFlatItem, VocabularyFlatResponse, VocabularyTreeResponse,
    VocabularyStandardResponse)

vocabulary_list_response = {200: VocabularyFlatResponse}
vocabulary_flat_response = {200: VocabularyFlatItem}
vocabulary_tree_response = {200: VocabularyTreeResponse}
vocabulary_standard_by_class_response = {200: VocabularyStandardResponse}

vocabulary_skos_response = {
    200: {
        'description': 'Vocabulary hierarchy exported as a SKOS graph in '
                       'different RDF serialization formats.',
        'content': {
            'text/turtle': {'schema': {'type': 'string'}},
            'application/rdf+xml': {'schema': {'type': 'string'}},
            'application/ld+json': {'schema': {'type': 'string'}},
            'application/n-triples': {'schema': {'type': 'string'}}}},
    404: {
        'description': 'Type not found.',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Entity not found'}}}}}}}
