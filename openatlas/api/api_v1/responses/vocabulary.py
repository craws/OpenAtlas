from http import HTTPStatus

from openatlas.api.api_v1.models.util import ErrorResponse
from openatlas.api.api_v1.models.vocabulary import (
    VocabularyFlatItem, VocabularyFlatResponse, VocabularyStandardResponse,
    VocabularyTreeResponse)

vocabulary_list_response = {HTTPStatus.OK: VocabularyFlatResponse}
vocabulary_flat_response = {
    HTTPStatus.OK: VocabularyFlatItem,
    HTTPStatus.NOT_FOUND: {
        'description': 'Type not found.',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
vocabulary_tree_response = {HTTPStatus.OK: VocabularyTreeResponse}
vocabulary_standard_by_class_response = {
    HTTPStatus.OK: VocabularyStandardResponse}

vocabulary_skos_response = {
    HTTPStatus.OK: {
        'description': 'Vocabulary hierarchy exported as a SKOS graph in '
                       'different RDF serialization formats.',
        'content': {
            'text/turtle': {
                'schema': {'type': 'string'}},
            'application/rdf+xml': {
                'schema': {'type': 'string'}},
            'application/ld+json': {
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'additionalProperties': True}}},
            'application/n-triples': {
                'schema': {'type': 'string'}}}},

    HTTPStatus.NOT_FOUND: {
        'description': 'Type not found.',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
