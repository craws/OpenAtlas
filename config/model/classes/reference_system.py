from typing import Any

from flask_babel import lazy_gettext as _


reference_system: dict[str, Any] = {
    'label': _('reference system'),
    'attributes': {
        'name': {
            'required': True},
        'website_url': {
            'label': _('website url'),
            'format': 'url'},
        'resolver_url': {
            'label': _('resolver url'),
            'format': 'url'},
        'example_id': {
            'label': _('example id')},
        'reference_system_classes': {
            'label': _('classes')},
        'description': {}},
    'relations': {},  # Added dynamically from database
    'display': {
        'buttons': ['insert'],
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {
            'note': {}}}}
