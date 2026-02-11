#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

# pylint: disable=invalid-name
version = '9.1.0'
release = '9.1.0'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'OpenAtlas'
author = 'The OpenAtlas team'
language = 'en'
pygments_style = 'sphinx'
extensions: List[str] = ['sphinx.ext.extlinks']
extlinks = {
    'cidoc_entity': (
        'https://www.cidoc-crm.org/Entity/%s/version-7.1',
        'cidoc_entity %s'),
    'cidoc_property': (
        'https://www.cidoc-crm.org/Property/%s/version-7.1',
        'cidoc_property %s')}

html_logo = 'logo.png'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_domain_indices = False
html_use_index = False
html_copy_source = False  # Prevent including source html files
html_show_copyright = False

html_theme_options = {
    'style_external_links': True,
    'navigation_depth': 2}
