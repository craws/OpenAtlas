# util2.py functions don't require the model (which prevents circular imports)
from __future__ import annotations

import math
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from bs4 import BeautifulSoup
from flask_babel import lazy_gettext as _
from flask_login import current_user
from jinja2 import pass_context

from openatlas import app
from openatlas.models.dates import format_date


@app.template_filter()
def sanitize(string: str | None, mode: Optional[str] = None) -> Optional[str]:
    if not string:
        return None
    if mode == 'ascii':
        return re.sub('[^A-Za-z0-9]+', '', string) or None
    return BeautifulSoup(string, "html.parser").get_text().replace("<>", "") \
        or None


def convert_size(size_bytes: int) -> str:
    if size_bytes <= 0:
        return "0 B"  # pragma: no cover
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    return f"{int(size_bytes / math.pow(1024, i))} {size_name[i]}"


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
def uc_first(string: str) -> str:
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
    return \
        '<a title="' + uc_first(_('manual')) + '" ' \
        f'href="/static/manual/{site}.html" class="manual" ' \
        f'target="_blank" rel="noopener noreferrer">' \
        f'<i class="fas fs-4 fa-book"></i></a>'


def get_backup_file_data() -> dict[str, Any]:
    path = app.config['SQL_PATH']
    latest_file = None
    latest_file_date = None
    for file in [
            f for f in path.iterdir()
            if (path / f).is_file() and f.name != '.gitignore']:
        file_date = datetime.fromtimestamp((path / file).stat().st_ctime)
        if not latest_file_date or file_date > latest_file_date:
            latest_file = file
            latest_file_date = file_date
    file_data: dict[str, Any] = {'backup_too_old': True}
    if latest_file and latest_file_date:
        yesterday = datetime.today() - timedelta(days=1)
        file_data['file'] = latest_file.name
        file_data['backup_too_old'] = \
            bool(yesterday > latest_file_date and not app.testing)
        file_data['size'] = convert_size(latest_file.stat().st_size)
        file_data['date'] = format_date(latest_file_date)
    return file_data
