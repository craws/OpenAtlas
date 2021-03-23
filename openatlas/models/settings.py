from typing import Any, Dict, Optional, Union

from flask import g

from openatlas import app


class Settings:

    @staticmethod
    def get_settings() -> Dict[str, Any]:
        g.cursor.execute("SELECT name, value FROM web.settings;")
        settings: Dict[str, Union[str, bool, int]] = {}
        for name in app.config['MODULES']:  # Set default if doesn't exist (e.g. after an upgrade)
            settings['module_' + name] = False
        for row in g.cursor.fetchall():
            settings[row.name] = row.value
            if row.name in ['table_rows',
                            'failed_login_forget_minutes',
                            'failed_login_tries',
                            'file_upload_max_size',
                            'minimum_password_length',
                            'random_password_length',
                            'reset_confirm_hours']:
                settings[row.name] = int(row.value)
            if row.name in ['mail_recipients_feedback', 'file_upload_allowed_extension']:
                settings[row.name] = row.value.split(' ')
        return settings

    @staticmethod
    def update(form: Any) -> None:
        # For each setting: update or insert if doesn't exist (e.g. after an upgrade)
        sql = """
            INSERT INTO web.settings (name, value) VALUES (%(name)s, %(value)s)
            ON CONFLICT (name) DO UPDATE SET "value" = %(value)s;"""
        for field in form:
            if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
                continue
            value = field.data
            if field.type == 'BooleanField':
                value = 'True' if field.data else ''
            g.cursor.execute(sql, {'name': field.name, 'value': value})

    @staticmethod
    def set_logo(file_id: Optional[int] = None) -> None:
        sql = "UPDATE web.settings SET value = %(file_id)s WHERE name = 'logo_file_id';"
        g.cursor.execute(sql, {'file_id': file_id if file_id else ''})
