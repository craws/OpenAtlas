from typing import Any, Dict, Optional

from flask import g


class Settings:

    @staticmethod
    def get_settings() -> Dict[str, Any]:
        g.execute("SELECT name, value FROM web.settings;")
        settings = {}
        for row in g.cursor.fetchall():
            settings[row.name] = row.value
            if row.name in ['default_table_rows',
                            'failed_login_forget_minutes',
                            'failed_login_tries',
                            'file_upload_max_size',
                            'minimum_password_length',
                            'random_password_length',
                            'reset_confirm_hours']:
                settings[row.name] = int(row.value)
        return settings

    @staticmethod
    def update(form: Any) -> None:
        sql = 'UPDATE web.settings SET "value" = %(value)s WHERE "name" = %(name)s;'
        for field in form:
            if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
                continue
            value = field.data
            if field.type == 'BooleanField':
                value = 'True' if field.data else ''
            g.execute(sql, {'name': field.name, 'value': value})

    @staticmethod
    def set_logo(file_id: Optional[int] = None) -> None:
        sql = "UPDATE web.settings SET value = %(file_id)s WHERE name = 'logo_file_id';"
        g.execute(sql, {'file_id': file_id if file_id else ''})
