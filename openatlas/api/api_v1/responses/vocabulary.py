from openatlas.api.api_v1.models.vocabulary import (
    VocabularyFlatResponse, VocabularyTreeResponse, VocabularyStandardResponse)

vocabulary_list_response = {200: VocabularyFlatResponse}
vocabulary_tree_response = {200: VocabularyTreeResponse}
vocabulary_standard_by_class_response = {200: VocabularyStandardResponse}
