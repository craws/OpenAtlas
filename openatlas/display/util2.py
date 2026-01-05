# util2.py functions don't require the model (which prevents circular imports)
from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup
from flask_babel import gettext as _
from flask_login import current_user
from jinja2 import pass_context

from openatlas import app


@app.template_filter()
def sanitize(
        string: str | None,
        mode: Optional[str] = None) -> Optional[str]:
    if not string:
        return None
    if mode == 'ascii':
        return re.sub('[^A-Za-z0-9]+', '', string) or None
    return BeautifulSoup(string, "html.parser").get_text().replace("<>", "") \
        or None


def convert_size(size_bytes: int) -> str:
    if size_bytes <= 0:
        return '0 B'  # pragma: no cover
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    return f'{int(size_bytes / math.pow(1024, i))} {size_name[i]}'


def display_bool(value: bool, show_false: bool = True) -> str:
    return _('yes') if value else _('no') if show_false else ''


@pass_context  # Prevent Jinja2 context caching
@app.template_filter()
def is_authorized(context: str, group: Optional[str] = None) -> bool:
    if not group:  # In case it wasn't called from a template
        group = context
    if not current_user.is_authenticated or not hasattr(current_user, 'group'):
        return False
    match str(current_user.group):
        case 'admin':
            authorized = True
        case 'manager' if group in ['editor', 'contributor', 'readonly']:
            authorized = True
        case 'editor' if group in ['contributor', 'readonly']:
            authorized = True
        case 'contributor' if group in ['readonly']:
            authorized = True
        case _ if current_user.group == group:
            authorized = True
        case _:
            authorized = False
    return authorized


@app.template_filter()
def uc_first(string: Optional[str] = None) -> str:
    return str(string)[0].upper() + str(string)[1:] if string else ''


@app.template_filter()
def manual(site: str) -> str:
    """ If the manual page exists, return the link to it"""
    parts = site.split('/')
    if len(parts) < 2 or parts[1] in ['entities', 'info', 'subs']:
        return ''
    path = \
        Path(app.root_path) / 'static' / 'manual' / parts[0] / \
        (parts[1] + '.html')
    if not path.exists():
        # print(f'Missing manual link: {path}')
        return ''
    return f"""
        <a title="{uc_first(_('manual'))}"
            href="/static/manual/{site}.html" class="manual"
            target="_blank"
            rel="noopener noreferrer">
          <i class="fas fs-4 fa-book"></i>
        </a>"""
