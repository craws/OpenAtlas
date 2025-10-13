from flask_babel import lazy_gettext as _

class_groups = {
    'actor': {
        'name': 'actor',
        'label': _('actor'),
        'classes': ['person', 'group'],
        'table_columns': ['name', 'class', 'begin', 'end', 'description']},
    'artifact': {
        'name': 'artifact',
        'label': _('artifact'),
        'classes': ['artifact', 'human_remains'],
        'table_columns': [
            'name', 'class', 'type', 'begin', 'end', 'description']},
    'event': {
        'name': 'event',
        'label': _('event'),
        'classes': [
            'activity', 'acquisition', 'modification', 'move', 'production'],
        'table_columns': [
            'name', 'class', 'type', 'begin', 'end', 'description']},
    'file': {
        'name': 'file',
        'label': _('file'),
        'classes': ['file'],
        'table_columns': [
            'created', 'icon', 'name', 'license', 'public', 'creator',
            'license holder', 'size', 'extension', 'description']},
    # 'object_location': {
    #    'name': 'object_location',
    #    'classes': ['object_location']},
    'place': {
        'name': 'place',
        'label': _('place'),
        'classes': ['feature', 'place', 'stratigraphic_unit'],
        'table_columns': [
            'name', 'class', 'type', 'begin', 'end', 'description']},
    'reference': {
        'name': 'reference',
        'label': _('reference'),
        'classes': ['bibliography', 'edition', 'external_reference'],
        'table_columns': ['name', 'class', 'type', 'description']},
    'reference_system': {
        'name': 'reference_system',
        'label': _('reference system'),
        'classes': ['reference_system'],
        'table_columns': [
            'name', 'count', 'website_url', 'resolver_url', 'example_id',
            'default_precision', 'description']},
    'source': {
        'name': 'source',
        'label': _('source'),
        'classes': ['source', 'source_translation'],
        'table_columns': ['name', 'class', 'type', 'content']},
    'type': {
        'name': 'type',
        'label': _('type'),
        'classes': ['administrative_unit', 'type'],
        'table_columns': ['name', 'description']}}

standard_relations = {
    'file': {
        'label': class_groups['file']['label'],
        'classes': class_groups['file']['classes'],
        'property': 'P67',
        'inverse': True,
        'multiple': True,
        'tab': {
            'additional_columns': ['main image'],
            'buttons': ['link', 'insert']}},
    'reference': {
        'label': class_groups['reference']['label'],
        'classes': class_groups['reference']['classes'],
        'property': 'P67',
        'inverse': True,
        'multiple': True,
        'additional_fields': ['page'],
        'tab': {
            'columns': ['name', 'class', 'type', 'page'],
            'buttons': ['link', 'insert']}},
    'source': {
        'classes': 'source',
        'property': 'P67',
        'inverse': True,
        'multiple': True,
        'tab': {
            'buttons': ['link', 'insert']}}}
