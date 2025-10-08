from typing import Any

from flask_babel import lazy_gettext as _


reference_system: dict[str, Any] = {
    'label': _('reference system'),
    'attributes': {
        'name': {
            'required': True},
        'website_url': {
            'label': _('website URL'),
            'format': 'url'},
        'resolver_url': {
            'label': _('resolver URL'),
            'format': 'url'},
        'placeholder': {
            'label': _('example ID')},
        'precision_default': {
            'label': _('precision default')},
        'classes': {
            'label': _('')},
        'description': {}},
    'display': {
        'buttons': ['insert'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}
