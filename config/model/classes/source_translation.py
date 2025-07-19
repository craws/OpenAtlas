from flask_babel import lazy_gettext as _

model = {
    'attributes': {
        'name': {'required': True},
        'description': {'label': _('content'), 'annotated': True}},
    'relations': {
        'source': {
            'class': 'source',
            'property': 'P73',
            'inverse': True,
            'required': True,
            'mode': 'direct'}},
    'display': {
        'form': {'insert_and_continue': True},
        'tabs': {
            'note': {}}}}
