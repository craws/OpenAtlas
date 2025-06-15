from typing import Any

model: dict[str, Any] = {
    'acquisition': {
        'attributes': {
            'name': {'required': True},
            'info': {},
            'end': {'label': 'readout', 'required': True},
            'begin': {'label': 'published'}},
        'relations': {
            'book': {
                'label': 'tags',
                'class': 'type',
                'property': 'has type',
                'multiple': True,
                'inverse': True}},
        'display': {
            'columns': [
                'readout',
                'published',
                'name',
                'tag',
                'author',
                'info']}},
    'activity': {
        'attributes': {}},
    'actor_function': {
        'attributes': {}},
    'actor_relation': {
        'attributes': {}},
    'administrative_unit': {
        'attributes': {}},
    'appellation': {
        'attributes': {}},
    'artifact': {
        'attributes': {}},
    'bibliography': {
        'attributes': {}},
    'creation': {
        'attributes': {}},
    'edition': {
        'attributes': {}},
    'event': {
        'attributes': {}},
    'external_reference': {
        'attributes': {}},
    'feature': {
        'attributes': {}},
    'file': {
        'attributes': {}},
    'group': {
        'attributes': {}},
    'human_remains': {
        'attributes': {}},
    'involvement': {
        'attributes': {}},
    'modification': {
        'attributes': {}},
    'move': {
        'attributes': {}},
    'object_location': {
        'attributes': {}},
    'person': {
        'attributes': {}},
    'place': {
        'attributes': {}},
    'production': {
        'attributes': {}},
    'reference_system': {
        'attributes': {}},
    'source': {
        'attributes': {}},
    'source_translation': {
        'attributes': {}},
    'stratigraphic_unit': {
        'attributes': {}},
    'type': {
        'attributes': {}},
    'type_tools': {
        'attributes': {}},
}
