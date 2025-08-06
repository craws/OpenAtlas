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

# Todo: remove after finishing new classes
# def get_table_columns() -> dict[str, list[str]]:
#     columns = {
#         'entities': ['name', 'class', 'info'],
#         'external_reference': ['name', 'class', 'type', 'description'],
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
#     for view in ['actor', 'artifact', 'event', 'place']:
#         for class_ in class_groups[view]:
#             columns[class_] = columns[view]
#     return columns
