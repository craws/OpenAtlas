from typing import Any, Optional

from openatlas.database.settings import Settings as Db


class Settings:
    MODULES = ['map_overlay', 'sub_units']

    @staticmethod
    def get_settings() -> dict[str, Any]:
        settings: dict[str, Any] = {}
        for name in Settings.MODULES:  # Set empty in case it doesn't exist
            settings[f'module_{name}'] = ''
        for name, value in Db.get_settings().items():
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
        for name, value in data.items():
            Db.update(name, value)

    @staticmethod
    def set_logo(file_id: Optional[int] = None) -> None:
        Db.set_logo(file_id or '')
