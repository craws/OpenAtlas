from typing import Any, Dict, List, Union

from flask import g


class Settings:

    @staticmethod
    def get_settings() -> List[Dict[str, str]]:
        g.cursor.execute("SELECT name, value FROM web.settings;")
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def update(field_name: str, value: Any) -> None:
        g.cursor.execute(
            """
            INSERT INTO web.settings (name, value) VALUES (%(name)s, %(value)s)
            ON CONFLICT (name) DO UPDATE SET "value" = %(value)s;""",
            {'name': field_name, 'value': value})

    @staticmethod
    def set_logo(file_id: Union[int, str] = None) -> None:
        g.cursor.execute(
            """
            UPDATE web.settings
            SET value = %(file_id)s
            WHERE name = 'logo_file_id';""", {'file_id': file_id})
