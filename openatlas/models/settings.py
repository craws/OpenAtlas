from typing import Any, Optional

from flask import g

from openatlas.database import settings as db
from openatlas.database.connect import Transaction
from openatlas.display.util2 import sanitize


class Settings:
    MODULES = ['map_overlay', 'time']

    @staticmethod
    def get_settings() -> dict[str, Any]:
        settings: dict[str, Any] = {}
        for name in Settings.MODULES:  # Set empty in case it doesn't exist
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

    @staticmethod
    def update(data: dict[str, str]) -> None:
        Transaction.begin()
        try:
            for name, value in data.items():
                db.update(
                    name,
                    sanitize(value) or '' if isinstance(value, str) else value)
            Transaction.commit()
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            raise e from None

    @staticmethod
    def set_logo(file_id: Optional[int] = None) -> None:
        db.set_logo(file_id or '')
