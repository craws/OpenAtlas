from typing import Any, Optional

from openatlas.database import settings as db
from openatlas.display.util2 import sanitize

MODULES = ['map_overlay', 'time']


def get_settings() -> dict[str, Any]:
    settings: dict[str, Any] = {}
    for name in MODULES:  # Set empty in case it doesn't exist
        settings[f'module_{name}'] = ''
    for name, value in db.get_settings().items():
        settings[name] = value
        if name in [
                'table_rows',
                'failed_login_forget_minutes',
                'failed_login_tries',
                'file_upload_max_size',
                'minimum_password_length',
                'random_password_length',
                'reset_confirm_hours']:
            settings[name] = int(value)
        elif name in [
                'mail_recipients_feedback',
                'file_upload_allowed_extension']:
            settings[name] = value.split(' ')
    return settings


def update_settings(data: dict[str, str]) -> None:
    for k, v in data.items():
        db.update(k, sanitize(v) or '' if isinstance(v, str) else v)


def set_logo(file_id: Optional[int] = None) -> None:
    db.set_logo(file_id or '')
