from flask_babel import lazy_gettext as _

class_groups = {
    'actor': {
        'name': 'actor',
        'classes': ['person', 'group'],
        'table_columns': ['name', 'class', 'begin', 'end', 'description']},
    'artifact': {
        'name': 'artifact',
        'classes': ['artifact', 'human_remains'],
        'table_columns': [
            'name', 'class', 'type', 'begin', 'end', 'description']},
    'event': {
        'name': 'event',
        'classes': [
            'activity', 'acquisition', 'creation', 'event', 'modification',
            'move', 'production'],
        'table_columns': [
            'name', 'class', 'type', 'begin', 'end', 'description']},
    'file': {
        'name': 'file',
        'classes': ['file'],
        'table_columns': [
            'name', 'license', 'public', 'creator', 'license holder',
            'size', 'extension', 'description']},
    # 'object_location': {
    #    'name': 'object_location',
    #    'classes': ['object_location']},
    'place': {
        'name': 'place',
        'classes': ['feature', 'place', 'stratigraphic_unit'],
        'table_columns': [
            'name', 'class', 'type', 'begin', 'end', 'description']},
    'reference': {
        'name': 'reference',
        'classes': ['bibliography', 'edition', 'external_reference'],
        'table_columns': ['name', 'class', 'type', 'description']},
    'reference_system': {
        'name': 'reference_system',
        'classes': ['reference_system'],
        'table_columns': ['name', 'class', 'type', 'description']},
    'source': {
        'name': 'source',
        'classes': ['source'],
        'table_columns': ['name', 'type', 'content']},
    'source_translation': {
        'name': 'source_translation',
        'classes': ['source_translation'],
        'table_columns': ['name', 'type', 'content']},
    'type': {
        'name': 'type',
        'classes': ['administrative_unit', 'type'],
        'table_columns': ['name', 'description']}}

standard_relations = {
    'file': {
        'relation': {
            'label': _('file'),
            'classes': class_groups['file']['classes'],
            'properties': 'P67',
            'inverse': True,
            'multiple': True},
        'tab': {
            'additional_columns': ['main image', 'remove'],
            'buttons': ['link', 'insert']}},
    'reference': {
        'relation': {
            'label': _('reference'),
            'classes': class_groups['reference']['classes'],
            'properties': 'P67',
            'inverse': True,
            'multiple': True,
            'additional_fields': ['page']},
        'tab': {
            'mode': 'link',
            'additional_columns': ['page', 'update', 'remove'],
            'buttons': ['link', 'insert']}},
    'source': {
        'relation': {
            'label': _('source'),
            'classes': 'source',
            'properties': 'P67',
            'inverse': True,
            'multiple': True},
        'tab': {
            'additional_columns': ['remove'],
            'buttons': ['link', 'insert']},
    }}

# Todo: remove after finishing new classes
# def get_table_columns() -> dict[str, list[str]]:
#     columns = {
#         'entities': ['name', 'class', 'info'],
#         'member': ['member', 'function', 'first', 'last', 'description'],
#         'member_of': [
#             'member of', 'function', 'first', 'last', 'description'],
#         'note': ['date', 'visibility', 'user', 'note'],
#         'relation': ['relation', 'actor', 'first', 'last', 'description'],
#         'reference_system': [
#             'name', 'count', 'website URL', 'resolver URL', 'example ID',
#             'default precision', 'description'],
#         'subs': ['name', 'count', 'info'],
#         'text': ['text', 'type', 'content']}
