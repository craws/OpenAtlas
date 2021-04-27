from __future__ import annotations  # Needed for Python 4.0 type annotations

import math
import os
import smtplib
from datetime import datetime, timedelta
from email.header import Header
from email.mime.text import MIMEText
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from flask import flash, request, session, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from openatlas import app, logger

if TYPE_CHECKING:  # pragma: no cover - Type checking is disabled in tests
    from openatlas.models.entity import Entity


def send_mail(
        subject: str,
        text: str,
        recipients: Union[str, List[str]],
        log_body: bool = True) -> bool:  # pragma: no cover
    """Send one mail to every recipient, set log_body to False for sensitive data e.g. passwords"""
    recipients = recipients if isinstance(recipients, list) else [recipients]
    settings = session['settings']
    if not settings['mail'] or len(recipients) < 1:
        return False
    mail_user = settings['mail_transport_username']
    from_ = settings['mail_from_name'] + ' <' + settings['mail_from_email'] + '>'
    server = smtplib.SMTP(settings['mail_transport_host'], settings['mail_transport_port'])
    server.ehlo()
    server.starttls()
    try:
        if settings['mail_transport_username']:
            server.login(mail_user, app.config['MAIL_PASSWORD'])
        for recipient in recipients:
            msg = MIMEText(text, _charset='utf-8')
            msg['From'] = from_
            msg['To'] = recipient.strip()
            msg['Subject'] = Header(subject.encode('utf-8'), 'utf-8')
            server.sendmail(settings['mail_from_email'], recipient, msg.as_string())
        log_text = 'Mail from ' + from_ + ' to ' + ', '.join(recipients) + ' Subject: ' + subject
        log_text += ' Content: ' + text if log_body else ''
        logger.log('info', 'mail', 'Mail send from ' + from_, log_text)
    except smtplib.SMTPAuthenticationError as e:
        logger.log('error', 'mail', 'Error mail login for ' + mail_user, e)
        flash(_('error mail login'), 'error')
        return False
    except Exception as e:
        logger.log('error', 'mail', 'Error send mail for ' + mail_user, e)
        flash(_('error mail send'), 'error')
        return False
    return True


def get_file_stats(path: Path = app.config['UPLOAD_DIR']) -> Dict[Union[int, str], Any]:
    """For performance: Build a dict with file ids and stats from files in given directory."""
    file_stats: Dict[Union[int, str], Any] = {}
    for file in path.iterdir():
        if file.stem.isdigit():
            file_stats[int(file.stem)] = {
                'ext': file.suffix,
                'size': file.stat().st_size,
                'date': file.stat().st_ctime}
    return file_stats


def get_disk_space_info() -> Optional[Dict[str, Any]]:
    from openatlas.util.filters import convert_size
    if os.name != "posix":  # pragma: no cover - e.g. Windows has no statvfs
        return None
    statvfs = os.statvfs(app.config['UPLOAD_DIR'])
    disk_space = statvfs.f_frsize * statvfs.f_blocks
    free_space = statvfs.f_frsize * statvfs.f_bavail  # Available space without reserved blocks
    return {
        'total': convert_size(statvfs.f_frsize * statvfs.f_blocks),
        'free': convert_size(statvfs.f_frsize * statvfs.f_bavail),
        'percent': 100 - math.ceil(free_space / (disk_space / 100))}


def was_modified(form: FlaskForm, entity: 'Entity') -> bool:  # pragma: no cover
    if not entity.modified or not form.opened.data:
        return False
    if entity.modified < datetime.fromtimestamp(float(form.opened.data)):
        return False
    logger.log('info', 'multi user', 'Multi user overwrite prevented.')
    return True


def is_float(value: Union[int, float]) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


@app.template_filter()
def is_authorized(group: str) -> bool:
    if not current_user.is_authenticated or not hasattr(current_user, 'group'):
        return False  # pragma: no cover - needed because AnonymousUserMixin has no group
    if current_user.group == 'admin' or (
            current_user.group == 'manager' and group in
            ['manager', 'editor', 'contributor', 'readonly']) or (
            current_user.group == 'editor' and group in ['editor', 'contributor',
                                                         'readonly']) or (
            current_user.group == 'contributor' and group in ['contributor', 'readonly']) or (
            current_user.group == 'readonly' and group == 'readonly'):
        return True
    return False


def required_group(group: str):  # type: ignore
    def wrapper(f):  # type: ignore
        @wraps(f)
        def wrapped(*args, **kwargs):  # type: ignore
            if not current_user.is_authenticated:
                return redirect(url_for('login', next=request.path))
            if not is_authorized(group):
                abort(403)
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def get_backup_file_data() -> Dict[str, Any]:
    from openatlas.util.filters import convert_size, format_date
    path = app.config['EXPORT_DIR'] / 'sql'
    latest_file = None
    latest_file_date = None
    for file in [f for f in path.iterdir() if (path / f).is_file()]:
        if file.name == '.gitignore':
            continue
        file_date = datetime.utcfromtimestamp((path / file).stat().st_ctime)
        if not latest_file_date or file_date > latest_file_date:
            latest_file = file
            latest_file_date = file_date
    file_data: Dict[str, Any] = {'backup_too_old': True}
    if latest_file and latest_file_date:
        yesterday = datetime.today() - timedelta(days=1)
        file_data['file'] = latest_file.name
        file_data['backup_too_old'] = True if yesterday > latest_file_date else False
        file_data['size'] = convert_size(latest_file.stat().st_size)
        file_data['date'] = format_date(latest_file_date)
    return file_data
